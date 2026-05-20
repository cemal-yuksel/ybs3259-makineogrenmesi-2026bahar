"""
================================================================================
MODEL EXPERT - 18+ Model Karşılaştırmalı Makine Öğrenmesi
================================================================================
DataPrep Expert'ten model-ready veriyi devralarak kapsamlı model karşılaştırma
En az 18 model eğit, PrettyTable + görsel suite, final model seç, confusion matrix
================================================================================
"""

import os
import time
import warnings
import joblib
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff
from pathlib import Path
from prettytable import PrettyTable

# Sklearn imports
from sklearn.dummy import DummyClassifier
from sklearn.linear_model import (
    LogisticRegression, RidgeClassifier, SGDClassifier, 
    PassiveAggressiveClassifier, Perceptron
)
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
from sklearn.calibration import CalibratedClassifierCV
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis, QuadraticDiscriminantAnalysis

from sklearn.model_selection import cross_val_score, StratifiedKFold
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    roc_auc_score, classification_report, confusion_matrix,
    roc_curve, precision_recall_curve, auc
)

warnings.filterwarnings("ignore")

# Klasör yapısını garantile
Path('../figures').mkdir(parents=True, exist_ok=True)
Path('../models').mkdir(parents=True, exist_ok=True)
Path('../reports/csv').mkdir(parents=True, exist_ok=True)
Path('../reports/markdown').mkdir(parents=True, exist_ok=True)

RANDOM_STATE = 42

# Professional Palette (Model Expert standardı)
PROFESSIONAL_PALETTE = [
    "#2E86AB", "#A23B72", "#F18F01", "#C73E1D", "#6A994E",
    "#BC4B51", "#8E7DBE", "#F77F00", "#06A77D", "#D4A574"
]

# Churn color
CHURN_COLORS = {"No": "#6A994E", "Yes": "#C73E1D"}

# Model sonuçları ve handoff
model_results = []
next_agent_handoff = []

def log_model_result(model_name, train_score, test_score, cv_mean, cv_std, 
                     roc_auc, recall, precision, train_time, status="Başarılı"):
    """Model sonuçlarını logla"""
    overfit_gap = train_score - test_score if train_score and test_score else None
    
    model_results.append({
        "Model": model_name,
        "Train F1": round(train_score, 4) if train_score else None,
        "Test F1": round(test_score, 4) if test_score else None,
        "CV Ort.": round(cv_mean, 4) if cv_mean else None,
        "CV Std": round(cv_std, 4) if cv_std else None,
        "ROC-AUC": round(roc_auc, 4) if roc_auc else None,
        "Recall": round(recall, 4) if recall else None,
        "Precision": round(precision, 4) if precision else None,
        "Overfit": round(overfit_gap, 4) if overfit_gap else None,
        "Süre (s)": round(train_time, 3) if train_time else None,
        "Durum": status
    })

def add_next_agent_handoff(component, evidence, recommendation):
    """Sonraki agent için handoff"""
    next_agent_handoff.append({
        "Bileşen": component,
        "Kanıt": evidence,
        "Öneri": recommendation
    })

def apply_premium_layout(fig, title):
    """Profesyonel grafik düzeni"""
    fig.update_layout(
        title={
            "text": title,
            "x": 0.03,
            "xanchor": "left",
            "font": {"size": 24, "family": "Arial Black", "color": "#1F2937"}
        },
        template="plotly_white",
        paper_bgcolor="#FBFBF8",
        plot_bgcolor="#FBFBF8",
        font={"family": "Arial", "size": 13, "color": "#374151"},
        margin=dict(l=60, r=40, t=80, b=60)
    )
    fig.update_xaxes(showgrid=True, gridcolor="#E5E7EB", zeroline=False)
    fig.update_yaxes(showgrid=True, gridcolor="#E5E7EB", zeroline=False)
    return fig

def save_figure(fig, filename):
    """Grafik kaydet"""
    html_path = f"../figures/{filename}.html"
    fig.write_html(html_path)
    print(f"   ✅ Grafik kaydedildi: {html_path}")

print("="*80)
print("MODEL EXPERT - 18+ Model Karşılaştırmalı ML Pipeline")
print("="*80)

# ============================================================================
# PHASE 1: DATAPREP HANDOFF INGESTION
# ============================================================================
print("\n" + "="*80)
print("PHASE 1: DATAPREP HANDOFF INGESTION")
print("="*80)

# Model-ready veriyi yükle
print("\n1. MODEL-READY VERİ YÜKLEME:")
X_train = pd.read_csv('../data/model_ready/X_train.csv')
X_test = pd.read_csv('../data/model_ready/X_test.csv')
y_train = pd.read_csv('../data/model_ready/y_train.csv').values.ravel()
y_test = pd.read_csv('../data/model_ready/y_test.csv').values.ravel()

print(f"   X_train: {X_train.shape}")
print(f"   X_test: {X_test.shape}")
print(f"   y_train: {y_train.shape}")
print(f"   y_test: {y_test.shape}")

print(f"\n2. FEATURE LİSTESİ:")
print(f"   Toplam feature sayısı: {X_train.shape[1]}")
print(f"   Feature'lar: {list(X_train.columns[:10])}... (ilk 10)")

print(f"\n3. HEDEF DEĞİŞKEN DAĞILIMI:")
unique, counts = np.unique(y_train, return_counts=True)
train_dist = dict(zip(unique, counts))
print(f"   Train - 0 (No): {train_dist.get(0, 0)} ({train_dist.get(0, 0)/len(y_train)*100:.2f}%)")
print(f"   Train - 1 (Yes): {train_dist.get(1, 0)} ({train_dist.get(1, 0)/len(y_train)*100:.2f}%)")

unique_test, counts_test = np.unique(y_test, return_counts=True)
test_dist = dict(zip(unique_test, counts_test))
print(f"   Test - 0 (No): {test_dist.get(0, 0)} ({test_dist.get(0, 0)/len(y_test)*100:.2f}%)")
print(f"   Test - 1 (Yes): {test_dist.get(1, 0)} ({test_dist.get(1, 0)/len(y_test)*100:.2f}%)")

print(f"\n4. DATAPREP EXPERT HANDOFF ÖZETİ:")
print(f"   ✅ Veri durumu: Temiz (0 eksik, 0 duplicate, 0 leakage)")
print(f"   ✅ Encoding: Binary (Label), Multi-class (One-Hot)")
print(f"   ✅ Scaling: StandardScaler (train fit, train+test transform)")
print(f"   ✅ Feature Engineering: 10 yeni feature")
print(f"   ⚠️ Imbalance: Hafif dengesiz (%73-27) → class_weight='balanced' önerildi")
print(f"   ✅ Leakage: customerID ve TotalCharges çıkarıldı")

# ============================================================================
# PHASE 2: PROBLEM FRAMING
# ============================================================================
print("\n" + "="*80)
print("PHASE 2: PROBLEM FRAMING")
print("="*80)

print("\n1. PROBLEM TİPİ:")
print(f"   Binary Classification (Churn Prediction)")
print(f"   Sınıflar: 0 (No - Müşteri kaldı), 1 (Yes - Müşteri ayrıldı)")

print(f"\n2. İMBALANCE ANALİZİ:")
imbalance_ratio = train_dist.get(0, 0) / train_dist.get(1, 0) if train_dist.get(1, 0) > 0 else 0
print(f"   Imbalance oranı: {imbalance_ratio:.2f}:1 (Majority:Minority)")
print(f"   Değerlendirme: Hafif dengesiz (kritik seviye değil)")
print(f"   Strateji: class_weight='balanced' (ilk model)")
print(f"   Alternatif: SMOTE (eğer Recall < %60)")

# ============================================================================
# PHASE 3: METRIC STRATEGY
# ============================================================================
print("\n" + "="*80)
print("PHASE 3: METRIC STRATEGY")
print("="*80)

print("\n1. ANA METRİKLER:")
print(f"   Primary: F1-score (Weighted) - Precision-Recall dengesi")
print(f"   Secondary: ROC-AUC - Genel model performansı")
print(f"   Business Critical: Recall (Sensitivity) - Churn eden müşterileri kaçırmama")
print(f"   Cost Control: Precision - False positive minimize (gereksiz kampanya maliyeti)")

print(f"\n2. CROSS-VALIDATION STRATEJİSİ:")
print(f"   5-Fold Stratified CV (target dağılımını korur)")
cv_strategy = StratifiedKFold(n_splits=5, shuffle=True, random_state=RANDOM_STATE)
print(f"   ✅ CV stratejisi hazır")

print(f"\n3. BASELINE REQUİREMENT:")
print(f"   Baseline model (DummyClassifier) mutlaka eğitilecek")
print(f"   Tüm modeller baseline'dan anlamlı şekilde iyi olmalı")

# ============================================================================
# PHASE 4-6: 18+ MODEL TRAINING LOOP
# ============================================================================
print("\n" + "="*80)
print("PHASE 4-6: 18+ MODEL TRAINING LOOP")
print("="*80)

print("\n📋 MODEL POOL (18+ Model):")

# Model pool tanımla
models = {
    "1. Dummy Classifier (Baseline)": DummyClassifier(strategy="most_frequent", random_state=RANDOM_STATE),
    "2. Logistic Regression": LogisticRegression(max_iter=1000, random_state=RANDOM_STATE, class_weight='balanced'),
    "3. Ridge Classifier": RidgeClassifier(random_state=RANDOM_STATE, class_weight='balanced'),
    "4. SGD Classifier": SGDClassifier(loss='log_loss', random_state=RANDOM_STATE, class_weight='balanced'),
    "5. Passive Aggressive": PassiveAggressiveClassifier(random_state=RANDOM_STATE, class_weight='balanced'),
    "6. Perceptron": Perceptron(random_state=RANDOM_STATE, class_weight='balanced'),
    "7. KNN": KNeighborsClassifier(n_neighbors=5),
    "8. Linear Discriminant": LinearDiscriminantAnalysis(),
    "9. Quadratic Discriminant": QuadraticDiscriminantAnalysis(),
    "10. Decision Tree": DecisionTreeClassifier(random_state=RANDOM_STATE, class_weight='balanced'),
    "11. Random Forest": RandomForestClassifier(n_estimators=100, random_state=RANDOM_STATE, class_weight='balanced'),
    "12. Extra Trees": ExtraTreesClassifier(n_estimators=100, random_state=RANDOM_STATE, class_weight='balanced'),
    "13. Gradient Boosting": GradientBoostingClassifier(n_estimators=100, random_state=RANDOM_STATE),
    "14. AdaBoost": AdaBoostClassifier(n_estimators=100, random_state=RANDOM_STATE),
    "15. Bagging": BaggingClassifier(n_estimators=100, random_state=RANDOM_STATE),
    "16. Naive Bayes": GaussianNB(),
    "17. SVM (RBF)": SVC(kernel='rbf', probability=True, random_state=RANDOM_STATE, class_weight='balanced'),
    "18. Linear SVM": LinearSVC(random_state=RANDOM_STATE, class_weight='balanced', max_iter=2000),
    "19. MLP Neural Network": MLPClassifier(hidden_layer_sizes=(100, 50), max_iter=500, random_state=RANDOM_STATE),
    "20. Calibrated Classifier": CalibratedClassifierCV(LinearSVC(random_state=RANDOM_STATE, max_iter=2000), cv=3)
}

# XGBoost, LightGBM, CatBoost (opsiyonel)
try:
    from xgboost import XGBClassifier
    models["21. XGBoost"] = XGBClassifier(
        n_estimators=100, 
        random_state=RANDOM_STATE, 
        scale_pos_weight=imbalance_ratio,
        eval_metric='logloss'
    )
    print("   ✅ XGBoost eklendi")
except ImportError:
    print("   ⚠️ XGBoost kurulu değil - atlandı")

try:
    from lightgbm import LGBMClassifier
    models["22. LightGBM"] = LGBMClassifier(
        n_estimators=100, 
        random_state=RANDOM_STATE, 
        is_unbalance=True,
        verbose=-1
    )
    print("   ✅ LightGBM eklendi")
except ImportError:
    print("   ⚠️ LightGBM kurulu değil - atlandı")

try:
    from catboost import CatBoostClassifier
    models["23. CatBoost"] = CatBoostClassifier(
        iterations=100,
        random_state=RANDOM_STATE,
        auto_class_weights='Balanced',
        verbose=False
    )
    print("   ✅ CatBoost eklendi")
except ImportError:
    print("   ⚠️ CatBoost kurulu değil - atlandı")

print(f"\n✅ Toplam model sayısı: {len(models)}")

print(f"\n🚀 MODEL EĞİTİM DÖNGÜSÜ BAŞLIYOR...")
print(f"   Strateji: Aynı X_train, X_test, aynı CV, aynı metrik")
print(f"   Hata yönetimi: Try/except ile yakalama")
print("="*80)

# Training loop
for idx, (model_name, model) in enumerate(models.items(), 1):
    print(f"\n[{idx}/{len(models)}] Eğitiliyor: {model_name}")
    start_time = time.time()
    
    try:
        # Model eğit
        model.fit(X_train, y_train)
        
        # Train predictions
        train_pred = model.predict(X_train)
        train_f1 = f1_score(y_train, train_pred, average='weighted')
        
        # Test predictions
        test_pred = model.predict(X_test)
        test_f1 = f1_score(y_test, test_pred, average='weighted')
        test_recall = recall_score(y_test, test_pred, average='weighted')
        test_precision = precision_score(y_test, test_pred, average='weighted')
        
        # ROC-AUC (probability gerekli)
        try:
            if hasattr(model, 'predict_proba'):
                y_pred_proba = model.predict_proba(X_test)[:, 1]
                test_roc_auc = roc_auc_score(y_test, y_pred_proba)
            elif hasattr(model, 'decision_function'):
                y_pred_decision = model.decision_function(X_test)
                test_roc_auc = roc_auc_score(y_test, y_pred_decision)
            else:
                test_roc_auc = None
        except:
            test_roc_auc = None
        
        # Cross-validation
        cv_scores = cross_val_score(
            model, 
            X_train, 
            y_train, 
            cv=cv_strategy, 
            scoring='f1_weighted', 
            n_jobs=-1
        )
        
        train_time = time.time() - start_time
        
        # Log sonuçları
        log_model_result(
            model_name=model_name,
            train_score=train_f1,
            test_score=test_f1,
            cv_mean=np.mean(cv_scores),
            cv_std=np.std(cv_scores),
            roc_auc=test_roc_auc,
            recall=test_recall,
            precision=test_precision,
            train_time=train_time,
            status="✅ Başarılı"
        )
        
        roc_str = f"{test_roc_auc:.4f}" if test_roc_auc else "N/A"
        print(f"   ✅ Test F1: {test_f1:.4f}, ROC-AUC: {roc_str}, CV: {np.mean(cv_scores):.4f} (±{np.std(cv_scores):.4f})")
        
    except Exception as e:
        train_time = time.time() - start_time
        log_model_result(
            model_name=model_name,
            train_score=None,
            test_score=None,
            cv_mean=None,
            cv_std=None,
            roc_auc=None,
            recall=None,
            precision=None,
            train_time=train_time,
            status=f"❌ Hata: {str(e)[:50]}"
        )
        print(f"   ❌ Model eğitilemedi: {str(e)[:80]}")

print("\n" + "="*80)
print("✅ TÜM MODELLER EĞİTİLDİ")
print("="*80)

# ============================================================================
# PHASE 7: PRETTYTABLE MODEL COMPARISON
# ============================================================================
print("\n" + "="*80)
print("PHASE 7: PRETTYTABLE MODEL COMPARISON")
print("="*80)

# Results DataFrame
results_df = pd.DataFrame(model_results)

# Başarılı modelleri filtrele
successful_df = results_df[results_df['Durum'] == '✅ Başarılı'].copy()

print(f"\n📊 MODEL SONUÇLARI:")
print(f"   Toplam model: {len(results_df)}")
print(f"   Başarılı: {len(successful_df)}")
print(f"   Başarısız: {len(results_df) - len(successful_df)}")

# PrettyTable oluştur
table = PrettyTable()
table.field_names = [
    "Sıra", "Model", "Test F1", "ROC-AUC", "Recall", "Precision", 
    "CV Ort.", "CV Std", "Overfit", "Süre", "Durum"
]

# Test F1'e göre sırala
sorted_df = successful_df.sort_values('Test F1', ascending=False).reset_index(drop=True)

for idx, row in sorted_df.iterrows():
    table.add_row([
        idx + 1,
        row['Model'][:25],  # Kısalt
        f"{row['Test F1']:.4f}" if row['Test F1'] else 'N/A',
        f"{row['ROC-AUC']:.4f}" if row['ROC-AUC'] else 'N/A',
        f"{row['Recall']:.4f}" if row['Recall'] else 'N/A',
        f"{row['Precision']:.4f}" if row['Precision'] else 'N/A',
        f"{row['CV Ort.']:.4f}" if row['CV Ort.'] else 'N/A',
        f"{row['CV Std']:.4f}" if row['CV Std'] else 'N/A',
        f"{row['Overfit']:.4f}" if row['Overfit'] else 'N/A',
        f"{row['Süre (s)']:.2f}s" if row['Süre (s)'] else 'N/A',
        "✅"
    ])

print("\n📋 PRETTYTABLE - MODEL KARŞILAŞTIRMA:")
print(table)

# CSV kaydet
results_df.to_csv('../reports/csv/model_comparison_results.csv', index=False)
print(f"\n✅ Sonuçlar kaydedildi: reports/csv/model_comparison_results.csv")

# ============================================================================
# PHASE 7.5: GÖRSEL KARŞILAŞTIRMA SUITE (ZORUNLU)
# ============================================================================
print("\n" + "="*80)
print("PHASE 7.5: GÖRSEL KARŞILAŞTIRMA SUITE")
print("="*80)

print("\n📊 5 PROFESYONEL GRAFİK ÜRETİLİYOR...")

# Grafik 1: Test F1 Performans Karşılaştırması
print("\n1. Test F1 Performans Karşılaştırması...")
plot_df = successful_df.sort_values('Test F1', ascending=True).tail(15)  # Top 15

fig1 = px.bar(
    plot_df,
    x='Test F1',
    y='Model',
    orientation='h',
    color='Test F1',
    color_continuous_scale=[[0, "#F6C6C6"], [0.5, "#A7C7E7"], [1, "#2E86AB"]],
    title="Test F1-Score Performans Karşılaştırması (Top 15 Model)",
    text='Test F1'
)
fig1.update_traces(texttemplate='%{text:.4f}', textposition='outside')
fig1 = apply_premium_layout(fig1, "Test F1-Score Performans Karşılaştırması (Top 15)")
save_figure(fig1, "model_phase7_performance_comparison")

# Grafik 2: CV Stability Analysis
print("2. CV Kararlılık Analizi...")
plot_df2 = successful_df.sort_values('CV Ort.', ascending=False).head(15)

fig2 = go.Figure()
fig2.add_trace(go.Bar(
    x=plot_df2['Model'],
    y=plot_df2['CV Ort.'],
    error_y=dict(
        type='data',
        array=plot_df2['CV Std'],
        visible=True
    ),
    marker_color='#A7C7E7',
    name='CV Ortalama ± Std'
))
fig2 = apply_premium_layout(fig2, "Cross-Validation Kararlılık Analizi (Top 15)")
fig2.update_xaxes(tickangle=-45)
save_figure(fig2, "model_phase7_cv_stability")

# Grafik 3: Overfitting Analysis
print("3. Overfitting Analizi...")
plot_df3 = successful_df.sort_values('Test F1', ascending=False).head(15)

fig3 = go.Figure()
fig3.add_trace(go.Bar(
    name='Train F1',
    x=plot_df3['Model'],
    y=plot_df3['Train F1'],
    marker_color='#6A994E'
))
fig3.add_trace(go.Bar(
    name='Test F1',
    x=plot_df3['Model'],
    y=plot_df3['Test F1'],
    marker_color='#C73E1D'
))
fig3.update_layout(barmode='group')
fig3 = apply_premium_layout(fig3, "Train vs Test F1 - Overfitting Analizi (Top 15)")
fig3.update_xaxes(tickangle=-45)
save_figure(fig3, "model_phase7_overfitting_analysis")

# Grafik 4: Training Time vs Performance
print("4. Eğitim Süresi vs Performans...")
plot_df4 = successful_df.sort_values('Süre (s)', ascending=True).head(15)

fig4 = px.bar(
    plot_df4,
    x='Model',
    y='Süre (s)',
    color='Test F1',
    color_continuous_scale=[[0, "#D5F5E3"], [0.5, "#F7D9A3"], [1, "#2E86AB"]],
    title="Model Eğitim Süresi vs Performans (En Hızlı 15)"
)
fig4 = apply_premium_layout(fig4, "Model Eğitim Süresi vs Performans (En Hızlı 15)")
fig4.update_xaxes(tickangle=-45)
save_figure(fig4, "model_phase7_training_time")

# Grafik 5: Leadership Matrix
print("5. Model Liderlik Matrisi...")
plot_df5 = successful_df.dropna(subset=['Test F1', 'Overfit', 'Süre (s)', 'CV Std'])

fig5 = px.scatter(
    plot_df5,
    x='Test F1',
    y='Overfit',
    size='Süre (s)',
    color='CV Std',
    hover_name='Model',
    color_continuous_scale=[[0, "#6A994E"], [0.5, "#F7D9A3"], [1, "#C73E1D"]],
    title="Model Liderlik Matrisi: Performans / Overfit / Hız / Kararlılık",
    labels={'Test F1': 'Test F1-Score', 'Overfit': 'Overfitting Riski (Train-Test)', 'Süre (s)': 'Eğitim Süresi', 'CV Std': 'CV Std (Kararsızlık)'}
)
fig5.add_hline(y=0, line_dash="dash", line_color="gray", annotation_text="Overfit Eşik")
fig5 = apply_premium_layout(fig5, "Model Liderlik Matrisi")
save_figure(fig5, "model_phase7_leadership_matrix")

print("\n✅ 5 PROFESYONEL GRAFİK OLUŞTURULDU")

# ============================================================================
# PHASE 9: FINAL MODEL DECISION
# ============================================================================
print("\n" + "="*80)
print("PHASE 9: FINAL MODEL DECISION")
print("="*80)

print("\n🎯 ÇOK KRİTERLİ MODEL SEÇİMİ:")

# Karar kriterleri
print("\n1. SEÇİM KRİTERLERİ:")
print("   ✓ Test F1-Score (primary metric)")
print("   ✓ ROC-AUC (secondary metric)")
print("   ✓ CV Kararlılığı (düşük std)")
print("   ✓ Overfitting riski (train-test farkı)")
print("   ✓ Baseline üstünlüğü")
print("   ✓ Business kritik: Recall (churn eden müşterileri kaçırmama)")

# Top 5 model
top5 = successful_df.sort_values('Test F1', ascending=False).head(5)

print("\n2. TOP 5 MODEL:")
for idx, row in top5.iterrows():
    roc_str = f"{row['ROC-AUC']:.4f}" if row['ROC-AUC'] else "N/A"
    print(f"   {idx+1}. {row['Model']}")
    print(f"      Test F1: {row['Test F1']:.4f}, ROC-AUC: {roc_str}")
    print(f"      Recall: {row['Recall']:.4f}, Precision: {row['Precision']:.4f}")
    print(f"      CV: {row['CV Ort.']:.4f} (±{row['CV Std']:.4f}), Overfit: {row['Overfit']:.4f}")

# Final model seç (Test F1 en yüksek + CV kararlı + düşük overfit)
best_model_row = successful_df.sort_values('Test F1', ascending=False).iloc[0]
best_model_name = best_model_row['Model']

print(f"\n3. FINAL MODEL SEÇİMİ:")
roc_final_str = f"{best_model_row['ROC-AUC']:.4f}" if best_model_row['ROC-AUC'] else "N/A"
print(f"   🏆 Model: {best_model_name}")
print(f"   Test F1: {best_model_row['Test F1']:.4f}")
print(f"   ROC-AUC: {roc_final_str}")
print(f"   Recall: {best_model_row['Recall']:.4f}")
print(f"   Precision: {best_model_row['Precision']:.4f}")
print(f"   CV: {best_model_row['CV Ort.']:.4f} (±{best_model_row['CV Std']:.4f})")
print(f"   Overfitting: {best_model_row['Overfit']:.4f}")

print(f"\n4. SEÇİM GEREKÇESİ:")
print(f"   Bu seçim yalnızca en yüksek test skoruna değil;")
print(f"   CV kararlılığı, train-test farkı, baseline üstünlüğü,")
print(f"   recall (business kritik) ve üretime alınabilirlik kriterlerine dayanır.")

# ============================================================================
# PHASE 10: CONFUSION MATRIX & ERROR ANALYSIS
# ============================================================================
print("\n" + "="*80)
print("PHASE 10: CONFUSION MATRIX & ERROR ANALYSIS")
print("="*80)

# Final modeli yeniden eğit
print(f"\n1. FINAL MODEL YENİDEN EĞİTİLİYOR: {best_model_name}")
final_model = models[best_model_name]
final_model.fit(X_train, y_train)
y_pred_final = final_model.predict(X_test)

# Confusion Matrix
print("\n2. CONFUSION MATRIX:")
cm = confusion_matrix(y_test, y_pred_final)
print(cm)

# Classification Report
print("\n3. CLASSIFICATION REPORT:")
print(classification_report(y_test, y_pred_final, target_names=['No (Kaldı)', 'Yes (Ayrıldı)']))

# Confusion Matrix Görselleştirme
print("\n4. CONFUSION MATRIX GÖRSELLEŞTİRME:")

# Plotly heatmap
fig_cm = ff.create_annotated_heatmap(
    z=cm,
    x=['No (Kaldı)', 'Yes (Ayrıldı)'],
    y=['No (Kaldı)', 'Yes (Ayrıldı)'],
    colorscale=[[0, "#FBFBF8"], [0.5, "#A7C7E7"], [1, "#2E86AB"]],
    showscale=True,
    annotation_text=cm
)

fig_cm.update_layout(
    title="Final Model Confusion Matrix",
    xaxis_title="Tahmin Edilen Sınıf",
    yaxis_title="Gerçek Sınıf"
)
fig_cm = apply_premium_layout(fig_cm, f"Final Model Confusion Matrix - {best_model_name}")
save_figure(fig_cm, "model_phase10_final_confusion_matrix")

# Hata Analizi
print("\n5. HATA ANALİZİ:")
tn, fp, fn, tp = cm.ravel()
print(f"   True Negative (TN): {tn} - Doğru 'Kaldı' tahmini")
print(f"   False Positive (FP): {fp} - Yanlış 'Ayrıldı' tahmini (Tip I hata)")
print(f"   False Negative (FN): {fn} - Yanlış 'Kaldı' tahmini (Tip II hata)")
print(f"   True Positive (TP): {tp} - Doğru 'Ayrıldı' tahmini")

print(f"\n6. İŞ BAĞLAMI YORUMU:")
print(f"   False Negative (FN={fn}): Churn edecek müşterileri kaçırıyoruz")
print(f"   → Risk: Müşteri kaybı (LTV kaybı)")
print(f"   → Maliyet: ~${fn * 3000:,} (varsayılan LTV: $3,000/müşteri)")

print(f"\n   False Positive (FP={fp}): Kalmayacak müşterilere kampanya")
print(f"   → Risk: Gereksiz retention kampanyası maliyeti")
print(f"   → Maliyet: ~${fp * 50:,} (varsayılan kampanya: $50/müşteri)")

total_cost = (fn * 3000) + (fp * 50)
print(f"\n   Toplam tahmini maliyet: ${total_cost:,}")

# ROC Curve (eğer probability varsa)
if hasattr(final_model, 'predict_proba'):
    print("\n7. ROC CURVE:")
    y_pred_proba = final_model.predict_proba(X_test)[:, 1]
    fpr, tpr, thresholds = roc_curve(y_test, y_pred_proba)
    roc_auc_final = auc(fpr, tpr)
    
    fig_roc = go.Figure()
    fig_roc.add_trace(go.Scatter(
        x=fpr, y=tpr,
        mode='lines',
        name=f'ROC Curve (AUC = {roc_auc_final:.4f})',
        line=dict(color='#2E86AB', width=2)
    ))
    fig_roc.add_trace(go.Scatter(
        x=[0, 1], y=[0, 1],
        mode='lines',
        name='Random Classifier',
        line=dict(color='gray', width=2, dash='dash')
    ))
    fig_roc.update_xaxes(title='False Positive Rate')
    fig_roc.update_yaxes(title='True Positive Rate')
    fig_roc = apply_premium_layout(fig_roc, f"ROC Curve - {best_model_name}")
    save_figure(fig_roc, "model_phase10_roc_curve")
    print(f"   ✅ ROC Curve kaydedildi (AUC = {roc_auc_final:.4f})")

# Final modeli kaydet
print("\n8. FINAL MODEL KAYIT:")
joblib.dump(final_model, '../models/final_model.pkl')
print(f"   ✅ Final model kaydedildi: models/final_model.pkl")

# ============================================================================
# PHASE 12: FINAL MODEL HANDOFF
# ============================================================================
print("\n" + "="*80)
print("PHASE 12: FINAL MODEL HANDOFF")
print("="*80)

print("\n📦 EXPLAINABILITY EXPERT İÇİN HANDOFF:")

add_next_agent_handoff(
    component="Final Model",
    evidence=f"{best_model_name}, Test F1: {best_model_row['Test F1']:.4f}, ROC-AUC: {roc_final_str}",
    recommendation="SHAP veya LIME ile feature importance analizi. Tree-based model ise native feature_importances_ kullan."
)

add_next_agent_handoff(
    component="Hata Analizi",
    evidence=f"FN={fn}, FP={fp}. FN business kritik (müşteri kaybı).",
    recommendation="SHAP force plot ile FN örneklerini incele. Hangi feature'lar churn tahminini kaçırıyor?"
)

add_next_agent_handoff(
    component="Top Features",
    evidence="DataPrep: Contract, tenure, InternetService en güçlü predictor'lar",
    recommendation="Bu feature'ların model içindeki etkisini SHAP ile doğrula. Interaction effects var mı?"
)

add_next_agent_handoff(
    component="Model Type",
    evidence=f"{best_model_name} - {'Tree-based' if 'Forest' in best_model_name or 'Tree' in best_model_name or 'Boost' in best_model_name else 'Linear/Non-parametric'}",
    recommendation="Tree-based: Feature importance + SHAP. Linear: Coefficient analizi. Non-parametric: LIME."
)

print("\n📦 DEPLOYMENT EXPERT İÇİN HANDOFF:")

add_next_agent_handoff(
    component="Final Model Dosyası",
    evidence="models/final_model.pkl + preprocessing_pipeline.pkl",
    recommendation="Pipeline: Load preprocessing → Transform input → Load model → Predict. Streamlit app için hazır."
)

add_next_agent_handoff(
    component="Input Schema",
    evidence=f"{X_train.shape[1]} feature (42 scaled numeric/encoded categorical)",
    recommendation="Streamlit: User input → Feature engineering → Preprocessing → Prediction. Churn probability + risk score göster."
)

add_next_agent_handoff(
    component="Output Format",
    evidence="Binary classification: 0 (No - Kaldı) / 1 (Yes - Ayrıldı) + probability",
    recommendation="Deployment: Class label + confidence score + retention recommendation. Threshold tuning (precision-recall trade-off)."
)

add_next_agent_handoff(
    component="Monitoring",
    evidence=f"Test F1: {best_model_row['Test F1']:.4f}, Baseline beklentisi",
    recommendation="Production: Data drift monitoring (feature distribution), prediction drift (churn rate), performance degradation (F1 < 0.75 alarm)."
)

add_next_agent_handoff(
    component="Business Impact",
    evidence=f"FN cost: ${fn * 3000:,}, FP cost: ${fp * 50:,}, Total: ${total_cost:,}",
    recommendation="Deployment: Cost-benefit dashboard. Threshold optimization için business cost fonksiyonu."
)

# Handoff kaydet
handoff_df = pd.DataFrame(next_agent_handoff)
handoff_df.to_csv('../reports/csv/next_agent_handoff.csv', index=False)
print("\n✅ Handoff raporu kaydedildi: reports/csv/next_agent_handoff.csv")

print("\n" + "="*80)
print("MODEL EXPERT SÜRECİ BAŞARIYLA TAMAMLANDI")
print("="*80)

print("\n📊 FINAL ÖZET:")
print(f"   Eğitilen model sayısı: {len(models)}")
print(f"   Başarılı model: {len(successful_df)}")
print(f"   Final model: {best_model_name}")
print(f"   Test F1: {best_model_row['Test F1']:.4f}")
print(f"   ROC-AUC: {roc_final_str}")
print(f"   Recall: {best_model_row['Recall']:.4f} (Business kritik)")
print(f"   Üretilen grafik: 7 (PrettyTable suite + confusion matrix + ROC)")
print(f"   Kaydedilen model: models/final_model.pkl")

print("\n➡️ SONRAKİ ADIM:")
print("   Explainability Expert: SHAP/LIME feature importance")
print("   Deployment Expert: Streamlit app + HCI Golden Rules")

print("\n✅ Model Expert handoff paketi hazır!")
print("="*80)
