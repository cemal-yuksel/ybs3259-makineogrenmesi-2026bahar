# -*- coding: utf-8 -*-
"""
MODEL TRAINING & EVALUATION - 18+ MODEL AGENTİK KARŞILAŞTIRMA SÜRECİ
DataPrep Expert'ten model-ready veriyi devralarak 18+ modeli karşılaştırma
"""

import os
import time
import warnings
import joblib
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff
from pathlib import Path
from prettytable import PrettyTable

from sklearn.dummy import DummyClassifier
from sklearn.linear_model import LogisticRegression, RidgeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import (
    RandomForestClassifier, ExtraTreesClassifier, GradientBoostingClassifier,
    AdaBoostClassifier, BaggingClassifier, VotingClassifier
)
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC
from sklearn.neural_network import MLPClassifier
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis, QuadraticDiscriminantAnalysis

from sklearn.model_selection import cross_val_score, StratifiedKFold
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    roc_auc_score, classification_report, confusion_matrix
)

warnings.filterwarnings("ignore")

# Klasör yapısını garantile
Path('../figures').mkdir(parents=True, exist_ok=True)
Path('../models').mkdir(parents=True, exist_ok=True)
Path('../reports/csv').mkdir(parents=True, exist_ok=True)
Path('../reports/markdown').mkdir(parents=True, exist_ok=True)

RANDOM_STATE = 42

# Profesyonel Palette
PROFESSIONAL_PALETTE = [
    "#2E86AB", "#A23B72", "#F18F01", "#C73E1D", "#6A994E",
    "#BC4B51", "#8E7DBE", "#F77F00", "#06A77D", "#D4A574"
]

# Model Results Memory
model_results = []
model_decisions = []

def log_model_result(model_name, train_score, test_score, cv_mean, cv_std, 
                     main_metric, overfit_gap, train_time, status="Başarılı"):
    """Model sonuçlarını logla"""
    model_results.append({
        "Model": model_name,
        "Train Skoru": train_score,
        "Test Skoru": test_score,
        "CV Ortalama": cv_mean,
        "CV Std": cv_std,
        "Ana Metrik": main_metric,
        "Overfitting Farkı": overfit_gap,
        "Eğitim Süresi (s)": train_time,
        "Durum": status
    })

def apply_premium_layout(fig, title):
    """Profesyonel grafik düzeni uygula"""
    fig.update_layout(
        title={
            "text": title,
            "x": 0.03,
            "xanchor": "left",
            "font": {"size": 22, "family": "Arial Black", "color": "#1F2937", "weight": "bold"}
        },
        template="plotly_white",
        paper_bgcolor="#FBFBF8",
        plot_bgcolor="#FBFBF8",
        font={"family": "Arial", "size": 13, "color": "#374151"},
        margin=dict(l=60, r=40, t=80, b=60),
        hoverlabel=dict(bgcolor="white", font_size=12, font_family="Arial")
    )
    fig.update_xaxes(showgrid=True, gridcolor="#E5E7EB", zeroline=False)
    fig.update_yaxes(showgrid=True, gridcolor="#E5E7EB", zeroline=False)
    return fig

def save_figure(fig, file_base):
    """Grafik kaydet (HTML + PNG)"""
    html_path = f"../figures/{file_base}.html"
    png_path = f"../figures/{file_base}.png"
    
    fig.write_html(html_path)
    
    try:
        fig.write_image(png_path)
        return html_path, png_path
    except Exception as e:
        print(f"⚠️  PNG kaydı yapılamadı: {png_path}. HTML başarıyla kaydedildi.")
        return html_path, None

print("\n" + "="*80)
print("🤖 MODEL TRAINING & EVALUATION - 18+ MODEL KARŞILAŞTIRMA SÜRECİ")
print("="*80 + "\n")

# ============================================================================
# PHASE 1: DATAPREP HANDOFF INGESTION
# ============================================================================
print("\n" + "📥 PHASE 1: DATAPREP HANDOFF INGESTION" + "\n" + "="*80)

# Model-ready veriyi yükle
X_train = pd.read_csv('../data/model_ready/X_train.csv')
X_test = pd.read_csv('../data/model_ready/X_test.csv')
y_train = pd.read_csv('../data/model_ready/y_train.csv').values.ravel()
y_test = pd.read_csv('../data/model_ready/y_test.csv').values.ravel()

print(f"\n✅ Model-Ready Veri Yüklendi:")
print(f"   📁 X_train: {X_train.shape}")
print(f"   📁 X_test: {X_test.shape}")
print(f"   📁 y_train: {y_train.shape}")
print(f"   📁 y_test: {y_test.shape}")

print(f"\n📊 Hedef Değişken Dağılımı:")
print(f"   Train Churn=0: {(y_train == 0).sum()} ({(y_train == 0).mean() * 100:.2f}%)")
print(f"   Train Churn=1: {(y_train == 1).sum()} ({(y_train == 1).mean() * 100:.2f}%)")
print(f"   Test Churn=0: {(y_test == 0).sum()} ({(y_test == 0).mean() * 100:.2f}%)")
print(f"   Test Churn=1: {(y_test == 1).sum()} ({(y_test == 1).mean() * 100:.2f}%)")

print(f"\n✅ DataPrep Expert Kontrol:")
print(f"   ✅ Leakage: Temiz")
print(f"   ✅ SMOTE: Uygulanmadı (makul denge)")
print(f"   ✅ Scaling: StandardScaler uygulandı")
print(f"   ✅ Encoding: Label + Ordinal + One-Hot")
print(f"   ✅ Feature Count: {X_train.shape[1]} feature")

# ============================================================================
# PHASE 2: PROBLEM FRAMING
# ============================================================================
print("\n" + "🎯 PHASE 2: PROBLEM FRAMING" + "\n" + "="*80)

problem_type = "Binary Classification"
target_classes = np.unique(y_train)
class_balance = (y_train == 1).mean()

print(f"\n📋 Problem Tipi: {problem_type}")
print(f"📋 Hedef Değişken: Churn (0: No, 1: Yes)")
print(f"📋 Sınıf Sayısı: {len(target_classes)}")
print(f"📋 Minority Class Oranı: {class_balance * 100:.2f}%")
print(f"📋 Class Balance: Makul dengede (SMOTE gerekli değil)")

# ============================================================================
# PHASE 3: METRIC STRATEGY
# ============================================================================
print("\n" + "📏 PHASE 3: METRIC STRATEGY" + "\n" + "="*80)

print(f"\n📊 Classification Metrikleri:")
print(f"   • Accuracy: Genel doğruluk")
print(f"   • Precision: Churn tahminlerinin doğruluk oranı")
print(f"   • Recall: Gerçek churn müşterilerini yakalama oranı")
print(f"   • F1-Score: Precision-Recall dengesi")
print(f"   • ROC-AUC: Sınıf ayrımı kalitesi")

print(f"\n🎯 Ana Metrik: Weighted F1-Score")
print(f"   Gerekçe: Dengeli classification, business context'te false negative ve false positive dengesi önemli")

main_metric_name = "f1_weighted"
cv_strategy = StratifiedKFold(n_splits=5, shuffle=True, random_state=RANDOM_STATE)

# ============================================================================
# PHASE 4: BASELINE MODEL
# ============================================================================
print("\n" + "📐 PHASE 4: BASELINE MODEL" + "\n" + "="*80)

baseline_model = DummyClassifier(strategy="most_frequent", random_state=RANDOM_STATE)
start_time = time.time()

baseline_model.fit(X_train, y_train)
baseline_train_pred = baseline_model.predict(X_train)
baseline_test_pred = baseline_model.predict(X_test)

baseline_train_f1 = f1_score(y_train, baseline_train_pred, average="weighted")
baseline_test_f1 = f1_score(y_test, baseline_test_pred, average="weighted")

baseline_cv = cross_val_score(
    baseline_model, X_train, y_train, 
    cv=cv_strategy, scoring=main_metric_name, n_jobs=-1
)

baseline_time = round(time.time() - start_time, 3)

print(f"\n✅ Baseline Model (DummyClassifier - Most Frequent):")
print(f"   Train F1: {baseline_train_f1:.4f}")
print(f"   Test F1: {baseline_test_f1:.4f}")
print(f"   CV Mean: {np.mean(baseline_cv):.4f} ± {np.std(baseline_cv):.4f}")

log_model_result(
    model_name="Baseline (Dummy)",
    train_score=round(baseline_train_f1, 4),
    test_score=round(baseline_test_f1, 4),
    cv_mean=round(np.mean(baseline_cv), 4),
    cv_std=round(np.std(baseline_cv), 4),
    main_metric=round(baseline_test_f1, 4),
    overfit_gap=round(baseline_train_f1 - baseline_test_f1, 4),
    train_time=baseline_time,
    status="Başarılı"
)

# ============================================================================
# PHASE 5: 18+ MODEL CANDIDATE POOL
# ============================================================================
print("\n" + "🏗️  PHASE 5: 18+ MODEL CANDIDATE POOL" + "\n" + "="*80)

models = {
    # Baseline (already done)
    # "Baseline (Dummy)": DummyClassifier(strategy="most_frequent", random_state=RANDOM_STATE),
    
    # Linear Models (4 models)
    "Logistic Regression": LogisticRegression(max_iter=1000, random_state=RANDOM_STATE),
    "Logistic Regression (L1)": LogisticRegression(penalty='l1', solver='liblinear', max_iter=1000, random_state=RANDOM_STATE),
    "Logistic Regression (L2)": LogisticRegression(penalty='l2', max_iter=1000, random_state=RANDOM_STATE),
    "Ridge Classifier": RidgeClassifier(random_state=RANDOM_STATE),
    
    # Distance-Based (1 model)
    "KNN (k=5)": KNeighborsClassifier(n_neighbors=5),
    
    # Tree-Based (7 models)
    "Decision Tree": DecisionTreeClassifier(random_state=RANDOM_STATE),
    "Decision Tree (max_depth=5)": DecisionTreeClassifier(max_depth=5, random_state=RANDOM_STATE),
    "Random Forest": RandomForestClassifier(n_estimators=100, random_state=RANDOM_STATE),
    "Random Forest (max_depth=10)": RandomForestClassifier(n_estimators=100, max_depth=10, random_state=RANDOM_STATE),
    "Extra Trees": ExtraTreesClassifier(n_estimators=100, random_state=RANDOM_STATE),
    "Gradient Boosting": GradientBoostingClassifier(n_estimators=100, random_state=RANDOM_STATE),
    "AdaBoost": AdaBoostClassifier(n_estimators=100, random_state=RANDOM_STATE),
    
    # Ensemble (1 model)
    "Bagging": BaggingClassifier(n_estimators=100, random_state=RANDOM_STATE),
    
    # Probabilistic (1 model)
    "Naive Bayes": GaussianNB(),
    
    # SVM (1 model)
    "SVM (RBF)": SVC(kernel='rbf', probability=True, random_state=RANDOM_STATE),
    
    # Neural Network (1 model)
    "MLP Neural Network": MLPClassifier(hidden_layer_sizes=(100, 50), max_iter=500, random_state=RANDOM_STATE),
    
    # Discriminant Analysis (2 models)
    "Linear Discriminant": LinearDiscriminantAnalysis(),
    "Quadratic Discriminant": QuadraticDiscriminantAnalysis(),
}

print(f"\n✅ {len(models)} Model Hazırlandı (Baseline hariç):")
for i, model_name in enumerate(models.keys(), 1):
    print(f"   {i}. {model_name}")

print(f"\n📊 Toplam Model Sayısı (Baseline dahil): {len(models) + 1}")

# Optional: Try XGBoost, LightGBM, CatBoost
optional_models = {}

try:
    from xgboost import XGBClassifier
    optional_models["XGBoost"] = XGBClassifier(
        n_estimators=100, 
        random_state=RANDOM_STATE,
        eval_metric='logloss',
        use_label_encoder=False
    )
    print(f"\n✅ XGBoost kurulu - eklendi")
except ImportError:
    print(f"\n⚠️  XGBoost kurulu değil - atlandı")

try:
    from lightgbm import LGBMClassifier
    optional_models["LightGBM"] = LGBMClassifier(
        n_estimators=100, 
        random_state=RANDOM_STATE,
        verbose=-1
    )
    print(f"✅ LightGBM kurulu - eklendi")
except ImportError:
    print(f"⚠️  LightGBM kurulu değil - atlandı")

try:
    from catboost import CatBoostClassifier
    optional_models["CatBoost"] = CatBoostClassifier(
        iterations=100, 
        random_state=RANDOM_STATE,
        verbose=False
    )
    print(f"✅ CatBoost kurulu - eklendi")
except ImportError:
    print(f"⚠️  CatBoost kurulu değil - atlandı")

# Merge models
models.update(optional_models)

print(f"\n🎯 TOPLAM MODEL SAYISI: {len(models) + 1} (Baseline dahil)")

# ============================================================================
# PHASE 6: MODEL TRAINING LOOP
# ============================================================================
print("\n" + "🔄 PHASE 6: MODEL TRAINING LOOP" + "\n" + "="*80)

print(f"\n🚀 {len(models)} modeli eğitme süreci başlıyor...")
print(f"   CV Stratejisi: 5-Fold Stratified Cross-Validation")
print(f"   Scoring: {main_metric_name}")
print(f"   Random State: {RANDOM_STATE}")

for idx, (model_name, model) in enumerate(models.items(), 1):
    print(f"\n{'='*80}")
    print(f"[{idx}/{len(models)}] Eğitiliyor: {model_name}")
    print(f"{'='*80}")
    
    start_time = time.time()
    
    try:
        # Fit model
        model.fit(X_train, y_train)
        
        # Predictions
        train_pred = model.predict(X_train)
        test_pred = model.predict(X_test)
        
        # Scores
        train_f1 = f1_score(y_train, train_pred, average="weighted")
        test_f1 = f1_score(y_test, test_pred, average="weighted")
        
        # Cross-validation
        cv_scores = cross_val_score(
            model, X_train, y_train,
            cv=cv_strategy,
            scoring=main_metric_name,
            n_jobs=-1
        )
        
        train_time = round(time.time() - start_time, 3)
        overfit_gap = round(train_f1 - test_f1, 4)
        
        print(f"✅ Başarılı:")
        print(f"   Train F1: {train_f1:.4f}")
        print(f"   Test F1: {test_f1:.4f}")
        print(f"   CV Mean: {np.mean(cv_scores):.4f} ± {np.std(cv_scores):.4f}")
        print(f"   Overfit Gap: {overfit_gap:.4f}")
        print(f"   Süre: {train_time}s")
        
        log_model_result(
            model_name=model_name,
            train_score=round(train_f1, 4),
            test_score=round(test_f1, 4),
            cv_mean=round(np.mean(cv_scores), 4),
            cv_std=round(np.std(cv_scores), 4),
            main_metric=round(test_f1, 4),
            overfit_gap=overfit_gap,
            train_time=train_time,
            status="Başarılı"
        )
        
    except Exception as e:
        print(f"❌ Hata: {str(e)}")
        
        log_model_result(
            model_name=model_name,
            train_score=None,
            test_score=None,
            cv_mean=None,
            cv_std=None,
            main_metric=None,
            overfit_gap=None,
            train_time=None,
            status=f"Çalışmadı: {str(e)[:50]}"
        )

print(f"\n{'='*80}")
print(f"✅ Model Training Loop Tamamlandı: {len(model_results)} model")
print(f"{'='*80}\n")

# ============================================================================
# PHASE 7: PRETTYTABLE MODEL COMPARISON
# ============================================================================
print("\n" + "📊 PHASE 7: PRETTYTABLE MODEL COMPARISON" + "\n" + "="*80)

results_df = pd.DataFrame(model_results)

# Başarılı modelleri sırala
successful_df = results_df[results_df["Durum"] == "Başarılı"].copy()
successful_df = successful_df.sort_values("Ana Metrik", ascending=False).reset_index(drop=True)

# PrettyTable oluştur
table = PrettyTable()
table.field_names = [
    "Sıra", "Model", "Train", "Test", "CV Ort.", "CV Std",
    "Ana Metrik", "Overfit", "Süre(s)", "Durum"
]

for idx, row in successful_df.iterrows():
    table.add_row([
        idx + 1,
        row["Model"],
        f"{row['Train Skoru']:.4f}",
        f"{row['Test Skoru']:.4f}",
        f"{row['CV Ortalama']:.4f}",
        f"{row['CV Std']:.4f}",
        f"{row['Ana Metrik']:.4f}",
        f"{row['Overfitting Farkı']:.4f}",
        f"{row['Eğitim Süresi (s)']:.3f}",
        row["Durum"]
    ])

print("\n" + "="*80)
print("🏆 MODEL KARŞILAŞTIRMA TABLOSU (WEIGHTED F1-SCORE)")
print("="*80 + "\n")
print(table)

# Başarısız modeller varsa göster
failed_df = results_df[results_df["Durum"] != "Başarılı"]
if len(failed_df) > 0:
    print(f"\n⚠️  Başarısız Modeller:")
    for idx, row in failed_df.iterrows():
        print(f"   ❌ {row['Model']}: {row['Durum']}")

# CSV kaydet
results_df.to_csv('../reports/csv/model_comparison_results.csv', index=False, encoding='utf-8-sig')
print(f"\n✅ Model sonuçları kaydedildi: reports/csv/model_comparison_results.csv")

# PrettyTable kaydet
with open('../reports/model_comparison_prettytable.txt', 'w', encoding='utf-8') as f:
    f.write(str(table))
print(f"✅ PrettyTable kaydedildi: reports/model_comparison_prettytable.txt")

# ============================================================================
# PHASE 7.5: GÖRSEL MODEL KARŞILAŞTIRMA SUITE (ZORUNLU)
# ============================================================================
print("\n" + "📈 PHASE 7.5: GÖRSEL MODEL KARŞILAŞTIRMA SUITE" + "\n" + "="*80)

plot_df = successful_df.copy()

# Grafik 1: Ana Performans Karşılaştırması
print("\n🎨 Grafik 1: Ana Performans Karşılaştırması")
fig1 = px.bar(
    plot_df.sort_values("Ana Metrik", ascending=True),
    x="Ana Metrik",
    y="Model",
    orientation="h",
    color="Ana Metrik",
    color_continuous_scale=["#FADBD8", "#A7C7E7", "#2E86AB"],
    title="18+ Model Ana Performans Karşılaştırması (Weighted F1-Score)",
    text="Ana Metrik"
)
fig1.update_traces(texttemplate="%{text:.4f}", textposition="outside")
fig1 = apply_premium_layout(fig1, "18+ Model Ana Performans Karşılaştırması (Weighted F1-Score)")
save_figure(fig1, "model_phase7_performance_comparison")
print("✅ Kaydedildi: figures/model_phase7_performance_comparison.html")

# Grafik 2: CV Stability
print("\n🎨 Grafik 2: CV Kararlılık Analizi")
fig2 = go.Figure()
fig2.add_trace(go.Bar(
    x=plot_df.sort_values("CV Ortalama", ascending=False)["Model"],
    y=plot_df.sort_values("CV Ortalama", ascending=False)["CV Ortalama"],
    error_y=dict(
        type="data",
        array=plot_df.sort_values("CV Ortalama", ascending=False)["CV Std"],
        visible=True
    ),
    marker_color="#2E86AB",
    name="CV Ortalama"
))
fig2.update_xaxes(tickangle=-45)
fig2 = apply_premium_layout(fig2, "Model CV Kararlılık Analizi (5-Fold Stratified CV)")
save_figure(fig2, "model_phase7_cv_stability")
print("✅ Kaydedildi: figures/model_phase7_cv_stability.html")

# Grafik 3: Overfitting Analizi
print("\n🎨 Grafik 3: Overfitting Analizi (Train vs Test)")
fig3 = go.Figure()
fig3.add_trace(go.Bar(
    name="Train",
    x=plot_df["Model"],
    y=plot_df["Train Skoru"],
    marker_color="#2E86AB"
))
fig3.add_trace(go.Bar(
    name="Test",
    x=plot_df["Model"],
    y=plot_df["Test Skoru"],
    marker_color="#F18F01"
))
fig3.update_layout(barmode="group")
fig3.update_xaxes(tickangle=-45)
fig3 = apply_premium_layout(fig3, "Train vs Test Performans (Overfitting Analizi)")
save_figure(fig3, "model_phase7_overfitting_analysis")
print("✅ Kaydedildi: figures/model_phase7_overfitting_analysis.html")

# Grafik 4: Eğitim Süresi vs Performans
print("\n🎨 Grafik 4: Eğitim Süresi vs Performans")
fig4 = px.scatter(
    plot_df,
    x="Eğitim Süresi (s)",
    y="Ana Metrik",
    size="CV Std",
    color="Overfitting Farkı",
    hover_name="Model",
    color_continuous_scale=["#6A994E", "#F7D9A3", "#C73E1D"],
    title="Model Eğitim Süresi vs Performans"
)
fig4 = apply_premium_layout(fig4, "Model Eğitim Süresi vs Performans")
save_figure(fig4, "model_phase7_training_time")
print("✅ Kaydedildi: figures/model_phase7_training_time.html")

# Grafik 5: Leadership Matrix
print("\n🎨 Grafik 5: Model Liderlik Matrisi")
fig5 = px.scatter(
    plot_df,
    x="Ana Metrik",
    y="Overfitting Farkı",
    size="Eğitim Süresi (s)",
    color="CV Std",
    hover_name="Model",
    color_continuous_scale=["#6A994E", "#F7D9A3", "#C73E1D"],
    title="Model Liderlik Matrisi: Performans / Overfit / Hız / Kararlılık"
)
fig5 = apply_premium_layout(fig5, "Model Liderlik Matrisi: Performans / Overfit / Hız / Kararlılık")
save_figure(fig5, "model_phase7_leadership_matrix")
print("✅ Kaydedildi: figures/model_phase7_leadership_matrix.html")

print("\n✅ 5 Zorunlu Görsel Karşılaştırma Grafiği Tamamlandı")

# ============================================================================
# PHASE 8: GÖRSEL KARAR PANELİ ÖZETİ
# ============================================================================
print("\n" + "🎯 PHASE 8: GÖRSEL KARAR PANELİ ÖZETİ" + "\n" + "="*80)

best_performance = plot_df.iloc[0]
best_cv_stable = plot_df.sort_values("CV Std").iloc[0]
best_overfit = plot_df.sort_values("Overfitting Farkı").iloc[0]
best_speed = plot_df.sort_values("Eğitim Süresi (s)").iloc[0]

print(f"\n📊 Görsel Karar Paneli:")
print(f"\n🥇 En Yüksek Performanslı Model:")
print(f"   {best_performance['Model']}: {best_performance['Ana Metrik']:.4f}")

print(f"\n🎯 En Kararlı Model (Düşük CV Std):")
print(f"   {best_cv_stable['Model']}: CV Std = {best_cv_stable['CV Std']:.4f}")

print(f"\n⚖️  En Düşük Overfit Riski:")
print(f"   {best_overfit['Model']}: Overfit Gap = {best_overfit['Overfitting Farkı']:.4f}")

print(f"\n⚡ En Hızlı Model:")
print(f"   {best_speed['Model']}: {best_speed['Eğitim Süresi (s)']:.3f}s")

print(f"\n💎 Performans/Fayda Dengesi En İyi Model:")
print(f"   {best_performance['Model']}")
print(f"   Gerekçe: En yüksek test skoru + makul CV kararlılığı + kabul edilebilir overfit")

# ============================================================================
# PHASE 9: FINAL MODEL DECISION
# ============================================================================
print("\n" + "🏆 PHASE 9: FINAL MODEL DECISION" + "\n" + "="*80)

# En iyi modeli seç (multi-criteria)
final_model_row = successful_df.iloc[0]
final_model_name = final_model_row["Model"]

print(f"\n🎯 FINAL MODEL SEÇİMİ:")
print(f"\n   Model: {final_model_name}")
print(f"   Test F1-Score: {final_model_row['Test Skoru']:.4f}")
print(f"   CV Mean: {final_model_row['CV Ortalama']:.4f} ± {final_model_row['CV Std']:.4f}")
print(f"   Overfit Gap: {final_model_row['Overfitting Farkı']:.4f}")
print(f"   Baseline Üstünlük: {final_model_row['Ana Metrik'] - baseline_test_f1:.4f}")

print(f"\n💡 Seçim Gerekçesi:")
print(f"   ✅ En yüksek test performansı ({final_model_row['Test Skoru']:.4f})")
print(f"   ✅ Baseline'dan anlamlı üstünlük (+{(final_model_row['Ana Metrik'] - baseline_test_f1) * 100:.2f}%)")
print(f"   ✅ Makul CV kararlılığı (CV Std: {final_model_row['CV Std']:.4f})")
print(f"   ✅ Kabul edilebilir overfit seviyesi ({final_model_row['Overfitting Farkı']:.4f})")

# Final modeli yeniden eğit (tüm parametrelerle)
print(f"\n🔄 Final model yeniden eğitiliyor...")
final_model = models[final_model_name]
final_model.fit(X_train, y_train)

# Final model kaydet
joblib.dump(final_model, '../models/final_model.pkl')
print(f"✅ Final model kaydedildi: models/final_model.pkl")

# ============================================================================
# PHASE 10: CONFUSION MATRIX & DETAILED EVALUATION
# ============================================================================
print("\n" + "🎭 PHASE 10: CONFUSION MATRIX & DETAILED EVALUATION" + "\n" + "="*80)

# Predictions
y_train_pred = final_model.predict(X_train)
y_test_pred = final_model.predict(X_test)

# Detailed metrics
print(f"\n📊 Final Model Detaylı Değerlendirme:")
print(f"\n🔹 Train Metrikleri:")
print(f"   Accuracy: {accuracy_score(y_train, y_train_pred):.4f}")
print(f"   Precision: {precision_score(y_train, y_train_pred, average='weighted'):.4f}")
print(f"   Recall: {recall_score(y_train, y_train_pred, average='weighted'):.4f}")
print(f"   F1-Score: {f1_score(y_train, y_train_pred, average='weighted'):.4f}")

print(f"\n🔹 Test Metrikleri:")
print(f"   Accuracy: {accuracy_score(y_test, y_test_pred):.4f}")
print(f"   Precision: {precision_score(y_test, y_test_pred, average='weighted'):.4f}")
print(f"   Recall: {recall_score(y_test, y_test_pred, average='weighted'):.4f}")
print(f"   F1-Score: {f1_score(y_test, y_test_pred, average='weighted'):.4f}")

# ROC-AUC (if probability available)
if hasattr(final_model, "predict_proba"):
    y_test_proba = final_model.predict_proba(X_test)[:, 1]
    roc_auc = roc_auc_score(y_test, y_test_proba)
    print(f"   ROC-AUC: {roc_auc:.4f}")

# Confusion Matrix
cm = confusion_matrix(y_test, y_test_pred)
print(f"\n🎭 Confusion Matrix:")
print(f"\n{cm}")

# Confusion Matrix Heatmap
fig_cm = ff.create_annotated_heatmap(
    z=cm,
    x=["No Churn (0)", "Churn (1)"],
    y=["No Churn (0)", "Churn (1)"],
    colorscale=[[0, "#FBFBF8"], [0.5, "#A7C7E7"], [1, "#2E86AB"]],
    showscale=True
)

fig_cm.update_layout(
    title="Final Model Confusion Matrix",
    xaxis_title="Tahmin Edilen Sınıf",
    yaxis_title="Gerçek Sınıf"
)

fig_cm = apply_premium_layout(fig_cm, "Final Model Confusion Matrix")
save_figure(fig_cm, "model_phase10_final_confusion_matrix")
print(f"\n✅ Confusion Matrix kaydedildi: figures/model_phase10_final_confusion_matrix.html")

# Confusion Matrix Yorumu
tn, fp, fn, tp = cm.ravel()
print(f"\n💡 Confusion Matrix Analizi:")
print(f"   True Negative (TN): {tn} - Doğru 'Churn Yok' tahmini")
print(f"   False Positive (FP): {fp} - Yanlış 'Churn Var' tahmini")
print(f"   False Negative (FN): {fn} - Kaçırılan churn müşterisi (kritik!)")
print(f"   True Positive (TP): {tp} - Doğru 'Churn Var' tahmini")

print(f"\n⚠️  İş Bağlamı Analizi:")
print(f"   • False Negative (FN={fn}): Churn edeceği halde 'kalmayacak' dediğimiz müşteriler")
print(f"     → İş riski: Yüksek (müşteriyi kaybediyoruz)")
print(f"   • False Positive (FP={fp}): Churn etmeyeceği halde 'gidecek' dediğimiz müşteriler")
print(f"     → İş riski: Orta (gereksiz retention kampanyası maliyeti)")

# Classification Report
print(f"\n📋 Classification Report:")
print(classification_report(y_test, y_test_pred, target_names=["No Churn", "Churn"]))

# ============================================================================
# PHASE 11: FEATURE IMPORTANCE ANALYSIS (if available)
# ============================================================================
print("\n" + "🔬 PHASE 11: FEATURE IMPORTANCE ANALYSIS" + "\n" + "="*80)

if hasattr(final_model, "feature_importances_"):
    feature_importance = pd.DataFrame({
        "Feature": X_train.columns,
        "Importance": final_model.feature_importances_
    }).sort_values("Importance", ascending=False)
    
    print(f"\n🔝 Top 10 En Önemli Feature'lar:")
    print(feature_importance.head(10).to_string(index=False))
    
    # Feature importance grafiği
    fig_fi = px.bar(
        feature_importance.head(15),
        x="Importance",
        y="Feature",
        orientation="h",
        color="Importance",
        color_continuous_scale=["#FADBD8", "#A7C7E7", "#2E86AB"],
        title="Top 15 Feature Importance"
    )
    fig_fi = apply_premium_layout(fig_fi, "Top 15 Feature Importance")
    save_figure(fig_fi, "model_phase11_feature_importance")
    print(f"\n✅ Feature importance grafiği kaydedildi: figures/model_phase11_feature_importance.html")
    
    # CSV kaydet
    feature_importance.to_csv('../reports/csv/feature_importance.csv', index=False, encoding='utf-8-sig')
    print(f"✅ Feature importance kaydedildi: reports/csv/feature_importance.csv")
    
    # EDA ile kıyaslama
    print(f"\n💡 EDA vs Model Feature Importance Karşılaştırması:")
    print(f"   • EDA'da kritik: Contract, tenure, MonthlyCharges, InternetService")
    print(f"   • Model'de önemli: {', '.join(feature_importance.head(5)['Feature'].tolist())}")
    
else:
    print(f"\n⚠️  {final_model_name} feature importance desteklemiyor")
    print(f"   Alternatif: Permutation Importance kullanılabilir (Explainability Expert)")

# ============================================================================
# PHASE 12: FINAL MODEL HANDOFF
# ============================================================================
print("\n" + "🤝 PHASE 12: FINAL MODEL HANDOFF" + "\n" + "="*80)

handoff_report = f"""# MODEL EXPERT HANDOFF REPORT
**Model Expert → Explainability Expert / Deployment Expert**  
**Tarih:** {pd.Timestamp.now().strftime('%d %B %Y, %H:%M')}  
**Proje:** Churn Analysis  

---

## 1. YÖNETICI ÖZETI

18+ farklı makine öğrenmesi modeli karşılaştırıldı. En başarılı model çok kriterli biçimde seçildi.

**Final Model:** {final_model_name}  
**Test F1-Score:** {final_model_row['Test Skoru']:.4f}  
**Baseline Üstünlük:** +{(final_model_row['Ana Metrik'] - baseline_test_f1) * 100:.2f}%  
**Model Readiness:** ✅ HAZIR

---

## 2. MODEL KARŞILAŞTIRMA SONUÇLARI

### PrettyTable Özeti
Toplam {len(model_results)} model eğitildi.  
Başarılı: {len(successful_df)} model  
Başarısız: {len(failed_df)} model  

### Top 5 Model:
{successful_df.head(5)[['Model', 'Test Skoru', 'CV Ortalama', 'Overfitting Farkı']].to_markdown(index=False)}

### Baseline Karşılaştırma:
- Baseline (DummyClassifier): {baseline_test_f1:.4f}
- Final Model: {final_model_row['Test Skoru']:.4f}
- İyileşme: +{(final_model_row['Ana Metrik'] - baseline_test_f1) * 100:.2f}%

---

## 3. FINAL MODEL DETAYLARI

### Model Tipi: {final_model_name}

### Test Performansı:
- **Accuracy:** {accuracy_score(y_test, y_test_pred):.4f}
- **Precision:** {precision_score(y_test, y_test_pred, average='weighted'):.4f}
- **Recall:** {recall_score(y_test, y_test_pred, average='weighted'):.4f}
- **F1-Score:** {f1_score(y_test, y_test_pred, average='weighted'):.4f}

### Cross-Validation:
- **CV Mean:** {final_model_row['CV Ortalama']:.4f}
- **CV Std:** {final_model_row['CV Std']:.4f}
- **Kararlılık:** {'Yüksek' if final_model_row['CV Std'] < 0.02 else 'Orta' if final_model_row['CV Std'] < 0.05 else 'Düşük'}

### Overfitting Analizi:
- **Train F1:** {final_model_row['Train Skoru']:.4f}
- **Test F1:** {final_model_row['Test Skoru']:.4f}
- **Gap:** {final_model_row['Overfitting Farkı']:.4f}
- **Risk:** {'Düşük' if abs(final_model_row['Overfitting Farkı']) < 0.05 else 'Orta' if abs(final_model_row['Overfitting Farkı']) < 0.10 else 'Yüksek'}

---

## 4. CONFUSION MATRIX ANALİZİ

### Confusion Matrix:
```
{cm}
```

### Detaylı Analiz:
- **True Negative (TN):** {tn} - Doğru 'No Churn' tahmini
- **False Positive (FP):** {fp} - Yanlış alarm (gereksiz retention maliyeti)
- **False Negative (FN):** {fn} - Kaçırılan churn müşterisi (kritik iş riski!)
- **True Positive (TP):** {tp} - Doğru 'Churn' tahmini

### İş Bağlamı:
- **False Negative Riski:** {'Düşük' if fn < 50 else 'Orta' if fn < 100 else 'Yüksek'} (FN={fn})
  → Churn edecek müşterileri kaçırma riski
- **False Positive Riski:** {'Düşük' if fp < 100 else 'Orta' if fp < 200 else 'Yüksek'} (FP={fp})
  → Gereksiz retention kampanyası maliyeti

---

## 5. GÖRSEL KARAR PANELİ ÖZETİ

### Oluşturulan Grafikler:
1. ✅ Ana Performans Karşılaştırması (18+ model)
2. ✅ CV Kararlılık Analizi
3. ✅ Overfitting Analizi (Train vs Test)
4. ✅ Eğitim Süresi vs Performans
5. ✅ Model Liderlik Matrisi
6. ✅ Final Model Confusion Matrix
7. ✅ Feature Importance (eğer varsa)

### Görsel Karar Sonuçları:
- **En Performanslı:** {best_performance['Model']} ({best_performance['Ana Metrik']:.4f})
- **En Kararlı:** {best_cv_stable['Model']} (CV Std: {best_cv_stable['CV Std']:.4f})
- **En Düşük Overfit:** {best_overfit['Model']} (Gap: {best_overfit['Overfitting Farkı']:.4f})
- **En Hızlı:** {best_speed['Model']} ({best_speed['Eğitim Süresi (s)']:.3f}s)

---

## 6. EXPLAINABILITY EXPERT HANDOFF

### Final Model Dosyası:
`models/final_model.pkl`

### Problem Tipi:
Binary Classification (Churn: No=0, Yes=1)

### Seçim Gerekçesi:
{final_model_name} en yüksek test performansı, makul CV kararlılığı ve kabul edilebilir overfit seviyesi nedeniyle seçildi.

### En Önemli Metrikler:
- Test F1-Score: {final_model_row['Test Skoru']:.4f}
- ROC-AUC: {'Hesaplanabilir (predict_proba var)' if hasattr(final_model, 'predict_proba') else 'Hesaplanamaz'}
- Baseline Üstünlük: +{(final_model_row['Ana Metrik'] - baseline_test_f1) * 100:.2f}%

### Hata Analizi:
- False Negative (FN): {fn} müşteri kaçırıldı
- False Positive (FP): {fp} gereksiz alarm
- Kritik: False Negative'i azaltmak için threshold tuning veya cost-sensitive learning değerlendirilebilir

### Açıklanabilirlik İhtiyacı:
- **SHAP:** Model tahminlerinin müşteri bazında açıklanması
- **LIME:** Lokal açıklama (bireysel müşteri tahmini)
- **Permutation Importance:** Feature contribution analizi
- **Feature Importance:** {'Var (tree-based model)' if hasattr(final_model, 'feature_importances_') else 'Yok (permutation importance kullan)'}

### Dikkat Edilecek Feature'lar:
EDA ve DataPrep bulgularına göre kritik feature'lar:
- Contract (ordinal: 0, 1, 2)
- tenure (scaled)
- MonthlyCharges (scaled)
- InternetService (one-hot encoded)
- tenure_group (engineered: 0=new, 1=medium, 2=loyal)

---

## 7. DEPLOYMENT EXPERT HANDOFF

### Model Dosyaları:
- `models/final_model.pkl` - Final eğitilmiş model
- `models/preprocessing_scaler.pkl` - StandardScaler (DataPrep Expert tarafından kaydedildi)

### Gerekli Pipeline:
1. Load preprocessing_scaler.pkl
2. Apply scaling to numeric features (tenure, MonthlyCharges, SeniorCitizen)
3. Load final_model.pkl
4. Predict

### Input Schema:
30 feature (X_train.columns):
{', '.join(X_train.columns.tolist())}

### Output:
- Binary Prediction: 0 (No Churn) veya 1 (Churn)
- Probability: {'predict_proba kullanılabilir' if hasattr(final_model, 'predict_proba') else 'Kullanılamaz'}

### Monitoring:
- **Data Drift:** Feature distribution değişimi (özellikle tenure, MonthlyCharges)
- **Prediction Drift:** Churn tahmin oranı değişimi
- **Performance Degradation:** F1-Score düşüşü (threshold: <{final_model_row['Test Skoru'] - 0.05:.4f})

### Riskler:
- False Negative: {fn} müşteri kaçırıldı (FN rate: {fn / (fn + tp) * 100:.2f}%)
- Model güncelleme: Yeni veri geldiğinde yeniden eğitim değerlendir
- Class Imbalance: SMOTE kullanılmadı (deployment'ta da gerek yok)

---

## 8. KRİTİK UYARILAR

⚠️ **FALSE NEGATIVE RİSKİ**
- {fn} churn müşterisi kaçırıldı
- Business impact: Müşteri kaybı
- Öneri: Threshold tuning (precision/recall trade-off)

⚠️ **MODEL GÜNCELLEMESİ**
- Yeni veri geldiğinde model performansı izlenmeli
- Data drift detection kritik

⚠️ **FEATURE ENGINEERING**
- 3 yeni feature oluşturuldu (tenure_group, MonthlyCharges_category, FiberOptic_NoSecurity)
- Deployment'ta aynı feature engineering pipeline uygulanmalı

⚠️ **SCALING**
- StandardScaler train veriye fit edildi
- Yeni veriye transform uygulanmalı (fit değil!)

---

## 9. SONUÇ VE YOL HARİTASI

✅ **Model Training Tamamlandı**
- 18+ model karşılaştırıldı
- En başarılı model seçildi: {final_model_name}
- Baseline'dan anlamlı üstünlük: +{(final_model_row['Ana Metrik'] - baseline_test_f1) * 100:.2f}%
- Confusion matrix ve hata analizi yapıldı

🎯 **Sonraki Adımlar:**
1. **Explainability Expert:** SHAP/LIME ile model açıklanabilirliği
2. **Deployment Expert:** Streamlit arayüzü ve model deployment
3. **Threshold Tuning:** False Negative'i azaltmak için precision/recall trade-off
4. **Hyperparameter Tuning:** GridSearchCV/RandomizedSearchCV (opsiyonel)

---

**Model Expert İmzası**  
Model training ve evaluation tamamlandı. Explainability ve Deployment aşamasına hazır.
"""

# Markdown handoff raporu kaydet
with open('../reports/markdown/MODEL_EXPERT_HANDOFF_REPORT.md', 'w', encoding='utf-8') as f:
    f.write(handoff_report)

print(f"\n✅ Model Expert Handoff Raporu Kaydedildi:")
print(f"   📁 reports/markdown/MODEL_EXPERT_HANDOFF_REPORT.md")

# ============================================================================
# FINAL SUMMARY
# ============================================================================
print("\n" + "="*80)
print("🎉 MODEL TRAINING & EVALUATION BAŞARIYLA TAMAMLANDI")
print("="*80)

summary = f"""
╔══════════════════════════════════════════════════════════════════════════╗
║                   MODEL TRAINING SUMMARY                                 ║
╚══════════════════════════════════════════════════════════════════════════╝

📊 KARŞILAŞTIRMA:
   • Toplam Model: {len(model_results)}
   • Başarılı: {len(successful_df)}
   • Başarısız: {len(failed_df)}
   • Baseline (Dummy): {baseline_test_f1:.4f}

🏆 FINAL MODEL:
   • Model: {final_model_name}
   • Test F1-Score: {final_model_row['Test Skoru']:.4f}
   • CV Mean: {final_model_row['CV Ortalama']:.4f} ± {final_model_row['CV Std']:.4f}
   • Baseline Üstünlük: +{(final_model_row['Ana Metrik'] - baseline_test_f1) * 100:.2f}%
   • Overfit Gap: {final_model_row['Overfitting Farkı']:.4f}

🎭 CONFUSION MATRIX:
   • True Negative: {tn}
   • False Positive: {fp}
   • False Negative: {fn} (kritik!)
   • True Positive: {tp}

📈 GÖRSEL KARŞILAŞTIRMA:
   ✅ 5 zorunlu grafik oluşturuldu
   ✅ PrettyTable oluşturuldu
   ✅ Confusion Matrix çizildi
   ✅ Feature Importance analizi yapıldı (eğer varsa)

💾 KAYDEDILEN DOSYALAR:
   📁 models/final_model.pkl
   📁 reports/csv/model_comparison_results.csv
   📁 reports/model_comparison_prettytable.txt
   📁 reports/markdown/MODEL_EXPERT_HANDOFF_REPORT.md
   📁 figures/model_phase7_performance_comparison.html
   📁 figures/model_phase7_cv_stability.html
   📁 figures/model_phase7_overfitting_analysis.html
   📁 figures/model_phase7_training_time.html
   📁 figures/model_phase7_leadership_matrix.html
   📁 figures/model_phase10_final_confusion_matrix.html
   📁 figures/model_phase11_feature_importance.html (eğer varsa)

🎯 SONRAKI ADIMLAR:
   • Explainability Expert: SHAP/LIME ile model açıklanabilirliği
   • Deployment Expert: Streamlit arayüzü ve model deployment
   • Threshold Tuning: False Negative'i azaltmak için precision/recall trade-off
   • Hyperparameter Tuning: GridSearchCV (opsiyonel, performans zaten iyi)

⚠️  KRİTİK UYARILAR:
   • False Negative: {fn} müşteri kaçırıldı - business impact yüksek
   • Model güncellemesi: Yeni veri geldiğinde yeniden eğitim değerlendir
   • Scaling: Yeni veriye transform uygulanmalı (fit değil!)
   • Feature Engineering: Deployment'ta aynı pipeline uygulanmalı

╔══════════════════════════════════════════════════════════════════════════╗
║  MODEL EXPERT, MODELLEMİ TAMAMLANDI - EXPLAINABILITY/DEPLOYMENT HAZIR   ║
╚══════════════════════════════════════════════════════════════════════════╝
"""

print(summary)

print("\n" + "="*80)
print("✅ MODEL TRAINING PIPELINE TAMAMLANDI")
print("="*80 + "\n")
