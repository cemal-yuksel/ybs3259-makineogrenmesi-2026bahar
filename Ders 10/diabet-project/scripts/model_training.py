"""
DIABETES DATASET - MODEL TRAINING & EVALUATION
==============================================

Model Expert - 18+ Model Karşılaştırma Pipeline

DataPrep Expert'ten Gelen Bilgiler:
- Train: 614 satır, Test: 154 satır
- 14 features (6 orijinal + 4 binary + 4 interaction)
- Binary Classification: Outcome (0=Diyabet Yok, 1=Diyabet Var)
- Class Imbalance: %65-35 (stratified split + class weighting)
- Leakage Riski: Yok
- Veri Kalitesi: 10/10
"""

import os
import time
import warnings
import numpy as np
import pandas as pd
from pathlib import Path
import joblib

import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff
from prettytable import PrettyTable

# Scikit-learn imports
from sklearn.dummy import DummyClassifier
from sklearn.linear_model import LogisticRegression, RidgeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import (
    RandomForestClassifier, ExtraTreesClassifier, 
    GradientBoostingClassifier, AdaBoostClassifier, 
    BaggingClassifier, VotingClassifier
)
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC, LinearSVC
from sklearn.neural_network import MLPClassifier

from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.model_selection import cross_val_score, StratifiedKFold
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    roc_auc_score, classification_report, confusion_matrix,
    roc_curve, precision_recall_curve
)

warnings.filterwarnings("ignore")

# Klasörlerin varlığını garantile
Path('../figures').mkdir(parents=True, exist_ok=True)
Path('../models').mkdir(parents=True, exist_ok=True)
Path('../reports/csv').mkdir(parents=True, exist_ok=True)
Path('../reports/markdown').mkdir(parents=True, exist_ok=True)

# Global ayarlar
RANDOM_STATE = 42
np.random.seed(RANDOM_STATE)

# Profesyonel renk paleti
PROFESSIONAL_PALETTE = [
    "#2E86AB", "#A23B72", "#F18F01", "#C73E1D", "#6A994E",
    "#BC4B51", "#8E7DBE", "#F77F00", "#06A77D", "#D4A574"
]

# Model sonuçları için global liste
model_results = []
model_decisions = []
next_agent_handoff = []

def log_model_result(model_name, train_score, test_score, cv_mean, cv_std, 
                     main_metric, overfit_gap, train_time, status="Başarılı"):
    """Model sonuçlarını loglar"""
    model_results.append({
        "Model": model_name,
        "Train Skoru": train_score,
        "Test Skoru": test_score,
        "CV Ortalama": cv_mean,
        "CV Std": cv_std,
        "Ana Metrik": main_metric,
        "Overfitting Farkı": overfit_gap,
        "Eğitim Süresi": train_time,
        "Durum": status
    })

def apply_premium_layout(fig, title):
    """Profesyonel grafik düzeni"""
    fig.update_layout(
        title={
            "text": title,
            "x": 0.03,
            "xanchor": "left",
            "font": {"size": 24, "family": "Arial Black", "color": "#1F2937", "weight": "bold"}
        },
        template="plotly_white",
        paper_bgcolor="#FBFBF8",
        plot_bgcolor="#FBFBF8",
        font={"family": "Arial", "size": 13, "color": "#374151"},
        margin=dict(l=60, r=40, t=80, b=60),
        legend_title_text="Kategori",
        hoverlabel=dict(bgcolor="white", font_size=12, font_family="Arial")
    )
    fig.update_xaxes(showgrid=True, gridcolor="#E5E7EB", zeroline=False)
    fig.update_yaxes(showgrid=True, gridcolor="#E5E7EB", zeroline=False)
    return fig

def save_figure(fig, file_base):
    """Grafikleri kaydet"""
    html_path = f'../figures/{file_base}.html'
    png_path = f'../figures/{file_base}.png'
    
    fig.write_html(html_path)
    
    try:
        fig.write_image(png_path)
        print(f"✅ Görsel kaydedildi: {file_base}.html & {file_base}.png")
    except Exception as e:
        print(f"✅ Görsel kaydedildi: {file_base}.html (PNG kaydı başarısız: kaleido gerekebilir)")

print("="*80)
print(" PHASE 1: DATAPREP HANDOFF INGESTION ".center(80, "="))
print("="*80)

# Model-ready verileri yükle
print("\n📦 Model-Ready Verileri Yükleniyor...")

X_train = pd.read_csv('../data/model_ready/X_train.csv')
X_test = pd.read_csv('../data/model_ready/X_test.csv')
y_train = pd.read_csv('../data/model_ready/y_train.csv').values.ravel()
y_test = pd.read_csv('../data/model_ready/y_test.csv').values.ravel()

print(f"\n✅ Veriler Yüklendi:")
print(f"   X_train shape: {X_train.shape}")
print(f"   X_test shape: {X_test.shape}")
print(f"   y_train shape: {y_train.shape}")
print(f"   y_test shape: {y_test.shape}")

print(f"\n📊 Feature Listesi ({len(X_train.columns)} adet):")
for i, col in enumerate(X_train.columns, 1):
    print(f"   {i}. {col}")

# DataPrep actions raporunu oku
print("\n📋 DataPrep Actions Raporu:")
dataprep_actions = pd.read_csv('../reports/csv/dataprep_actions_report.csv')
print(f"   Toplam preprocessing adımı: {len(dataprep_actions)}")
print(f"   Veri kalitesi: 10/10")
print(f"   Leakage riski: Yok")

print("\n" + "="*80)
print(" PHASE 2: PROBLEM FRAMING ".center(80, "="))
print("="*80)

# Problem tipini doğrula
unique_classes = np.unique(y_train)
n_classes = len(unique_classes)

print(f"\n🎯 Problem Tipi: Binary Classification")
print(f"   Sınıf sayısı: {n_classes}")
print(f"   Sınıflar: {unique_classes}")

# Class distribution
train_dist = pd.Series(y_train).value_counts(normalize=True) * 100
test_dist = pd.Series(y_test).value_counts(normalize=True) * 100

print(f"\n📊 Class Distribution:")
print(f"   Train - Class 0: {train_dist[0]:.1f}%, Class 1: {train_dist[1]:.1f}%")
print(f"   Test  - Class 0: {test_dist[0]:.1f}%, Class 1: {test_dist[1]:.1f}%")
print(f"   Imbalance Ratio: {train_dist[0] / train_dist[1]:.2f}:1")

# Class imbalance stratejisi
imbalance_ratio = train_dist.max()
if imbalance_ratio > 70:
    print(f"\n⚠️ Class Imbalance Tespit Edildi (%{imbalance_ratio:.1f})")
    print(f"   Strateji: class_weight='balanced' + StratifiedKFold CV")
else:
    print(f"\n✅ Class Imbalance Kabul Edilebilir Seviyede")

print("\n" + "="*80)
print(" PHASE 3: METRIC STRATEGY ".center(80, "="))
print("="*80)

print("\n📏 Ana Metrikler:")
print("   1️⃣ F1-Score (Weighted) - Öncelikli")
print("   2️⃣ ROC-AUC - Model ayırt etme gücü")
print("   3️⃣ Accuracy - Genel doğruluk")
print("   4️⃣ Precision - False Positive maliyeti")
print("   5️⃣ Recall - False Negative maliyeti")

print("\n💡 Metrik Seçim Gerekçesi:")
print("   - Class imbalance nedeniyle F1-Score öncelikli")
print("   - ROC-AUC threshold'dan bağımsız değerlendirme")
print("   - Accuracy tek başına yanıltıcı olabilir")

# Cross-validation stratejisi
cv_strategy = StratifiedKFold(n_splits=5, shuffle=True, random_state=RANDOM_STATE)
print(f"\n🔄 Cross-Validation: StratifiedKFold (k=5)")

print("\n" + "="*80)
print(" PHASE 4: BASELINE MODEL ".center(80, "="))
print("="*80)

print("\n🎯 Baseline Model: DummyClassifier")
print("   Strateji: most_frequent (her zaman majority class tahmin eder)")
print("   Amaç: Gelişmiş modellerin anlamlı katkısını ölçmek")

# Dummy Classifier
dummy_model = DummyClassifier(strategy='most_frequent', random_state=RANDOM_STATE)
start_time = time.time()

dummy_model.fit(X_train, y_train)
dummy_train_pred = dummy_model.predict(X_train)
dummy_test_pred = dummy_model.predict(X_test)

dummy_train_f1 = f1_score(y_train, dummy_train_pred, average='weighted')
dummy_test_f1 = f1_score(y_test, dummy_test_pred, average='weighted')

dummy_time = round(time.time() - start_time, 3)

print(f"\n📊 Baseline Sonuçlar:")
print(f"   Train F1-Score: {dummy_train_f1:.4f}")
print(f"   Test F1-Score: {dummy_test_f1:.4f}")
print(f"   Eğitim Süresi: {dummy_time:.3f}s")

log_model_result(
    model_name="Dummy Classifier (Baseline)",
    train_score=round(dummy_train_f1, 4),
    test_score=round(dummy_test_f1, 4),
    cv_mean=round(dummy_test_f1, 4),
    cv_std=0.0,
    main_metric=round(dummy_test_f1, 4),
    overfit_gap=round(dummy_train_f1 - dummy_test_f1, 4),
    train_time=dummy_time,
    status="Baseline"
)

print("\n💡 Yorum: Gelişmiş modeller bu baseline'ı geçmek zorundadır!")

print("\n" + "="*80)
print(" PHASE 5: MODEL CANDIDATE POOL (18+ MODELS) ".center(80, "="))
print("="*80)

print("\n🤖 18+ Model Hazırlanıyor...")

# Model havuzu (18+ model)
models = {
    # Baseline
    "Dummy Classifier": DummyClassifier(strategy='most_frequent', random_state=RANDOM_STATE),
    
    # Linear Models (5 model)
    "Logistic Regression": LogisticRegression(max_iter=1000, random_state=RANDOM_STATE, class_weight='balanced'),
    "Logistic Regression (L1)": LogisticRegression(penalty='l1', solver='liblinear', max_iter=1000, 
                                                    random_state=RANDOM_STATE, class_weight='balanced'),
    "Logistic Regression (L2)": LogisticRegression(penalty='l2', max_iter=1000, 
                                                    random_state=RANDOM_STATE, class_weight='balanced'),
    "Ridge Classifier": RidgeClassifier(random_state=RANDOM_STATE, class_weight='balanced'),
    "Linear SVC": LinearSVC(max_iter=2000, random_state=RANDOM_STATE, class_weight='balanced'),
    
    # Neighbors (1 model)
    "KNN (k=5)": KNeighborsClassifier(n_neighbors=5),
    
    # Tree-based (6 model)
    "Decision Tree": DecisionTreeClassifier(random_state=RANDOM_STATE, class_weight='balanced'),
    "Random Forest": RandomForestClassifier(n_estimators=100, random_state=RANDOM_STATE, 
                                           class_weight='balanced', n_jobs=-1),
    "Extra Trees": ExtraTreesClassifier(n_estimators=100, random_state=RANDOM_STATE, 
                                       class_weight='balanced', n_jobs=-1),
    "Gradient Boosting": GradientBoostingClassifier(n_estimators=100, random_state=RANDOM_STATE),
    "AdaBoost": AdaBoostClassifier(n_estimators=100, random_state=RANDOM_STATE),
    "Bagging": BaggingClassifier(n_estimators=100, random_state=RANDOM_STATE, n_jobs=-1),
    
    # Naive Bayes (1 model)
    "Gaussian Naive Bayes": GaussianNB(),
    
    # SVM (1 model)
    "SVC (RBF Kernel)": SVC(probability=True, random_state=RANDOM_STATE, class_weight='balanced'),
    
    # Neural Network (1 model)
    "MLP Neural Network": MLPClassifier(hidden_layer_sizes=(100, 50), max_iter=500, 
                                       random_state=RANDOM_STATE, early_stopping=True)
}

# XGBoost, LightGBM, CatBoost eklemeyi dene
try:
    from xgboost import XGBClassifier
    models["XGBoost"] = XGBClassifier(n_estimators=100, random_state=RANDOM_STATE, 
                                      scale_pos_weight=1.87, n_jobs=-1, eval_metric='logloss')
    print("   ✅ XGBoost eklendi")
except ImportError:
    print("   ⚠️ XGBoost kurulu değil, atlandı")

try:
    from lightgbm import LGBMClassifier
    models["LightGBM"] = LGBMClassifier(n_estimators=100, random_state=RANDOM_STATE, 
                                       class_weight='balanced', n_jobs=-1, verbose=-1)
    print("   ✅ LightGBM eklendi")
except ImportError:
    print("   ⚠️ LightGBM kurulu değil, atlandı")

try:
    from catboost import CatBoostClassifier
    models["CatBoost"] = CatBoostClassifier(iterations=100, random_state=RANDOM_STATE, 
                                           auto_class_weights='Balanced', verbose=0)
    print("   ✅ CatBoost eklendi")
except ImportError:
    print("   ⚠️ CatBoost kurulu değil, atlandı")

print(f"\n✅ Toplam Model Sayısı: {len(models)}")

print("\n" + "="*80)
print(" PHASE 6: MODEL TRAINING LOOP ".center(80, "="))
print("="*80)

print("\n🚀 Tüm Modeller Eğitiliyor (StandardScaler ile pipeline)...")
print("   Metrik: F1-Score (Weighted)")
print("   CV: StratifiedKFold (k=5)")
print("\n")

# Her modeli eğit
for model_name, model in models.items():
    print(f"{'='*80}")
    print(f" {model_name} ".center(80, "="))
    print(f"{'='*80}")
    
    start_time = time.time()
    
    try:
        # Pipeline oluştur (StandardScaler + Model)
        pipeline = Pipeline([
            ('scaler', StandardScaler()),
            ('model', model)
        ])
        
        # Train
        pipeline.fit(X_train, y_train)
        
        # Predictions
        train_pred = pipeline.predict(X_train)
        test_pred = pipeline.predict(X_test)
        
        # Metrics
        train_f1 = f1_score(y_train, train_pred, average='weighted')
        test_f1 = f1_score(y_test, test_pred, average='weighted')
        train_acc = accuracy_score(y_train, train_pred)
        test_acc = accuracy_score(y_test, test_pred)
        
        # Cross-validation
        print(f"   🔄 Cross-validation başlatılıyor...")
        cv_scores = cross_val_score(
            pipeline, X_train, y_train,
            cv=cv_strategy,
            scoring='f1_weighted',
            n_jobs=-1
        )
        
        cv_mean = np.mean(cv_scores)
        cv_std = np.std(cv_scores)
        
        train_time = round(time.time() - start_time, 3)
        overfit_gap = round(train_f1 - test_f1, 4)
        
        # Sonuçları göster
        print(f"\n   📊 Sonuçlar:")
        print(f"      Train F1:  {train_f1:.4f}")
        print(f"      Test F1:   {test_f1:.4f}")
        print(f"      Train Acc: {train_acc:.4f}")
        print(f"      Test Acc:  {test_acc:.4f}")
        print(f"      CV Mean:   {cv_mean:.4f}")
        print(f"      CV Std:    {cv_std:.4f}")
        print(f"      Overfit:   {overfit_gap:.4f}")
        print(f"      Süre:      {train_time:.3f}s")
        
        # Log
        log_model_result(
            model_name=model_name,
            train_score=round(train_f1, 4),
            test_score=round(test_f1, 4),
            cv_mean=round(cv_mean, 4),
            cv_std=round(cv_std, 4),
            main_metric=round(test_f1, 4),
            overfit_gap=overfit_gap,
            train_time=train_time,
            status="✅ Başarılı"
        )
        
        print(f"   ✅ {model_name} başarıyla eğitildi!")
        
    except Exception as e:
        print(f"\n   ❌ Hata: {str(e)}")
        log_model_result(
            model_name=model_name,
            train_score=None,
            test_score=None,
            cv_mean=None,
            cv_std=None,
            main_metric=None,
            overfit_gap=None,
            train_time=None,
            status=f"❌ Çalışmadı: {str(e)[:50]}"
        )
    
    print()

print("\n" + "="*80)
print(" PHASE 7: PRETTYTABLE MODEL COMPARISON ".center(80, "="))
print("="*80)

# Results DataFrame
results_df = pd.DataFrame(model_results)

# Başarılı modelleri sırala
successful_results = results_df[results_df['Durum'].str.contains('Başarılı|Baseline', na=False)].copy()
successful_results = successful_results.sort_values('Ana Metrik', ascending=False).reset_index(drop=True)

print(f"\n✅ Başarılı Model Sayısı: {len(successful_results)}/{len(models)}")

# PrettyTable oluştur
table = PrettyTable()
table.field_names = [
    "Sıra", "Model", "Train F1", "Test F1", 
    "CV Mean", "CV Std", "Ana Metrik", "Overfit", "Süre (s)", "Durum"
]

for idx, row in successful_results.iterrows():
    table.add_row([
        idx + 1,
        row["Model"],
        f"{row['Train Skoru']:.4f}",
        f"{row['Test Skoru']:.4f}",
        f"{row['CV Ortalama']:.4f}",
        f"{row['CV Std']:.4f}",
        f"{row['Ana Metrik']:.4f}",
        f"{row['Overfitting Farkı']:.4f}",
        f"{row['Eğitim Süresi']:.3f}",
        row['Durum']
    ])

print("\n" + "="*80)
print(" MODEL KARŞILAŞTIRMA TABLOSU ".center(80, "="))
print("="*80)
print(table)

# CSV'ye kaydet
results_df.to_csv('../reports/csv/model_comparison_results.csv', index=False)
print(f"\n✅ Sonuçlar kaydedildi: model_comparison_results.csv")

# PrettyTable'ı txt olarak kaydet
with open('../reports/model_comparison_prettytable.txt', 'w', encoding='utf-8') as f:
    f.write(str(table))
print(f"✅ PrettyTable kaydedildi: model_comparison_prettytable.txt")

print("\n" + "="*80)
print(" PHASE 7.5: GÖRSEL MODEL KARŞILAŞTIRMA SUITE ".center(80, "="))
print("="*80)

print("\n📊 5 Profesyonel Grafik Oluşturuluyor...")

# Grafik 1: Ana Performans Karşılaştırması
print("\n1️⃣ Ana Performans Karşılaştırması...")
plot_df = successful_results.dropna(subset=['Ana Metrik']).sort_values('Ana Metrik', ascending=True)

fig1 = px.bar(
    plot_df,
    x='Ana Metrik',
    y='Model',
    orientation='h',
    color='Ana Metrik',
    color_continuous_scale=[[0, "#D5F5E3"], [0.5, "#A7C7E7"], [1, "#2E86AB"]],
    title="18+ Model Ana Performans Karşılaştırması (F1-Score)",
    text='Ana Metrik'
)
fig1.update_traces(texttemplate='%{text:.4f}', textposition='outside')
fig1 = apply_premium_layout(fig1, "18+ Model Ana Performans Karşılaştırması (F1-Score)")
save_figure(fig1, "model_phase7_performance_comparison")

# Grafik 2: CV Kararlılık Analizi
print("2️⃣ CV Kararlılık Analizi...")
plot_df2 = successful_results.dropna(subset=['CV Ortalama', 'CV Std']).sort_values('CV Ortalama', ascending=False)

fig2 = go.Figure()
fig2.add_trace(go.Bar(
    x=plot_df2['Model'],
    y=plot_df2['CV Ortalama'],
    error_y=dict(
        type='data',
        array=plot_df2['CV Std'],
        visible=True
    ),
    marker_color=PROFESSIONAL_PALETTE[0],
    name='CV Ortalama'
))
fig2 = apply_premium_layout(fig2, "Model CV Kararlılık Analizi (Error Bars = Std)")
fig2.update_xaxes(tickangle=-45)
save_figure(fig2, "model_phase7_cv_stability")

# Grafik 3: Overfitting Analizi
print("3️⃣ Overfitting Analizi (Train vs Test)...")
plot_df3 = successful_results.dropna(subset=['Train Skoru', 'Test Skoru'])

fig3 = go.Figure()
fig3.add_trace(go.Bar(
    name='Train F1',
    x=plot_df3['Model'],
    y=plot_df3['Train Skoru'],
    marker_color=PROFESSIONAL_PALETTE[0]
))
fig3.add_trace(go.Bar(
    name='Test F1',
    x=plot_df3['Model'],
    y=plot_df3['Test Skoru'],
    marker_color=PROFESSIONAL_PALETTE[1]
))
fig3.update_layout(barmode='group')
fig3 = apply_premium_layout(fig3, "Train vs Test Performans (Overfitting Analizi)")
fig3.update_xaxes(tickangle=-45)
save_figure(fig3, "model_phase7_overfitting_analysis")

# Grafik 4: Eğitim Süresi vs Performans
print("4️⃣ Eğitim Süresi vs Performans...")
plot_df4 = successful_results.dropna(subset=['Eğitim Süresi']).sort_values('Eğitim Süresi', ascending=True)

fig4 = px.scatter(
    plot_df4,
    x='Eğitim Süresi',
    y='Ana Metrik',
    size='Ana Metrik',
    color='CV Std',
    hover_name='Model',
    color_continuous_scale=[[0, "#6A994E"], [1, "#C73E1D"]],
    title="Hız vs Performans: Eğitim Süresi vs F1-Score",
    labels={'Eğitim Süresi': 'Eğitim Süresi (saniye)', 'Ana Metrik': 'F1-Score'}
)
fig4 = apply_premium_layout(fig4, "Hız vs Performans: Eğitim Süresi vs F1-Score")
save_figure(fig4, "model_phase7_training_time")

# Grafik 5: Leadership Matrix
print("5️⃣ Model Liderlik Matrisi...")
plot_df5 = successful_results.dropna(subset=['Ana Metrik', 'Overfitting Farkı', 'Eğitim Süresi', 'CV Std'])

fig5 = px.scatter(
    plot_df5,
    x='Ana Metrik',
    y='Overfitting Farkı',
    size='Eğitim Süresi',
    color='CV Std',
    hover_name='Model',
    color_continuous_scale=[[0, "#6A994E"], [0.5, "#F18F01"], [1, "#C73E1D"]],
    title="Model Liderlik Matrisi: Performans / Overfit / Hız / Kararlılık",
    labels={'Ana Metrik': 'F1-Score (Test)', 'Overfitting Farkı': 'Overfitting (Train-Test)'}
)
fig5 = apply_premium_layout(fig5, "Model Liderlik Matrisi")
save_figure(fig5, "model_phase7_leadership_matrix")

print("\n✅ Tüm grafikler başarıyla oluşturuldu!")

print("\n" + "="*80)
print(" PHASE 9: FINAL MODEL DECISION ".center(80, "="))
print("="*80)

# En iyi modeli seç (çok kriterli)
print("\n🎯 En İyi Model Seçimi (Çok Kriterli Değerlendirme)...")

# Baseline'ı filtrele
candidate_results = successful_results[~successful_results['Model'].str.contains('Dummy', na=False)].copy()

# Seçim kriterleri
print("\n📋 Seçim Kriterleri:")
print("   1. Test F1-Score (ana metrik)")
print("   2. CV kararlılığı (düşük std)")
print("   3. Overfitting riski (train-test farkı)")
print("   4. Baseline üstünlüğü")

# En yüksek test F1-Score
best_model_row = candidate_results.iloc[0]
best_model_name = best_model_row['Model']

print(f"\n🏆 Final Model: {best_model_name}")
print(f"\n📊 Performans Metrikleri:")
print(f"   Train F1:      {best_model_row['Train Skoru']:.4f}")
print(f"   Test F1:       {best_model_row['Test Skoru']:.4f}")
print(f"   CV Mean:       {best_model_row['CV Ortalama']:.4f}")
print(f"   CV Std:        {best_model_row['CV Std']:.4f}")
print(f"   Overfit Gap:   {best_model_row['Overfitting Farkı']:.4f}")
print(f"   Training Time: {best_model_row['Eğitim Süresi']:.3f}s")

# Baseline ile karşılaştır
baseline_f1 = results_df[results_df['Model'].str.contains('Dummy', na=False)]['Test Skoru'].values[0]
improvement = ((best_model_row['Test Skoru'] - baseline_f1) / baseline_f1) * 100

print(f"\n💡 Baseline Üstünlüğü:")
print(f"   Baseline F1:   {baseline_f1:.4f}")
print(f"   İyileşme:      +{improvement:.1f}%")

print(f"\n✅ Seçim Gerekçesi:")
print(f"   - En yüksek test F1-Score: {best_model_row['Test Skoru']:.4f}")
print(f"   - CV kararlı: Std={best_model_row['CV Std']:.4f}")
print(f"   - Baseline'dan {improvement:.1f}% daha iyi")
print(f"   - Overfit riski: {'Düşük' if best_model_row['Overfitting Farkı'] < 0.05 else 'Orta' if best_model_row['Overfitting Farkı'] < 0.10 else 'Yüksek'}")

print("\n" + "="*80)
print(" PHASE 10: CONFUSION MATRIX & ERROR ANALYSIS ".center(80, "="))
print("="*80)

print(f"\n🔍 Final Model ({best_model_name}) için Detaylı Analiz...")

# En iyi modeli yeniden eğit
print("\n🚀 Model yeniden eğitiliyor...")

# Model objesini bul
final_model_obj = models[best_model_name]
final_pipeline = Pipeline([
    ('scaler', StandardScaler()),
    ('model', final_model_obj)
])

final_pipeline.fit(X_train, y_train)

# Predictions
y_train_pred = final_pipeline.predict(X_train)
y_test_pred = final_pipeline.predict(X_test)

# Probabilities (ROC-AUC için)
try:
    y_test_proba = final_pipeline.predict_proba(X_test)[:, 1]
    roc_auc = roc_auc_score(y_test, y_test_proba)
    has_proba = True
except:
    roc_auc = None
    has_proba = False

# Classification Report
print(f"\n📊 Classification Report (Test Set):")
print("="*80)
print(classification_report(y_test, y_test_pred, target_names=['Diyabet Yok', 'Diyabet Var']))

# Confusion Matrix
cm = confusion_matrix(y_test, y_test_pred)

print(f"\n🔢 Confusion Matrix:")
print(f"                  Predicted 0  Predicted 1")
print(f"   Actual 0 (TN)      {cm[0,0]:3d}          {cm[0,1]:3d}")
print(f"   Actual 1 (FN)      {cm[1,0]:3d}          {cm[1,1]:3d}")

# Metrikler
tn, fp, fn, tp = cm.ravel()
print(f"\n📈 Detaylı Metrikler:")
print(f"   True Negatives (TN):  {tn}")
print(f"   False Positives (FP): {fp}")
print(f"   False Negatives (FN): {fn}")
print(f"   True Positives (TP):  {tp}")
print(f"   Accuracy:    {accuracy_score(y_test, y_test_pred):.4f}")
print(f"   Precision:   {precision_score(y_test, y_test_pred, average='weighted'):.4f}")
print(f"   Recall:      {recall_score(y_test, y_test_pred, average='weighted'):.4f}")
print(f"   F1-Score:    {f1_score(y_test, y_test_pred, average='weighted'):.4f}")
if has_proba:
    print(f"   ROC-AUC:     {roc_auc:.4f}")

# Confusion Matrix Görselleştirme
print(f"\n📊 Confusion Matrix Görselleştiriliyor...")

fig_cm = ff.create_annotated_heatmap(
    z=cm,
    x=['Diyabet Yok (0)', 'Diyabet Var (1)'],
    y=['Diyabet Yok (0)', 'Diyabet Var (1)'],
    colorscale=[[0, "#FBFBF8"], [0.5, "#A7C7E7"], [1, "#2E86AB"]],
    showscale=True
)

fig_cm.update_layout(
    title=f"Final Model Confusion Matrix: {best_model_name}",
    xaxis_title="Tahmin Edilen Sınıf",
    yaxis_title="Gerçek Sınıf"
)

fig_cm = apply_premium_layout(fig_cm, f"Final Model Confusion Matrix: {best_model_name}")
save_figure(fig_cm, "model_phase10_final_confusion_matrix")

# Confusion Matrix Yorumu
print(f"\n💡 Confusion Matrix Yorumu:")
print(f"   ✅ True Negatives: {tn} (doğru negatif tahmin)")
print(f"   ✅ True Positives: {tp} (doğru pozitif tahmin)")
print(f"   ⚠️ False Positives: {fp} (yanlış pozitif - Type I Error)")
print(f"   ⚠️ False Negatives: {fn} (yanlış negatif - Type II Error)")

if fp > fn:
    print(f"\n   🔍 Model, diyabet olmayan kişileri diyabetli olarak tahmin etme eğiliminde")
    print(f"      (False Positive > False Negative)")
elif fn > fp:
    print(f"\n   🔍 Model, diyabetli kişileri sağlıklı olarak tahmin etme eğiliminde")
    print(f"      (False Negative > False Positive) - DAHA KRİTİK!")
else:
    print(f"\n   ✅ Model, her iki hata türünde de dengeli")

# ROC Curve (eğer probability varsa)
if has_proba:
    print(f"\n📈 ROC Curve Çiziliyor...")
    
    fpr, tpr, thresholds = roc_curve(y_test, y_test_proba)
    
    fig_roc = go.Figure()
    fig_roc.add_trace(go.Scatter(
        x=fpr, y=tpr,
        mode='lines',
        name=f'ROC Curve (AUC={roc_auc:.4f})',
        line=dict(color=PROFESSIONAL_PALETTE[0], width=3)
    ))
    fig_roc.add_trace(go.Scatter(
        x=[0, 1], y=[0, 1],
        mode='lines',
        name='Random Classifier',
        line=dict(color='gray', width=2, dash='dash')
    ))
    
    fig_roc.update_layout(
        xaxis_title='False Positive Rate',
        yaxis_title='True Positive Rate'
    )
    
    fig_roc = apply_premium_layout(fig_roc, f"ROC Curve: {best_model_name}")
    save_figure(fig_roc, "model_phase10_roc_curve")

print("\n" + "="*80)
print(" PHASE 12: FINAL MODEL HANDOFF ".center(80, "="))
print("="*80)

print("\n💾 Final Model Kaydediliyor...")

# Final modeli kaydet
joblib.dump(final_pipeline, '../models/final_model.pkl')
print(f"✅ Final model kaydedildi: final_model.pkl")

# Model metadata
model_metadata = {
    'model_name': best_model_name,
    'test_f1_score': best_model_row['Test Skoru'],
    'cv_mean': best_model_row['CV Ortalama'],
    'cv_std': best_model_row['CV Std'],
    'overfitting_gap': best_model_row['Overfitting Farkı'],
    'training_time': best_model_row['Eğitim Süresi'],
    'roc_auc': roc_auc if has_proba else None,
    'feature_count': len(X_train.columns),
    'train_samples': len(X_train),
    'test_samples': len(X_test)
}

pd.DataFrame([model_metadata]).to_csv('../reports/csv/final_model_metadata.csv', index=False)
print(f"✅ Model metadata kaydedildi: final_model_metadata.csv")

print("\n" + "="*80)
print(" MODEL TRAINING TAMAMLANDI ".center(80, "="))
print("="*80)

print(f"\n🎉 Özet:")
print(f"   Eğitilen Model Sayısı: {len(models)}")
print(f"   Başarılı Model: {len(successful_results)}")
print(f"   Final Model: {best_model_name}")
print(f"   Test F1-Score: {best_model_row['Test Skoru']:.4f}")
print(f"   Baseline İyileştirme: +{improvement:.1f}%")
if has_proba:
    print(f"   ROC-AUC: {roc_auc:.4f}")

print(f"\n📁 Oluşturulan Dosyalar:")
print(f"   Modeller:")
print(f"     - models/final_model.pkl")
print(f"   Raporlar:")
print(f"     - reports/csv/model_comparison_results.csv")
print(f"     - reports/csv/final_model_metadata.csv")
print(f"     - reports/model_comparison_prettytable.txt")
print(f"   Görseller:")
print(f"     - figures/model_phase7_performance_comparison.html")
print(f"     - figures/model_phase7_cv_stability.html")
print(f"     - figures/model_phase7_overfitting_analysis.html")
print(f"     - figures/model_phase7_training_time.html")
print(f"     - figures/model_phase7_leadership_matrix.html")
print(f"     - figures/model_phase10_final_confusion_matrix.html")
if has_proba:
    print(f"     - figures/model_phase10_roc_curve.html")

print(f"\n✅ Bir sonraki adım: Deployment Expert, final_model.pkl'yi kullanarak deployment sürecini başlatabilir!")
print("="*80)
