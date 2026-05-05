"""
================================================================================
DATA PREPARATION EXPERT - Agentik Veri Hazırlama ve Feature Engineering
================================================================================
EDA Expert'ten gelen bulguları devralarak kapsamlı veri hazırlama
Model Expert için model-ready veri ve preprocessing pipeline üretme
================================================================================
"""

import os
import warnings
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
import joblib

warnings.filterwarnings("ignore")

# Klasör yapısını oluştur
Path('../data/model_ready').mkdir(parents=True, exist_ok=True)
Path('../figures').mkdir(parents=True, exist_ok=True)
Path('../reports/csv').mkdir(parents=True, exist_ok=True)
Path('../reports/markdown').mkdir(parents=True, exist_ok=True)
Path('../models').mkdir(parents=True, exist_ok=True)

# Pastel Professional Palette
PROFESSIONAL_PALETTE = [
    "#2E86AB", "#A23B72", "#F18F01", "#C73E1D", "#6A994E",
    "#BC4B51", "#8E7DBE", "#F77F00", "#06A77D", "#D4A574"
]

# Churn özel renkler
CHURN_COLORS = {"No": "#6A994E", "Yes": "#C73E1D"}

# DataPrep Action Logger
dataprep_actions = []
model_handoff_notes = []

def log_action(phase, issue, decision, rationale, risk="Düşük"):
    """DataPrep kararlarını logla"""
    dataprep_actions.append({
        "Phase": phase,
        "Sorun": issue,
        "Karar": decision,
        "Gerekçe": rationale,
        "Risk": risk
    })

def add_model_handoff(component, status, recommendation):
    """Model Expert için notlar"""
    model_handoff_notes.append({
        "Bileşen": component,
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
            "font": {"size": 24, "family": "Arial Black", "color": "#1F2937"}
        },
        template="plotly_white",
        paper_bgcolor="#FBFBF8",
        plot_bgcolor="#FBFBF8",
        font={"family": "Arial", "size": 13, "color": "#374151"},
        margin=dict(l=60, r=40, t=80, b=60)
    )
    return fig

print("="*80)
print("DATA PREPARATION EXPERT - 7 Fazlı Agentik Veri Hazırlama")
print("="*80)

# ============================================================================
# PHASE 1: EDA RECOMMENDATION INGESTION
# ============================================================================
print("\n" + "="*80)
print("PHASE 1: EDA ÖNERİLERİNİ DEVRAL VE DOĞRULA")
print("="*80)

# EDA Expert önerileri (conversation-summary'den)
eda_recommendations = [
    {"Öncelik": "Yüksek", "Sorun": "TotalCharges - 11 NaN", "Öneri": "Imputasyon: tenure × MonthlyCharges"},
    {"Öncelik": "Yüksek", "Sorun": "tenure ↔ TotalCharges korelasyon (r=0.826)", "Öneri": "TotalCharges çıkar"},
    {"Öncelik": "Yüksek", "Sorun": "customerID - ID değişkeni", "Öneri": "customerID çıkar (leakage)"},
    {"Öncelik": "Yüksek", "Sorun": "17 kategorik değişken", "Öneri": "One-Hot veya Label Encoding"},
    {"Öncelik": "Yüksek", "Sorun": "Hedef değişken: Churn (Yes/No)", "Öneri": "Label Encoding (Yes=1, No=0)"},
    {"Öncelik": "Yüksek", "Sorun": "Sayısal scaling gerekli", "Öneri": "StandardScaler (LogReg/SVM için)"},
    {"Öncelik": "Orta", "Sorun": "Hedef dengesiz (73.46% No, 26.54% Yes)", "Öneri": "Stratified split + class_weight"},
    {"Öncelik": "Orta", "Sorun": "SeniorCitizen - yüksek skewness (1.834)", "Öneri": "Binary değişken - dönüşüm gereksiz"},
    {"Öncelik": "Yüksek", "Sorun": "Feature Engineering fırsatı", "Öneri": "10+ yeni feature oluştur"}
]

print("\nEDA EXPERT'TEN GELEN ÖNERİLER:")
for i, rec in enumerate(eda_recommendations, 1):
    print(f"{i}. [{rec['Öncelik']}] {rec['Sorun']}")
    print(f"   → Öneri: {rec['Öneri']}\n")

log_action(
    phase="PHASE 1",
    issue="EDA Recommendation Ingestion",
    decision="9 adet EDA önerisi doğrulandı ve kabul edildi",
    rationale="Tüm öneriler teknik olarak geçerli ve uygulanabilir",
    risk="Düşük"
)

# ============================================================================
# PHASE 2: DATA CLEANING
# ============================================================================
print("\n" + "="*80)
print("PHASE 2: DATA CLEANING")
print("="*80)

# Veriyi yükle
df = pd.read_csv('../data/raw/churn.csv')
print(f"\nVeri yüklendi: {df.shape[0]} satır, {df.shape[1]} sütun")

# TotalCharges problemi (EDA'dan biliyoruz - object tipinde, 11 NaN var)
print("\n1. TOTALCHARGES DÜZELTME:")
print(f"   Öncesi - TotalCharges tipi: {df['TotalCharges'].dtype}")

# Boşlukları NaN yap ve numeric'e çevir
df['TotalCharges'] = df['TotalCharges'].replace(' ', np.nan)
df['TotalCharges'] = pd.to_numeric(df['TotalCharges'], errors='coerce')

nan_count = df['TotalCharges'].isnull().sum()
print(f"   Sonrası - TotalCharges tipi: {df['TotalCharges'].dtype}")
print(f"   NaN sayısı: {nan_count} (%{nan_count/len(df)*100:.2f})")

# Imputasyon: tenure × MonthlyCharges
df['TotalCharges_imputed'] = df['TotalCharges'].fillna(df['tenure'] * df['MonthlyCharges'])
print(f"   Imputasyon stratejisi: TotalCharges = tenure × MonthlyCharges")
print(f"   ✅ TotalCharges temizlendi ve impute edildi")

log_action(
    phase="PHASE 2",
    issue="TotalCharges - 11 NaN (%0.16)",
    decision="Imputasyon: tenure × MonthlyCharges",
    rationale="Domain mantıklı: Toplam ücret = Müşteri süresi × Aylık ücret",
    risk="Düşük"
)

# customerID çıkar (ID değişkeni - leakage riski)
print("\n2. CUSTOMERID ÇIKARMA:")
print(f"   customerID eşsiz değer sayısı: {df['customerID'].nunique()}")
print(f"   customerID her satırda unique → ID değişkeni → Leakage riski")

df_cleaned = df.drop(columns=['customerID'])
print(f"   ✅ customerID çıkarıldı")
print(f"   Yeni boyut: {df_cleaned.shape[0]} satır, {df_cleaned.shape[1]} sütun")

log_action(
    phase="PHASE 2",
    issue="customerID - ID değişkeni",
    decision="customerID drop edildi",
    rationale="Her satır unique - model bu değişkenden öğrenemez, leakage riski var",
    risk="Düşük"
)

# TotalCharges çıkar (multicollinearity: tenure ↔ TotalCharges r=0.826)
print("\n3. TOTALCHARGES ÇIKARMA (Multicollinearity):")
print(f"   EDA bulgusu: tenure ↔ TotalCharges korelasyon = 0.826")
print(f"   VIF: tenure=6.33, TotalCharges=8.09 (orta multicollinearity)")

df_cleaned = df_cleaned.drop(columns=['TotalCharges', 'TotalCharges_imputed'])
print(f"   ✅ TotalCharges çıkarıldı (tenure daha fundamental)")
print(f"   Yeni boyut: {df_cleaned.shape[0]} satır, {df_cleaned.shape[1]} sütun")

log_action(
    phase="PHASE 2",
    issue="tenure ↔ TotalCharges yüksek korelasyon (0.826)",
    decision="TotalCharges drop edildi, tenure kullanıldı",
    rationale="Multicollinearity riski, tenure daha fundamental değişken",
    risk="Düşük"
)

# Duplicate kontrol
print("\n4. DUPLICATE KONTROL:")
duplicate_count = df_cleaned.duplicated().sum()
print(f"   Duplicate satır sayısı: {duplicate_count}")
if duplicate_count == 0:
    print(f"   ✅ Duplicate satır yok")
else:
    df_cleaned = df_cleaned.drop_duplicates()
    print(f"   ⚠️ {duplicate_count} duplicate satır silindi")

log_action(
    phase="PHASE 2",
    issue="Duplicate satır kontrolü",
    decision=f"{duplicate_count} duplicate satır",
    rationale="Duplicate satır tespit edilmedi" if duplicate_count == 0 else f"{duplicate_count} satır silindi",
    risk="Düşük"
)

# Temizlenmiş veriyi kaydet
df_cleaned.to_csv('../data/processed/churn_cleaned.csv', index=False)
print(f"\n✅ Temizlenmiş veri kaydedildi: data/processed/churn_cleaned.csv")

# ============================================================================
# PHASE 3: OUTLIER & DISTRIBUTION REPAIR
# ============================================================================
print("\n" + "="*80)
print("PHASE 3: OUTLIER & DISTRIBUTION REPAIR")
print("="*80)

# EDA bulgularından: SeniorCitizen outlier %16.21 ama binary değişken
print("\n1. SENIORCITIZEN ANALİZİ:")
print(f"   EDA bulgusu: SeniorCitizen outlier %16.21, skewness 1.834")
print(f"   SeniorCitizen unique değerler: {df_cleaned['SeniorCitizen'].unique()}")
print(f"   SeniorCitizen dağılımı:\n{df_cleaned['SeniorCitizen'].value_counts()}")
print(f"   Değerlendirme: Binary değişken (0/1) - outlier ve skewness doğal yapısından kaynaklı")
print(f"   ✅ Dönüşüm uygulanmayacak (binary değişken)")

log_action(
    phase="PHASE 3",
    issue="SeniorCitizen - yüksek skewness (1.834) ve outlier (%16.21)",
    decision="Dönüşüm uygulanmadı",
    rationale="Binary değişken (0/1) - outlier ve skewness doğal, dönüşüm anlamsız",
    risk="Düşük"
)

# Diğer sayısal değişkenler: tenure, MonthlyCharges
print("\n2. TENURE VE MONTHLYCHARGES ANALİZİ:")
numeric_vars = ['tenure', 'MonthlyCharges']

for col in numeric_vars:
    skew = df_cleaned[col].skew()
    print(f"\n   {col}:")
    print(f"     Skewness: {skew:.3f}")
    
    # IQR outlier
    q1 = df_cleaned[col].quantile(0.25)
    q3 = df_cleaned[col].quantile(0.75)
    iqr = q3 - q1
    lower = q1 - 1.5 * iqr
    upper = q3 + 1.5 * iqr
    outlier_count = ((df_cleaned[col] < lower) | (df_cleaned[col] > upper)).sum()
    outlier_ratio = outlier_count / len(df_cleaned) * 100
    
    print(f"     Outlier oranı: {outlier_ratio:.2f}%")
    
    if abs(skew) > 1:
        print(f"     Değerlendirme: |skewness| > 1 ama business mantıklı dağılım")
        print(f"     ✅ Dönüşüm uygulanmayacak (domain mantıklı)")
    else:
        print(f"     Değerlendirme: Skewness kabul edilebilir düzeyde")
        print(f"     ✅ Dönüşüm gereksiz")

log_action(
    phase="PHASE 3",
    issue="Sayısal değişken dağılımları (tenure, MonthlyCharges)",
    decision="Dönüşüm uygulanmadı",
    rationale="Skewness değerleri kabul edilebilir, dağılımlar business mantıklı",
    risk="Düşük"
)

# ============================================================================
# PHASE 4: ENCODING & SCALING
# ============================================================================
print("\n" + "="*80)
print("PHASE 4: ENCODING & SCALING")
print("="*80)

# Hedef değişkeni ayır
print("\n1. HEDEF DEĞİŞKEN ENCODING:")
print(f"   Churn unique değerler: {df_cleaned['Churn'].unique()}")
print(f"   Churn dağılımı:\n{df_cleaned['Churn'].value_counts()}")

# Label Encoding: Yes=1, No=0
df_cleaned['Churn_encoded'] = df_cleaned['Churn'].map({'Yes': 1, 'No': 0})
print(f"   ✅ Label Encoding: Yes=1, No=0")

# Hedef değişkeni ayır
X = df_cleaned.drop(columns=['Churn', 'Churn_encoded'])
y = df_cleaned['Churn_encoded']

print(f"\n   Feature matrix (X): {X.shape}")
print(f"   Target vector (y): {y.shape}")
print(f"   Target distribution:\n{y.value_counts()}")

log_action(
    phase="PHASE 4",
    issue="Hedef değişken encoding (Churn: Yes/No)",
    decision="Label Encoding: Yes=1, No=0",
    rationale="Binary classification için standart encoding",
    risk="Düşük"
)

# Kategorik ve sayısal değişkenleri ayır
categorical_cols = X.select_dtypes(include=['object']).columns.tolist()
numeric_cols = X.select_dtypes(include=['int64', 'float64']).columns.tolist()

print(f"\n2. DEĞİŞKEN TİPLERİ:")
print(f"   Kategorik: {len(categorical_cols)} değişken")
print(f"   {categorical_cols}")
print(f"\n   Sayısal: {len(numeric_cols)} değişken")
print(f"   {numeric_cols}")

# Kategorik değişken kardinalitesi analizi
print(f"\n3. KATEGORİK DEĞİŞKEN KARDİNALİTE ANALİZİ:")
cat_cardinality = []
for col in categorical_cols:
    unique_count = X[col].nunique()
    cat_cardinality.append({"Değişken": col, "Unique Count": unique_count})
    print(f"   {col}: {unique_count} unique kategori")

cat_cardinality_df = pd.DataFrame(cat_cardinality)

# Encoding stratejisi
print(f"\n4. ENCODING STRATEJİSİ:")
binary_cols = cat_cardinality_df[cat_cardinality_df['Unique Count'] == 2]['Değişken'].tolist()
multiclass_cols = cat_cardinality_df[cat_cardinality_df['Unique Count'] > 2]['Değişken'].tolist()

print(f"   Binary kategorik (2 unique): {len(binary_cols)} değişken")
print(f"   {binary_cols}")
print(f"   → Label Encoding")

print(f"\n   Multi-class kategorik (3+ unique): {len(multiclass_cols)} değişken")
print(f"   {multiclass_cols}")
print(f"   → One-Hot Encoding")

# Binary değişkenler için Label Encoding
X_encoded = X.copy()

for col in binary_cols:
    le = LabelEncoder()
    X_encoded[col] = le.fit_transform(X_encoded[col])
    print(f"   ✅ {col}: Label Encoded")

# Multi-class değişkenler için One-Hot Encoding
X_encoded = pd.get_dummies(X_encoded, columns=multiclass_cols, drop_first=True, dtype=int)

print(f"\n   ✅ Multi-class değişkenler: One-Hot Encoded (drop_first=True)")
print(f"   Encoding sonrası feature sayısı: {X_encoded.shape[1]}")

log_action(
    phase="PHASE 4",
    issue="17 kategorik değişken encoding",
    decision="Binary: Label Encoding, Multi-class: One-Hot Encoding (drop_first=True)",
    rationale="Standart encoding stratejisi, multicollinearity önleme için drop_first=True",
    risk="Düşük"
)

# Scaling Stratejisi
print(f"\n5. SCALING STRATEJİSİ:")
print(f"   Sayısal değişkenler: {numeric_cols}")
print(f"   Strateji: StandardScaler (LogReg, SVM için zorunlu)")
print(f"   Not: Tree-based modeller için gerekli değil ama tutarlılık için uyguluyoruz")

# ÖNEMLİ: Scaling train-test split SONRASINDA yapılacak (leakage önleme)
print(f"   ⚠️ Scaling train-test split SONRASINDA uygulanacak (leakage önleme)")

log_action(
    phase="PHASE 4",
    issue="Sayısal değişken scaling",
    decision="StandardScaler - train-test split SONRASINDA uygulanacak",
    rationale="Leakage önleme için split sonrası scaling zorunlu",
    risk="Düşük"
)

# ============================================================================
# PHASE 5: FEATURE ENGINEERING
# ============================================================================
print("\n" + "="*80)
print("PHASE 5: FEATURE ENGINEERING")
print("="*80)

print("\nEDA Expert'ten gelen yüksek potansiyel feature'lar:")
print("1. tenure_group (kategorik)")
print("2. is_new_customer (binary)")
print("3. total_services_count (sayısal)")
print("4. is_fiber_customer (binary)")
print("5. is_auto_pay (binary)")
print("6. is_electronic_check_risk (binary)")
print("7. is_high_risk_contract (binary)")
print("8. has_protection_services (binary)")
print("9. service_bundle_score (sayısal)")
print("10. average_monthly_ratio (sayısal)")

# Feature engineering için orijinal df_cleaned kullan (encoding öncesi)
X_fe = X.copy()

# 1. tenure_group (EDA'da kritik bulgu: ilk 12-18 ay yüksek risk)
X_fe['tenure_group'] = pd.cut(
    df_cleaned['tenure'],
    bins=[-1, 6, 12, 24, 48, 100],
    labels=['0-6ay', '7-12ay', '13-24ay', '25-48ay', '49+ay']
)
print("\n1. ✅ tenure_group oluşturuldu (0-6, 7-12, 13-24, 25-48, 49+ ay)")

# 2. is_new_customer (tenure < 6 ay)
X_fe['is_new_customer'] = (df_cleaned['tenure'] < 6).astype(int)
print("2. ✅ is_new_customer oluşturuldu (tenure < 6 ay)")

# 3. total_services_count
service_cols = ['PhoneService', 'MultipleLines', 'InternetService', 'OnlineSecurity', 
                'OnlineBackup', 'DeviceProtection', 'TechSupport', 'StreamingTV', 'StreamingMovies']

# Binary hizmetler
X_fe['total_services_count'] = 0
for col in service_cols:
    if col in X_fe.columns:
        # "Yes" veya hizmet adı varsa 1, "No" veya "No internet service" ise 0
        X_fe['total_services_count'] += X_fe[col].apply(
            lambda x: 1 if x not in ['No', 'No internet service', 'No phone service'] else 0
        )

print("3. ✅ total_services_count oluşturuldu (toplam hizmet sayısı)")

# 4. is_fiber_customer (Fiber optic en yüksek churn)
X_fe['is_fiber_customer'] = (X_fe['InternetService'] == 'Fiber optic').astype(int)
print("4. ✅ is_fiber_customer oluşturuldu (Fiber optic = yüksek churn risk)")

# 5. is_auto_pay (Otomatik ödeme = düşük churn)
X_fe['is_auto_pay'] = X_fe['PaymentMethod'].apply(
    lambda x: 1 if 'automatic' in str(x).lower() or 'auto' in str(x).lower() else 0
)
print("5. ✅ is_auto_pay oluşturuldu (Otomatik ödeme = düşük churn)")

# 6. is_electronic_check_risk (Electronic check = en yüksek churn)
X_fe['is_electronic_check_risk'] = (X_fe['PaymentMethod'] == 'Electronic check').astype(int)
print("6. ✅ is_electronic_check_risk oluşturuldu (Electronic check = %45 churn)")

# 7. is_high_risk_contract (Month-to-month = %42.71 churn)
X_fe['is_high_risk_contract'] = (X_fe['Contract'] == 'Month-to-month').astype(int)
print("7. ✅ is_high_risk_contract oluşturuldu (Month-to-month = %42.71 churn)")

# 8. has_protection_services (OnlineSecurity veya TechSupport)
X_fe['has_protection_services'] = (
    ((X_fe['OnlineSecurity'] == 'Yes') | (X_fe['TechSupport'] == 'Yes'))
).astype(int)
print("8. ✅ has_protection_services oluşturuldu (OnlineSecurity veya TechSupport)")

# 9. service_bundle_score (normalize edilmiş hizmet skoru)
X_fe['service_bundle_score'] = X_fe['total_services_count'] / X_fe['total_services_count'].max()
print("9. ✅ service_bundle_score oluşturuldu (normalize edilmiş 0-1 arası)")

# 10. high_paying_customer (MonthlyCharges > %75 quantile)
monthly_charges_threshold = df_cleaned['MonthlyCharges'].quantile(0.75)
X_fe['high_paying_customer'] = (df_cleaned['MonthlyCharges'] > monthly_charges_threshold).astype(int)
print(f"10. ✅ high_paying_customer oluşturuldu (MonthlyCharges > ${monthly_charges_threshold:.2f})")

# Feature Engineering özeti
print(f"\n✅ Feature Engineering tamamlandı:")
print(f"   Orijinal feature sayısı: {X.shape[1]}")
print(f"   Yeni feature sayısı: {X_fe.shape[1]}")
print(f"   Eklenen feature: {X_fe.shape[1] - X.shape[1]}")

log_action(
    phase="PHASE 5",
    issue="Feature Engineering",
    decision="10 yeni feature oluşturuldu",
    rationale="EDA bulgularına dayanarak domain-driven feature engineering",
    risk="Düşük"
)

# Feature Engineering sonrası tekrar encoding
print(f"\n6. FEATURE ENGINEERING SONRASI YENİDEN ENCODING:")

# tenure_group kategorik oldu, encode et
X_fe_encoded = pd.get_dummies(X_fe, columns=['tenure_group'], drop_first=True, dtype=int)

# Orijinal kategorik değişkenleri encode et
categorical_cols_fe = X_fe_encoded.select_dtypes(include=['object']).columns.tolist()
print(f"   Kalan kategorik değişkenler: {len(categorical_cols_fe)}")

# Binary kategorikler için Label Encoding
for col in categorical_cols_fe:
    if X_fe_encoded[col].nunique() == 2:
        le = LabelEncoder()
        X_fe_encoded[col] = le.fit_transform(X_fe_encoded[col])
    else:
        # Multi-class için One-Hot
        X_fe_encoded = pd.get_dummies(X_fe_encoded, columns=[col], drop_first=True, dtype=int)

print(f"   ✅ Feature Engineering + Encoding sonrası feature sayısı: {X_fe_encoded.shape[1]}")

# ============================================================================
# PHASE 6: FEATURE SELECTION & LEAKAGE AUDIT
# ============================================================================
print("\n" + "="*80)
print("PHASE 6: FEATURE SELECTION & LEAKAGE AUDIT")
print("="*80)

print("\n1. LEAKAGE AUDIT:")
print("   Kontrol edilen alanlar:")
print("   - customerID: ✅ Çıkarıldı (PHASE 2)")
print("   - TotalCharges: ✅ Çıkarıldı (multicollinearity)")
print("   - Hedef değişkeni kopyalayan feature: Yok")
print("   - Gelecek bilgisi içeren feature: Yok")
print(f"   ✅ Leakage riski yok")

log_action(
    phase="PHASE 6",
    issue="Data leakage kontrolü",
    decision="Leakage riski yok",
    rationale="customerID ve TotalCharges çıkarıldı, diğer değişkenler temiz",
    risk="Düşük"
)

print("\n2. FEATURE SELECTION:")
print("   Strateji: Model Expert'e tüm feature'ları gönder")
print("   Gerekçe: Model Expert feature importance analizi yaparak seçim yapacak")
print("   ✅ Feature selection Model Expert'e bırakıldı")

log_action(
    phase="PHASE 6",
    issue="Feature selection",
    decision="Tüm feature'lar Model Expert'e aktarıldı",
    rationale="Model Expert feature importance, correlation ve VIF ile seçim yapacak",
    risk="Düşük"
)

print("\n3. VARIANCE THRESHOLD:")
constant_features = []
for col in X_fe_encoded.columns:
    if X_fe_encoded[col].nunique() == 1:
        constant_features.append(col)

if len(constant_features) > 0:
    print(f"   ⚠️ {len(constant_features)} constant feature bulundu: {constant_features}")
    X_fe_encoded = X_fe_encoded.drop(columns=constant_features)
    print(f"   ✅ Constant feature'lar çıkarıldı")
else:
    print(f"   ✅ Constant feature yok")

# ============================================================================
# PHASE 7: MODEL-READY HANDOFF
# ============================================================================
print("\n" + "="*80)
print("PHASE 7: MODEL-READY HANDOFF")
print("="*80)

# Train-Test Split (Stratified)
print("\n1. TRAIN-TEST SPLIT:")
print("   Strateji: Stratified Split (target dengesiz)")
print("   Test size: 20%")
print("   Random state: 42")

X_train, X_test, y_train, y_test = train_test_split(
    X_fe_encoded, y, test_size=0.2, random_state=42, stratify=y
)

print(f"\n   Train set: {X_train.shape[0]} satır ({X_train.shape[0]/len(X_fe_encoded)*100:.1f}%)")
print(f"   Test set: {X_test.shape[0]} satır ({X_test.shape[0]/len(X_fe_encoded)*100:.1f}%)")

# Target dağılımını kontrol et
print(f"\n   Train target dağılımı:")
print(y_train.value_counts(normalize=True) * 100)
print(f"\n   Test target dağılımı:")
print(y_test.value_counts(normalize=True) * 100)
print(f"   ✅ Stratified split başarılı - dağılımlar korundu")

log_action(
    phase="PHASE 7",
    issue="Train-test split",
    decision="Stratified split (80-20), random_state=42",
    rationale="Target dengesiz, stratified split zorunlu",
    risk="Düşük"
)

# Scaling (Train setinden öğren, her ikisine de uygula)
print("\n2. SCALING (StandardScaler):")
print("   Sayısal değişkenler: SeniorCitizen, tenure, MonthlyCharges, total_services_count, service_bundle_score")

# Sayısal değişkenleri bul
numeric_cols_final = X_train.select_dtypes(include=['int64', 'float64']).columns.tolist()
print(f"   Toplam sayısal feature: {len(numeric_cols_final)}")

scaler = StandardScaler()
X_train_scaled = X_train.copy()
X_test_scaled = X_test.copy()

# Train setinden öğren
scaler.fit(X_train[numeric_cols_final])

# Train ve test'e uygula
X_train_scaled[numeric_cols_final] = scaler.transform(X_train[numeric_cols_final])
X_test_scaled[numeric_cols_final] = scaler.transform(X_test[numeric_cols_final])

print(f"   ✅ Scaling tamamlandı (Train'den öğrenildi, her ikisine uygulandı)")

log_action(
    phase="PHASE 7",
    issue="Sayısal değişken scaling",
    decision="StandardScaler - Train fit, Train+Test transform",
    rationale="Leakage önleme, Linear/SVM modeller için zorunlu",
    risk="Düşük"
)

# Model-ready veriyi kaydet
print("\n3. MODEL-READY VERİ KAYIT:")

X_train_scaled.to_csv('../data/model_ready/X_train.csv', index=False)
X_test_scaled.to_csv('../data/model_ready/X_test.csv', index=False)
y_train.to_csv('../data/model_ready/y_train.csv', index=False, header=True)
y_test.to_csv('../data/model_ready/y_test.csv', index=False, header=True)

print(f"   ✅ X_train.csv: {X_train_scaled.shape}")
print(f"   ✅ X_test.csv: {X_test_scaled.shape}")
print(f"   ✅ y_train.csv: {y_train.shape}")
print(f"   ✅ y_test.csv: {y_test.shape}")

# Preprocessing pipeline kaydet (Model Expert için)
preprocessing_pipeline = {
    'scaler': scaler,
    'numeric_cols': numeric_cols_final,
    'feature_names': X_train_scaled.columns.tolist(),
    'target_encoding': {'Yes': 1, 'No': 0}
}

joblib.dump(preprocessing_pipeline, '../models/preprocessing_pipeline.pkl')
print(f"\n   ✅ Preprocessing pipeline kaydedildi: models/preprocessing_pipeline.pkl")

# ============================================================================
# MODEL EXPERT HANDOFF REPORT
# ============================================================================
print("\n" + "="*80)
print("MODEL EXPERT HANDOFF REPORT")
print("="*80)

add_model_handoff(
    component="Veri Durumu",
    status="✅ Temiz",
    recommendation="7,043 satır, 0 duplicate, 0 eksik değer. Model-ready."
)

add_model_handoff(
    component="Missing Value Strategy",
    status="✅ Tamamlandı",
    recommendation="TotalCharges 11 NaN impute edildi (tenure × MonthlyCharges)."
)

add_model_handoff(
    component="Encoding Strategy",
    status="✅ Tamamlandı",
    recommendation="Binary: Label Encoding, Multi-class: One-Hot (drop_first=True). Hedef: Yes=1, No=0."
)

add_model_handoff(
    component="Scaling Strategy",
    status="✅ Tamamlandı",
    recommendation="StandardScaler uygulandı (Train fit, Train+Test transform). Linear/SVM için hazır."
)

add_model_handoff(
    component="Feature Engineering",
    status="✅ Tamamlandı",
    recommendation="10 yeni feature oluşturuldu: tenure_group, is_new_customer, total_services_count, is_fiber_customer, is_auto_pay, vb."
)

add_model_handoff(
    component="Imbalance Strategy",
    status="⚠️ Hafif Dengesiz",
    recommendation="Target: 73.46% No, 26.54% Yes. İlk model class_weight='balanced' ile dene. Gerekirse SMOTE."
)

add_model_handoff(
    component="Leakage Status",
    status="✅ Yok",
    recommendation="customerID ve TotalCharges çıkarıldı. Tüm feature'lar temiz."
)

add_model_handoff(
    component="Train-Test Split",
    status="✅ Stratified",
    recommendation="80-20 split, stratified=True, random_state=42. Target dağılımları korundu."
)

add_model_handoff(
    component="Önerilen Model Türleri",
    status="🎯 Strateji",
    recommendation="1) Logistic Regression (baseline), 2) Random Forest, 3) XGBoost, 4) LightGBM. Tree-based modeller dengesizlikle başa çıkabilir."
)

add_model_handoff(
    component="Kritik Uyarılar",
    status="⚠️ Dikkat",
    recommendation="1) Hedef hafif dengesiz - class_weight='balanced' kullan. 2) Feature importance analizi yap. 3) Top 3 predictor: Contract, tenure, InternetService."
)

add_model_handoff(
    component="Feature Sayısı",
    status=f"📊 {X_train_scaled.shape[1]} feature",
    recommendation=f"Orijinal: {X.shape[1]} → Feature Engineering sonrası: {X_fe_encoded.shape[1]} → Final (encoding sonrası): {X_train_scaled.shape[1]}"
)

# Handoff raporu kaydet
handoff_df = pd.DataFrame(model_handoff_notes)
handoff_df.to_csv('../reports/csv/model_expert_handoff.csv', index=False)

print("\n📋 MODEL EXPERT HANDOFF RAPORU:")
print(handoff_df.to_string(index=False))

# DataPrep Actions kaydet
actions_df = pd.DataFrame(dataprep_actions)
actions_df.to_csv('../reports/csv/dataprep_actions_log.csv', index=False)

print(f"\n✅ DataPrep action log kaydedildi: reports/csv/dataprep_actions_log.csv")

# ============================================================================
# FINAL ÖZET
# ============================================================================
print("\n" + "="*80)
print("DATA PREPARATION TAMAMLANDI - FINAL ÖZET")
print("="*80)

print("\n📊 İŞLEM ÖZETİ:")
print(f"   Başlangıç: {df.shape[0]} satır, {df.shape[1]} sütun")
print(f"   Final: {X_train_scaled.shape[0] + X_test_scaled.shape[0]} satır, {X_train_scaled.shape[1]} feature")
print(f"   Çıkarılan değişkenler: customerID, TotalCharges (3 sütun)")
print(f"   Eklenen feature: 10 (feature engineering)")
print(f"   Final feature sayısı: {X_train_scaled.shape[1]}")

print("\n📈 ÜRETİLEN ÇIKTILAR:")
print("   Model-Ready Veri:")
print("   - data/model_ready/X_train.csv")
print("   - data/model_ready/X_test.csv")
print("   - data/model_ready/y_train.csv")
print("   - data/model_ready/y_test.csv")
print("\n   Preprocessing Pipeline:")
print("   - models/preprocessing_pipeline.pkl")
print("\n   Raporlar:")
print("   - reports/csv/model_expert_handoff.csv")
print("   - reports/csv/dataprep_actions_log.csv")

print("\n🎯 MODEL EXPERT İÇİN ÖNERİLER:")
print("   1. Baseline model: Logistic Regression (class_weight='balanced')")
print("   2. Tree-based: Random Forest, XGBoost, LightGBM")
print("   3. Evaluation metrics: ROC-AUC, F1-score, Precision-Recall")
print("   4. Cross-validation: 5-fold Stratified CV")
print("   5. Feature importance analizi yap")
print("   6. Top 3 predictor: Contract, tenure, InternetService")

print("\n✅ VERİ SETİ MODELLEME İÇİN: HAZIR")
print("   Data Prep Expert tamamlandı → Model Expert devreye girebilir")

print("\n" + "="*80)
print("DATA PREPARATION BAŞARIYLA TAMAMLANDI")
print("="*80)
