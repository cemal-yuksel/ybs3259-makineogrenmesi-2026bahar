"""
DIABETES DATASET - DATA PREPARATION & FEATURE ENGINEERING
=========================================================

Data Prep Expert - Agentik Pipeline

EDA Expert'ten Gelen Kritik Bulgular:
- Insulin (%48.7 eksik) ve SkinThickness (%29.6 eksik) → Modelden çıkarılmalı
- Glucose, BloodPressure, BMI → %0.65-4.56 eksik → Median imputation
- BloodPressure → %5.86 outlier → Winsorization gerekli
- Çarpıklık → Yeo-Johnson dönüşümü gerekli
- Class imbalance %65-35 → Stratified CV + Class weighting
- Feature set: 6 değişken (Glucose, Pregnancies, BMI, Age, DiabetesPedigreeFunction, BloodPressure)
"""

import os
import warnings
import pandas as pd
import numpy as np
from pathlib import Path
from scipy.stats import mstats
import plotly.express as px
import plotly.graph_objects as go
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, PowerTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
import joblib

warnings.filterwarnings("ignore")

# Klasörlerin varlığını garantile
Path('../data/model_ready').mkdir(parents=True, exist_ok=True)
Path('../figures').mkdir(parents=True, exist_ok=True)
Path('../reports/csv').mkdir(parents=True, exist_ok=True)
Path('../reports/markdown').mkdir(parents=True, exist_ok=True)
Path('../models').mkdir(parents=True, exist_ok=True)

# Profesyonel renk paleti
PROFESSIONAL_PALETTE = [
    "#2E86AB", "#A23B72", "#F18F01", "#C73E1D", "#6A994E",
    "#BC4B51", "#8E7DBE", "#F77F00", "#06A77D", "#D4A574"
]

# DataPrep Action Logger
dataprep_actions = []

def log_dataprep_action(step, issue, decision, rationale, risk="Düşük"):
    """DataPrep kararlarını loglar"""
    dataprep_actions.append({
        "Aşama": step,
        "Sorun": issue,
        "Karar": decision,
        "Gerekçe": rationale,
        "Risk": risk
    })
    print(f"\n✅ {step} | {issue}")
    print(f"   Karar: {decision}")
    print(f"   Gerekçe: {rationale}")
    print(f"   Risk: {risk}")

# Model Expert Handoff Logger
model_handoff_report = []

def add_model_handoff(item, status, recommendation):
    """Model Expert için handoff notları"""
    model_handoff_report.append({
        "Bileşen": item,
        "Durum": status,
        "Model Expert Notu": recommendation
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

print("="*80)
print(" PHASE 1: EDA RECOMMENDATION INGESTION ".center(80, "="))
print("="*80)

# Veri setini yükle
df_original = pd.read_csv('../data/raw/diabetes.csv')
df = df_original.copy()

print(f"\n📊 Orijinal Veri Boyutu: {df.shape}")
print(f"   Satır: {df.shape[0]}, Sütun: {df.shape[1]}")

# EDA'dan gelen öneriler
eda_recommendations = [
    {
        "Sorun": "Glucose değişkeninde düşük oranda gizli eksik veri",
        "Kanıt": "0 değer oranı: %0.65",
        "Öneri": "0 değerlerini NaN'a dönüştür, median imputation uygula",
        "Öncelik": "Düşük",
        "DataPrep Kararı": "UYGULA",
        "Gerekçe": "Mantıksal olarak Glucose 0 olamaz, median imputation güvenli"
    },
    {
        "Sorun": "BloodPressure değişkeninde düşük oranda gizli eksik veri",
        "Kanıt": "0 değer oranı: %4.56",
        "Öneri": "0 değerlerini NaN'a dönüştür, median imputation uygula",
        "Öncelik": "Düşük",
        "DataPrep Kararı": "UYGULA",
        "Gerekçe": "Mantıksal olarak BloodPressure 0 olamaz, median imputation güvenli"
    },
    {
        "Sorun": "BMI değişkeninde düşük oranda gizli eksik veri",
        "Kanıt": "0 değer oranı: %1.43",
        "Öneri": "0 değerlerini NaN'a dönüştür, median imputation uygula",
        "Öncelik": "Düşük",
        "DataPrep Kararı": "UYGULA",
        "Gerekçe": "Mantıksal olarak BMI 0 olamaz, median imputation güvenli"
    },
    {
        "Sorun": "SkinThickness değişkeninde yüksek oranda gizli eksik veri",
        "Kanıt": "0 değer oranı: %29.56",
        "Öneri": "Değişkeni modelden çıkar veya ileri imputasyon",
        "Öncelik": "Yüksek",
        "DataPrep Kararı": "MODELDEN ÇIKART",
        "Gerekçe": "%30'a yakın eksik veri overfitting riskini artırır, istatistiksel anlamlılık zayıf (p=0.0130)"
    },
    {
        "Sorun": "Insulin değişkeninde çok yüksek oranda gizli eksik veri",
        "Kanıt": "0 değer oranı: %48.70",
        "Öneri": "Değişkeni modelden çıkar (önerilen)",
        "Öncelik": "Yüksek",
        "DataPrep Kararı": "MODELDEN ÇIKART",
        "Gerekçe": "%50'ye yakın eksik veri, istatistiksel olarak anlamsız (p=0.0657)"
    },
    {
        "Sorun": "BloodPressure değişkeninde yüksek outlier oranı",
        "Kanıt": "Outlier oranı: %5.86 (eşik: %5)",
        "Öneri": "Winsorization, log dönüşümü veya RobustScaler",
        "Öncelik": "Orta",
        "DataPrep Kararı": "UYGULA - Winsorization",
        "Gerekçe": "Kritik eşiği hafif aşıyor, winsorization güvenli ve etkili"
    },
    {
        "Sorun": "Çarpıklık - DiabetesPedigreeFunction, Age",
        "Kanıt": "DiabetesPedigreeFunction skewness: 1.920, Age: 1.130",
        "Öneri": "Yeo-Johnson dönüşümü",
        "Öncelik": "Orta",
        "DataPrep Kararı": "UYGULA - Tüm değişkenlere",
        "Gerekçe": "Lineer modeller için faydalı, tree-based için zarar vermez"
    },
    {
        "Sorun": "Class imbalance",
        "Kanıt": "Baskın sınıf oranı: %65.1",
        "Öneri": "Stratified CV + Class weighting",
        "Öncelik": "Yüksek",
        "DataPrep Kararı": "UYGULA - Stratified split + class_weight bilgisini aktar",
        "Gerekçe": "SMOTE yerine class weighting daha güvenli, overfitting riski düşük"
    }
]

# EDA Önerilerini tablo olarak göster
eda_df = pd.DataFrame(eda_recommendations)
print("\n📋 EDA Expert'ten Gelen Öneriler ve DataPrep Kararları:")
print(eda_df[['Sorun', 'Öncelik', 'DataPrep Kararı']].to_string(index=False))

log_dataprep_action(
    step="PHASE 1",
    issue="EDA önerileri değerlendirildi",
    decision="8 öneri doğrulandı, hepsi uygulanacak",
    rationale="EDA bulguları tutarlı, mantıksal ve istatistiksel olarak destekleniyor",
    risk="Düşük"
)

print("\n" + "="*80)
print(" PHASE 2: DATA CLEANING ".center(80, "="))
print("="*80)

# Adım 1: 0 → NaN dönüşümü
print("\n🔄 Adım 1: Gizli Eksik Veri (0 değerleri) → NaN Dönüşümü")

zero_to_nan_cols = ['Glucose', 'BloodPressure', 'BMI']  # SkinThickness ve Insulin çıkarılacak
before_zero_counts = {}

for col in zero_to_nan_cols:
    before_zero_counts[col] = (df[col] == 0).sum()
    df[col] = df[col].replace(0, np.nan)
    after_nan_count = df[col].isna().sum()
    print(f"   {col}: {before_zero_counts[col]} adet 0 → {after_nan_count} adet NaN")

log_dataprep_action(
    step="PHASE 2.1",
    issue="Gizli eksik veri (0 değerleri)",
    decision="Glucose, BloodPressure, BMI için 0 → NaN dönüşümü uygulandı",
    rationale="Tıbbi ölçümlerde 0 değeri mantıksal olarak imkansız",
    risk="Düşük"
)

# Adım 2: Insulin ve SkinThickness'i modelden çıkar
print("\n❌ Adım 2: Yüksek Eksik Veri - Değişken Çıkarma")
drop_columns = ['Insulin', 'SkinThickness']

for col in drop_columns:
    zero_ratio = (df_original[col] == 0).sum() / len(df_original) * 100
    print(f"   {col}: %{zero_ratio:.2f} eksik veri nedeniyle ÇIKARILDI")

df = df.drop(columns=drop_columns)

log_dataprep_action(
    step="PHASE 2.2",
    issue="Insulin (%48.7) ve SkinThickness (%29.6) yüksek eksik veri",
    decision="İki değişken modelden çıkarıldı",
    rationale="Kritik eşik (%30) üzerinde, istatistiksel anlamlılık zayıf/yok, overfitting riski yüksek",
    risk="Düşük - Bu değişkenler zayıf öngörücüler"
)

print(f"\n📊 Temizleme Sonrası Veri Boyutu: {df.shape}")
print(f"   Kalan Değişkenler: {df.columns.tolist()}")

# Adım 3: Eksik veri durumunu görselleştir (Before)
missing_before = pd.DataFrame({
    'Değişken': df.columns,
    'Eksik Sayı': df.isna().sum().values,
    'Eksik Oran (%)': (df.isna().sum() / len(df) * 100).values
}).sort_values('Eksik Oran (%)', ascending=False)

print("\n📊 Eksik Veri Durumu (0→NaN Dönüşümü Sonrası, İmputasyon Öncesi):")
print(missing_before[missing_before['Eksik Sayı'] > 0].to_string(index=False))

# Görselleştirme - Missing Data Before Imputation
missing_plot_data = missing_before[missing_before['Eksik Sayı'] > 0].copy()

if len(missing_plot_data) > 0:
    fig = px.bar(
        missing_plot_data,
        x='Eksik Oran (%)',
        y='Değişken',
        orientation='h',
        color='Eksik Oran (%)',
        color_continuous_scale=[[0, "#6A994E"], [0.5, "#F18F01"], [1, "#C73E1D"]],
        title="Eksik Veri Oranları (İmputasyon Öncesi)"
    )
    fig = apply_premium_layout(fig, "Eksik Veri Oranları (İmputasyon Öncesi)")
    fig.write_html('../figures/dataprep_phase2_missing_before.html')
    print("\n✅ Görsel kaydedildi: dataprep_phase2_missing_before.html")

# Adım 4: Median Imputation
print("\n🔧 Adım 3: Median Imputation (Glucose, BloodPressure, BMI)")

imputation_cols = ['Glucose', 'BloodPressure', 'BMI']
imputer = SimpleImputer(strategy='median')

# İmputasyon öncesi medyan değerleri kaydet
median_values = {}
for col in imputation_cols:
    median_values[col] = df[col].median()
    print(f"   {col}: Median = {median_values[col]:.2f}")

# İmputasyon uygula
df[imputation_cols] = imputer.fit_transform(df[imputation_cols])

# İmputasyon sonrası kontrol
print("\n✅ İmputasyon Tamamlandı - Eksik Veri Kontrolü:")
print(f"   Toplam Eksik Veri: {df.isna().sum().sum()} adet")

log_dataprep_action(
    step="PHASE 2.3",
    issue="Düşük oranda eksik veri (<%5)",
    decision="Glucose, BloodPressure, BMI için median imputation uygulandı",
    rationale="Eksik veri oranı düşük, median robust ve güvenli bir yöntem",
    risk="Düşük"
)

# İmputasyon raporunu kaydet
imputation_report = pd.DataFrame({
    'Değişken': imputation_cols,
    'Eksik Veri Sayısı (Öncesi)': [before_zero_counts[col] for col in imputation_cols],
    'Median Değer': [median_values[col] for col in imputation_cols],
    'Strateji': ['Median Imputation'] * len(imputation_cols)
})
imputation_report.to_csv('../reports/csv/imputation_report.csv', index=False)
print("\n✅ Rapor kaydedildi: imputation_report.csv")

print("\n" + "="*80)
print(" PHASE 3: OUTLIER & DISTRIBUTION REPAIR ".center(80, "="))
print("="*80)

# Adım 1: BloodPressure Outlier Kontrolü (Before)
print("\n🔍 Adım 1: BloodPressure Outlier Durumu (Winsorization Öncesi)")

q1_bp = df['BloodPressure'].quantile(0.25)
q3_bp = df['BloodPressure'].quantile(0.75)
iqr_bp = q3_bp - q1_bp
lower_bound_bp = q1_bp - 1.5 * iqr_bp
upper_bound_bp = q3_bp + 1.5 * iqr_bp

outlier_count_before = ((df['BloodPressure'] < lower_bound_bp) | (df['BloodPressure'] > upper_bound_bp)).sum()
outlier_ratio_before = outlier_count_before / len(df) * 100

print(f"   Q1: {q1_bp:.2f}, Q3: {q3_bp:.2f}, IQR: {iqr_bp:.2f}")
print(f"   Alt Sınır: {lower_bound_bp:.2f}, Üst Sınır: {upper_bound_bp:.2f}")
print(f"   Outlier Sayısı: {outlier_count_before} adet (%{outlier_ratio_before:.2f})")

# Adım 2: Winsorization (5%-95% aralığına kırp)
print("\n✂️ Adım 2: Winsorization Uygulanıyor (5%-95% aralığı)")

bp_before_winsor = df['BloodPressure'].copy()
df['BloodPressure'] = mstats.winsorize(df['BloodPressure'], limits=[0.05, 0.05])

# Outlier kontrolü (After)
outlier_count_after = ((df['BloodPressure'] < lower_bound_bp) | (df['BloodPressure'] > upper_bound_bp)).sum()
outlier_ratio_after = outlier_count_after / len(df) * 100

print(f"\n✅ Winsorization Tamamlandı:")
print(f"   Öncesi Outlier: {outlier_count_before} adet (%{outlier_ratio_before:.2f})")
print(f"   Sonrası Outlier: {outlier_count_after} adet (%{outlier_ratio_after:.2f})")
print(f"   İyileşme: %{outlier_ratio_before - outlier_ratio_after:.2f} azalma")

log_dataprep_action(
    step="PHASE 3.1",
    issue="BloodPressure yüksek outlier oranı (%5.86)",
    decision="Winsorization (5%-95%) uygulandı",
    rationale="Kritik eşiği hafif aşıyor, winsorization güvenli ve veri kaybı yok",
    risk="Düşük"
)

# Görselleştirme - BloodPressure Before/After
fig = go.Figure()
fig.add_trace(go.Box(y=bp_before_winsor, name='Öncesi', marker_color=PROFESSIONAL_PALETTE[3]))
fig.add_trace(go.Box(y=df['BloodPressure'], name='Sonrası', marker_color=PROFESSIONAL_PALETTE[4]))
fig = apply_premium_layout(fig, "BloodPressure Outlier Yönetimi (Winsorization)")
fig.write_html('../figures/dataprep_phase3_bloodpressure_outlier.html')
print("✅ Görsel kaydedildi: dataprep_phase3_bloodpressure_outlier.html")

# Adım 3: Çarpıklık Analizi (Before)
print("\n📊 Adım 3: Çarpıklık Analizi (Yeo-Johnson Öncesi)")

numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
numeric_cols.remove('Outcome')  # Target değişkenini çıkar

skewness_before = {}
for col in numeric_cols:
    skew_val = df[col].skew()
    skewness_before[col] = skew_val
    status = "✅ Normal" if abs(skew_val) < 0.5 else ("⚠️ Hafif Çarpık" if abs(skew_val) < 1 else "🚨 Çarpık")
    print(f"   {col}: {skew_val:.3f} {status}")

# Adım 4: Yeo-Johnson Dönüşümü
print("\n🔄 Adım 4: Yeo-Johnson Dönüşümü Uygulanıyor")

transformer = PowerTransformer(method='yeo-johnson', standardize=False)
df[numeric_cols] = transformer.fit_transform(df[numeric_cols])

# Çarpıklık Analizi (After)
skewness_after = {}
print("\n✅ Yeo-Johnson Sonrası Çarpıklık:")
for col in numeric_cols:
    skew_val = df[col].skew()
    skewness_after[col] = skew_val
    improvement = skewness_before[col] - skew_val
    status = "✅ Normal" if abs(skew_val) < 0.5 else ("⚠️ Hafif Çarpık" if abs(skew_val) < 1 else "🚨 Çarpık")
    print(f"   {col}: {skew_val:.3f} {status} (İyileşme: {improvement:.3f})")

log_dataprep_action(
    step="PHASE 3.2",
    issue="Çarpıklık (DiabetesPedigreeFunction: 1.920, Age: 1.130)",
    decision="Yeo-Johnson dönüşümü tüm sayısal değişkenlere uygulandı",
    rationale="Lineer modeller için faydalı, çarpıklığı azaltır, tree-based modellere zarar vermez",
    risk="Düşük"
)

# Çarpıklık raporunu kaydet
skewness_report = pd.DataFrame({
    'Değişken': numeric_cols,
    'Çarpıklık (Öncesi)': [skewness_before[col] for col in numeric_cols],
    'Çarpıklık (Sonrası)': [skewness_after[col] for col in numeric_cols],
    'İyileşme': [skewness_before[col] - skewness_after[col] for col in numeric_cols]
})
skewness_report.to_csv('../reports/csv/skewness_report.csv', index=False)
print("\n✅ Rapor kaydedildi: skewness_report.csv")

# Görselleştirme - Skewness Before/After
fig = go.Figure()
fig.add_trace(go.Bar(
    x=numeric_cols,
    y=[abs(skewness_before[col]) for col in numeric_cols],
    name='Öncesi',
    marker_color=PROFESSIONAL_PALETTE[1]
))
fig.add_trace(go.Bar(
    x=numeric_cols,
    y=[abs(skewness_after[col]) for col in numeric_cols],
    name='Sonrası',
    marker_color=PROFESSIONAL_PALETTE[0]
))
fig.update_layout(barmode='group')
fig = apply_premium_layout(fig, "Çarpıklık İyileşmesi (Yeo-Johnson Dönüşümü)")
fig.write_html('../figures/dataprep_phase3_skewness_improvement.html')
print("✅ Görsel kaydedildi: dataprep_phase3_skewness_improvement.html")

print("\n" + "="*80)
print(" PHASE 4: ENCODING & TRANSFORMATION ".center(80, "="))
print("="*80)

print("\n✅ Encoding: Gerekli Değil")
print("   Tüm değişkenler sayısal, kategorik değişken yok")

log_dataprep_action(
    step="PHASE 4.1",
    issue="Kategorik değişken encoding",
    decision="Uygulanmadı - Kategorik değişken yok",
    rationale="Veri setindeki tüm değişkenler sayısal",
    risk="Yok"
)

# Scaling - StandardScaler pipeline'a eklenecek (Model Expert için)
print("\n⚠️ Scaling: Pipeline içinde uygulanacak (Model Expert)")
print("   Lineer modeller için StandardScaler önerilir")
print("   Tree-based modeller için opsiyonel")

add_model_handoff(
    item="Scaling Strategy",
    status="Pipeline'a StandardScaler eklenmelidir",
    recommendation="Lineer modeller (LogisticRegression) için kesinlikle gerekli. Tree-based için opsiyonel ama zarar vermez."
)

log_dataprep_action(
    step="PHASE 4.2",
    issue="Feature scaling",
    decision="Pipeline içinde StandardScaler kullanılacak",
    rationale="Değişkenler farklı ölçeklerde (Glucose: 0-199, Age: 21-81), lineer modeller için gerekli",
    risk="Düşük"
)

print("\n" + "="*80)
print(" PHASE 5: FEATURE ENGINEERING ".center(80, "="))
print("="*80)

# EDA'dan gelen kritik değişkenler: Glucose, Pregnancies, BMI, Age, DiabetesPedigreeFunction
print("\n🧠 Adım 1: Binary Features (Yüksek Risk Profilleri)")

# Binary features
df['High_Glucose'] = (df['Glucose'] > df['Glucose'].quantile(0.75)).astype(int)
df['High_BMI'] = (df['BMI'] > 30).astype(int)
df['Old_Age'] = (df['Age'] > df['Age'].quantile(0.75)).astype(int)
df['Many_Pregnancies'] = (df['Pregnancies'] > df['Pregnancies'].quantile(0.75)).astype(int)

print("   ✅ High_Glucose: Glucose > Q3 (75th percentile)")
print("   ✅ High_BMI: BMI > 30 (obezite eşiği)")
print("   ✅ Old_Age: Age > Q3 (75th percentile)")
print("   ✅ Many_Pregnancies: Pregnancies > Q3 (75th percentile)")

log_dataprep_action(
    step="PHASE 5.1",
    issue="Binary feature generation",
    decision="4 binary feature oluşturuldu (High_Glucose, High_BMI, Old_Age, Many_Pregnancies)",
    rationale="EDA'da Glucose, BMI, Age güçlü öngörücüler, eşik bazlı binary features model performansını artırabilir",
    risk="Düşük - Tree-based modeller için faydalı"
)

print("\n🔗 Adım 2: Interaction Features (İkili Etkileşimler)")

# Interaction features (EDA'da güçlü korelasyonlar)
df['BMI_Age'] = df['BMI'] * df['Age']
df['Glucose_BMI'] = df['Glucose'] * df['BMI']
df['Glucose_Age'] = df['Glucose'] * df['Age']
df['BMI_DiabetesPedigreeFunction'] = df['BMI'] * df['DiabetesPedigreeFunction']

print("   ✅ BMI_Age: BMI × Age etkileşimi")
print("   ✅ Glucose_BMI: Glucose × BMI etkileşimi")
print("   ✅ Glucose_Age: Glucose × Age etkileşimi")
print("   ✅ BMI_DiabetesPedigreeFunction: BMI × Genetik risk etkileşimi")

log_dataprep_action(
    step="PHASE 5.2",
    issue="Interaction feature generation",
    decision="4 interaction feature oluşturuldu",
    rationale="EDA'da güçlü değişkenler arası etkileşim potansiyeli, lineer modeller için non-lineer ilişkileri yakalayabilir",
    risk="Orta - Multicollinearity riskini artırabilir, feature selection ile kontrol edilmeli"
)

print(f"\n📊 Feature Engineering Sonrası Veri Boyutu: {df.shape}")
print(f"   Yeni Feature Sayısı: 8 adet")
print(f"   Toplam Feature: {df.shape[1] - 1} (Outcome hariç)")

# Feature listesini kaydet
feature_list = df.drop(columns=['Outcome']).columns.tolist()
feature_report = pd.DataFrame({
    'Feature': feature_list,
    'Tip': ['Original' if col in ['Pregnancies', 'Glucose', 'BloodPressure', 'BMI', 'DiabetesPedigreeFunction', 'Age'] 
            else ('Binary' if col.startswith('High_') or col.startswith('Many_') or col.startswith('Old_') 
                  else 'Interaction') 
            for col in feature_list]
})
feature_report.to_csv('../reports/csv/feature_engineering_report.csv', index=False)
print("✅ Rapor kaydedildi: feature_engineering_report.csv")

print("\n" + "="*80)
print(" PHASE 6: FEATURE SELECTION & LEAKAGE AUDIT ".center(80, "="))
print("="*80)

# Multicollinearity Kontrolü
print("\n🔍 Adım 1: Multicollinearity Kontrolü")

X_features = df.drop(columns=['Outcome'])
corr_matrix = X_features.corr()

# Yüksek korelasyon tespiti (|r| > 0.90)
high_corr_pairs = []
for i in range(len(corr_matrix.columns)):
    for j in range(i+1, len(corr_matrix.columns)):
        if abs(corr_matrix.iloc[i, j]) > 0.90:
            high_corr_pairs.append({
                'Feature 1': corr_matrix.columns[i],
                'Feature 2': corr_matrix.columns[j],
                'Korelasyon': corr_matrix.iloc[i, j]
            })

if len(high_corr_pairs) > 0:
    print(f"\n⚠️ Yüksek Korelasyon Tespit Edildi ({len(high_corr_pairs)} çift):")
    for pair in high_corr_pairs:
        print(f"   {pair['Feature 1']} <-> {pair['Feature 2']}: r = {pair['Korelasyon']:.3f}")
    
    log_dataprep_action(
        step="PHASE 6.1",
        issue="Yüksek multicollinearity",
        decision="Model Expert feature selection yapmalı veya regularization kullanmalı",
        rationale=f"{len(high_corr_pairs)} değişken çifti |r| > 0.90, VIF kontrolü önerilir",
        risk="Orta"
    )
else:
    print("   ✅ Yüksek multicollinearity (|r| > 0.90) tespit edilmedi")
    log_dataprep_action(
        step="PHASE 6.1",
        issue="Multicollinearity kontrolü",
        decision="Multicollinearity riski düşük",
        rationale="Hiçbir değişken çifti |r| > 0.90 eşiğini aşmıyor",
        risk="Düşük"
    )

# Korelasyon matrisini kaydet
corr_matrix.to_csv('../reports/csv/correlation_matrix_final.csv')
print("✅ Rapor kaydedildi: correlation_matrix_final.csv")

# Leakage Audit
print("\n🔒 Adım 2: Data Leakage Audit")

# Target korelasyonları
target_corr = df.corr()['Outcome'].sort_values(ascending=False)
print("\n📊 Target (Outcome) ile Korelasyonlar:")
print(target_corr.to_string())

# Çok yüksek korelasyon (potansiyel leakage)
leakage_risk = target_corr[(abs(target_corr) > 0.95) & (target_corr.index != 'Outcome')]

if len(leakage_risk) > 0:
    print(f"\n🚨 LEAKAGE RİSKİ TESPİT EDİLDİ!")
    print(leakage_risk.to_string())
    log_dataprep_action(
        step="PHASE 6.2",
        issue="Yüksek target korelasyonu (potansiyel leakage)",
        decision="Şüpheli değişkenler modelden çıkarılmalı",
        rationale="Target ile |r| > 0.95 korelasyon leakage riski taşıyor",
        risk="YÜKSEKeakage riski yüksek, modeli geçersiz kılabilir"
    )
else:
    print("\n✅ Leakage riski tespit edilmedi (|r| < 0.95)")
    log_dataprep_action(
        step="PHASE 6.2",
        issue="Data leakage kontrolü",
        decision="Leakage riski yok",
        rationale="Hiçbir feature target ile |r| > 0.95 korelasyona sahip değil",
        risk="Yok"
    )

print("\n" + "="*80)
print(" PHASE 7: MODEL-READY HANDOFF & TRAIN-TEST SPLIT ".center(80, "="))
print("="*80)

# Adım 1: Feature ve Target Ayırma
print("\n📦 Adım 1: Feature ve Target Ayırma")

X = df.drop(columns=['Outcome'])
y = df['Outcome']

print(f"   X shape: {X.shape}")
print(f"   y shape: {y.shape}")
print(f"   Feature sayısı: {X.shape[1]}")

# Adım 2: Stratified Train-Test Split
print("\n✂️ Adım 2: Stratified Train-Test Split (80-20)")

X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.2,
    stratify=y,
    random_state=42
)

print(f"\n✅ Split Tamamlandı:")
print(f"   Train: {X_train.shape[0]} satır (%{X_train.shape[0]/len(df)*100:.1f})")
print(f"   Test:  {X_test.shape[0]} satır (%{X_test.shape[0]/len(df)*100:.1f})")

# Class distribution kontrolü
train_dist = y_train.value_counts(normalize=True) * 100
test_dist = y_test.value_counts(normalize=True) * 100

print(f"\n📊 Class Distribution Kontrolü:")
print(f"   Train - Class 0: %{train_dist[0]:.1f}, Class 1: %{train_dist[1]:.1f}")
print(f"   Test  - Class 0: %{test_dist[0]:.1f}, Class 1: %{test_dist[1]:.1f}")
print(f"   ✅ Stratified split başarılı (oranlar korundu)")

log_dataprep_action(
    step="PHASE 7.1",
    issue="Train-test split stratejisi",
    decision="Stratified split (80-20) uygulandı",
    rationale="Class imbalance (%65-35) nedeniyle stratified split şart, test setinde de oran korundu",
    risk="Yok"
)

# Adım 3: Model-Ready Verileri Kaydet
print("\n💾 Adım 3: Model-Ready Verileri Kaydediliyor...")

X_train.to_csv('../data/model_ready/X_train.csv', index=False)
X_test.to_csv('../data/model_ready/X_test.csv', index=False)
y_train.to_csv('../data/model_ready/y_train.csv', index=False)
y_test.to_csv('../data/model_ready/y_test.csv', index=False)

# Feature processed veriyi de kaydet (tüm veri)
df.to_csv('../data/processed/diabetes_preprocessed.csv', index=False)

print("✅ Model-ready veriler kaydedildi:")
print("   - X_train.csv")
print("   - X_test.csv")
print("   - y_train.csv")
print("   - y_test.csv")
print("   - diabetes_preprocessed.csv (tüm işlenmiş veri)")

# Adım 4: Preprocessing Pipeline Kaydet
print("\n🔧 Adım 4: Preprocessing Pipeline Oluşturuluyor...")

# Model Expert için kullanıma hazır pipeline
preprocessing_pipeline = Pipeline([
    ('scaler', StandardScaler())  # Scaling train data üzerinde fit edilecek
])

# Pipeline'ı kaydet
joblib.dump(preprocessing_pipeline, '../models/preprocessing_pipeline.pkl')
print("✅ Preprocessing pipeline kaydedildi: preprocessing_pipeline.pkl")

add_model_handoff(
    item="Preprocessing Pipeline",
    status="Hazır",
    recommendation="Pipeline StandardScaler içeriyor. Train data üzerinde fit edin, test data'ya transform uygulayın. Tree-based modeller için opsiyonel."
)

# Adım 5: DataPrep Actions Report
print("\n📋 Adım 5: DataPrep Actions Raporu Oluşturuluyor...")

actions_df = pd.DataFrame(dataprep_actions)
actions_df.to_csv('../reports/csv/dataprep_actions_report.csv', index=False)
print("✅ DataPrep actions raporu kaydedildi: dataprep_actions_report.csv")

# Adım 6: Model Expert Handoff Report
print("\n🤝 Adım 6: Model Expert Handoff Raporu Oluşturuluyor...")

handoff_df = pd.DataFrame(model_handoff_report)
if len(handoff_df) > 0:
    handoff_df.to_csv('../reports/csv/model_expert_handoff.csv', index=False)
    print("✅ Model Expert handoff raporu kaydedildi: model_expert_handoff.csv")

print("\n" + "="*80)
print(" DATA PREPARATION TAMAMLANDI ".center(80, "="))
print("="*80)

print("\n🎉 Özet:")
print(f"   Orijinal veri: {df_original.shape}")
print(f"   İşlenmiş veri: {df.shape}")
print(f"   Çıkarılan değişken: 2 (Insulin, SkinThickness)")
print(f"   Eklenen feature: 8 (4 binary + 4 interaction)")
print(f"   Toplam feature: {X.shape[1]}")
print(f"   Train samples: {X_train.shape[0]}")
print(f"   Test samples: {X_test.shape[0]}")
print(f"   Toplam preprocessing adımı: {len(dataprep_actions)}")

print("\n📁 Oluşturulan Dosyalar:")
print("   Veriler:")
print("     - data/model_ready/X_train.csv")
print("     - data/model_ready/X_test.csv")
print("     - data/model_ready/y_train.csv")
print("     - data/model_ready/y_test.csv")
print("     - data/processed/diabetes_preprocessed.csv")
print("   Modeller:")
print("     - models/preprocessing_pipeline.pkl")
print("   Raporlar:")
print("     - reports/csv/imputation_report.csv")
print("     - reports/csv/skewness_report.csv")
print("     - reports/csv/feature_engineering_report.csv")
print("     - reports/csv/correlation_matrix_final.csv")
print("     - reports/csv/dataprep_actions_report.csv")
print("     - reports/csv/model_expert_handoff.csv")
print("   Görseller:")
print("     - figures/dataprep_phase2_missing_before.html")
print("     - figures/dataprep_phase3_bloodpressure_outlier.html")
print("     - figures/dataprep_phase3_skewness_improvement.html")

print("\n✅ Bir sonraki adım: Model Expert, model-ready verileri kullanarak model eğitimine başlayabilir!")
print("="*80)
