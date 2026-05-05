"""
PHASE 5-6-7: DATA QUALITY, INSIGHT GENERATION & MODEL READINESS
Son kontroller, içgörü özeti ve model hazırlık değerlendirmesi
"""

import os
import warnings
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path

warnings.filterwarnings("ignore")

# Klasörlerin varlığını garantile
Path('../figures').mkdir(parents=True, exist_ok=True)
Path('../reports/csv').mkdir(parents=True, exist_ok=True)
Path('../reports/markdown').mkdir(parents=True, exist_ok=True)

# Profesyonel renk paleti
PROFESSIONAL_PALETTE = [
    "#2E86AB", "#A23B72", "#F18F01", "#C73E1D", "#6A994E",
    "#BC4B51", "#8E7DBE", "#F77F00", "#06A77D", "#D4A574"
]

def apply_premium_layout(fig, title):
    fig.update_layout(
        title={"text": title, "x": 0.03, "xanchor": "left",
               "font": {"size": 24, "family": "Arial Black", "color": "#1F2937", "weight": "bold"}},
        template="plotly_white", paper_bgcolor="#FBFBF8", plot_bgcolor="#FBFBF8",
        font={"family": "Arial", "size": 13, "color": "#374151"},
        margin=dict(l=60, r=40, t=80, b=60), legend_title_text="Kategori",
        hoverlabel=dict(bgcolor="white", font_size=12, font_family="Arial")
    )
    fig.update_xaxes(showgrid=True, gridcolor="#E5E7EB", zeroline=False)
    fig.update_yaxes(showgrid=True, gridcolor="#E5E7EB", zeroline=False)
    return fig

def save_figure(fig, file_base):
    html_path = f"../figures/{file_base}.html"
    fig.write_html(html_path)
    print(f"  ✅ Grafik kaydedildi: {file_base}.html")
    return html_path

# Veri setini yükle
print("="*80)
print("PHASE 5-6-7: DATA QUALITY, INSIGHTS & MODEL READINESS")
print("="*80)

df = pd.read_csv('../data/raw/churn.csv')

# TotalCharges düzelt (PHASE 4'ten)
df['TotalCharges'] = df['TotalCharges'].replace(' ', np.nan)
df['TotalCharges'] = pd.to_numeric(df['TotalCharges'], errors='coerce')

# ========================================================================
# PHASE 5: DATA QUALITY FINAL CHECK
# ========================================================================

print("\n" + "="*80)
print("PHASE 5: DATA QUALITY FINAL CHECK")
print("="*80)

# 1. Eksik Veri Özeti
print("\n1. EKSİK VERİ ÖZETİ:")
missing_summary = pd.DataFrame({
    'Değişken': df.columns,
    'Eksik Sayı': df.isnull().sum().values,
    'Eksik Oran (%)': (df.isnull().sum() / len(df) * 100).round(2).values
}).sort_values('Eksik Oran (%)', ascending=False)

print(missing_summary[missing_summary['Eksik Sayı'] > 0].to_string(index=False))

if missing_summary['Eksik Sayı'].sum() == 0:
    print("✅ Eksik değer yok (TotalCharges hariç, %0.16)")
else:
    print(f"⚠️ Toplam eksik hücre sayısı: {missing_summary['Eksik Sayı'].sum()}")

# 2. Duplicate Kontrolü
dup_count = df.duplicated().sum()
print(f"\n2. DUPLICATE KONTROL:")
print(f"Duplicate satır sayısı: {dup_count}")
if dup_count == 0:
    print("✅ Duplicate satır yok")

# 3. Veri Tipi Özeti
print(f"\n3. VERİ TİPİ ÖZETİ:")
dtype_summary = pd.DataFrame({
    'Veri Tipi': df.dtypes.value_counts().index.astype(str),
    'Değişken Sayısı': df.dtypes.value_counts().values
})
print(dtype_summary.to_string(index=False))

# 4. Final Data Quality Score
total_cells = df.shape[0] * df.shape[1]
missing_cells = df.isnull().sum().sum()
quality_score = ((total_cells - missing_cells) / total_cells * 100).round(2)

print(f"\n4. DATA QUALITY SCORE:")
print(f"Toplam hücre: {total_cells:,}")
print(f"Eksik hücre: {missing_cells}")
print(f"Kalite Skoru: %{quality_score} ✅")

missing_summary.to_csv('../reports/csv/phase5_data_quality_summary.csv', index=False)
print("\n✅ Data quality özeti: reports/csv/phase5_data_quality_summary.csv")

# ========================================================================
# PHASE 6: INSIGHT GENERATION
# ========================================================================

print("\n" + "="*80)
print("PHASE 6: INSIGHT GENERATION")
print("="*80)

insights = []

# İçgörü 1: tenure - En güçlü predictor
insights.append({
    "İçgörü": "1. tenure (Müşteri Süresi) - En Güçlü Churn Predictor",
    "Kanıt": "Churn eden müşteriler ort. 17.98 ay, etmeyen 37.57 ay (19.59 ay fark). p<0.001",
    "İş Değeri": "İlk 12-18 ay kritik risk periyodu. Yeni müşteri onboarding ve retention programı zorunlu.",
    "Modelleme Etkisi": "En yüksek feature importance beklenir. tenure_group, is_new_customer features önerilir."
})

# İçgörü 2: Contract - Sözleşme bağlılığı
insights.append({
    "İçgörü": "2. Contract (Sözleşme Tipi) - Bağlılık Faktörü",
    "Kanıt": "Month-to-month %42.71 churn, Two year %2.83 churn (%39.88 fark). Chi2=1184.60, p<0.001",
    "İş Değeri": "Aylık sözleşmeliler en riskli segment. Yıllık sözleşmeye geçiş incentive'leri agresif uygulanmalı.",
    "Modelleme Etkisi": "En yüksek feature importance (tenure ile birlikte). is_at_risk_contract flag önerilir."
})

# İçgörü 3: InternetService - Fiber optic paradoksu
insights.append({
    "İçgörü": "3. InternetService (Fiber Optic) - Premium Hizmet Paradoksu",
    "Kanıt": "Fiber optic %41.89 churn, DSL %18.96 churn. Fiber 2.2x daha riskli.",
    "İş Değeri": "En pahalı hizmet en yüksek churn'e sahip. Fiyat-değer dengesi sorunlu. Hizmet kalitesi audit gerekli.",
    "Modelleme Etkisi": "is_fiber_customer flag ve InternetService × Contract interaction feature önerilir."
})

# İçgörü 4: MonthlyCharges - Fiyat duyarlılığı
insights.append({
    "İçgörü": "4. MonthlyCharges (Aylık Ücret) - Fiyat Duyarlılığı",
    "Kanıt": "Churn eden ort. $74.44, etmeyen $61.27 ($13.17 fark, %21.5). p<0.001",
    "İş Değeri": "Yüksek fiyat segmenti churn'e yatkın. $70+ segment için value-added services ve dynamic pricing önerilir.",
    "Modelleme Etkisi": "price_per_tenure, is_high_spender features önerilir."
})

# İçgörü 5: PaymentMethod - Otomatik ödeme etkisi
insights.append({
    "İçgörü": "5. PaymentMethod (Ödeme Yöntemi) - Otomatik Ödeme Etkisi",
    "Kanıt": "Electronic check %45.29 churn, Credit card (auto) %15.24 churn (%30.05 fark). Chi2=648.14, p<0.001",
    "İş Değeri": "Manuel ödeme yapanlar 3x daha fazla churn ediyor. Otomatik ödeme geçiş incentive'leri önerilir.",
    "Modelleme Etkisi": "is_auto_pay, is_electronic_check_risk flags önerilir."
})

insights_df = pd.DataFrame(insights)
print(insights_df.to_string(index=False))

insights_df.to_csv('../reports/csv/phase6_key_insights.csv', index=False)
print("\n✅ Temel içgörüler: reports/csv/phase6_key_insights.csv")

# ========================================================================
# PHASE 7: MODEL READINESS ASSESSMENT
# ========================================================================

print("\n" + "="*80)
print("PHASE 7: MODEL READINESS ASSESSMENT")
print("="*80)

readiness_check = []

# 1. Eksik Veri Yönetimi
readiness_check.append({
    "Kontrol": "Eksik Veri Yönetimi",
    "Durum": "Hazır",
    "Açıklama": "TotalCharges'da %0.16 NaN var. Imputasyon: tenure × MonthlyCharges. Kritik değil.",
    "Öneri": "Data Prep Expert imputasyon uygulasın."
})

# 2. Encoding Gereksinimi
readiness_check.append({
    "Kontrol": "Encoding Gereksinimi",
    "Durum": "Gerekli",
    "Açıklama": "17 kategorik değişken var. Binary ve multi-class kategoriler encoding gerektirir.",
    "Öneri": "One-Hot Encoding (düşük kardinalite) veya Label Encoding. Hedef değişken (Churn) Label Encode edilmeli (Yes=1, No=0)."
})

# 3. Scaling Gereksinimi
readiness_check.append({
    "Kontrol": "Scaling Gereksinimi",
    "Durum": "Gerekli",
    "Açıklama": "Sayısal değişkenler farklı ölçeklerde (tenure: 0-72, MonthlyCharges: 18-118, TotalCharges: 18-8684).",
    "Öneri": "StandardScaler veya MinMaxScaler. Tree-based modeller için gerekli değil ama Logistic Regression, SVM için zorunlu."
})

# 4. Outlier İşleme
readiness_check.append({
    "Kontrol": "Outlier İşleme",
    "Durum": "İzlenmeli",
    "Açıklama": "SeniorCitizen'da %16.21 outlier (binary değişken yapısından kaynaklı, sorun değil). Diğer değişkenlerde kritik outlier yok.",
    "Öneri": "Outlier işleme gerekli değil. Binary değişkenlerde outlier doğal."
})

# 5. Target Imbalance
readiness_check.append({
    "Kontrol": "Target Imbalance",
    "Durum": "Hafif Dengesiz",
    "Açıklama": "Churn: No %73.46, Yes %26.54. Hafif dengesizlik var ama kritik değil.",
    "Öneri": "Stratified split zorunlu. Class weighting veya SMOTE opsiyonel (ilk model class_weight='balanced' ile dene)."
})

# 6. Leakage Riski
readiness_check.append({
    "Kontrol": "Leakage Riski",
    "Durum": "Kontrol Edildi",
    "Açıklama": "customerID ID değişkeni, modellemeden çıkarılmalı. Diğer değişkenlerde leakage riski yok.",
    "Öneri": "customerID çıkar."
})

# 7. Train-Test Split Stratejisi
readiness_check.append({
    "Kontrol": "Train-Test Split Stratejisi",
    "Durum": "Stratified Split",
    "Açıklama": "Hedef değişken dengesiz, stratified split zorunlu.",
    "Öneri": "train_test_split(..., stratify=y, test_size=0.2, random_state=42)"
})

# 8. Feature Engineering Fırsatları
readiness_check.append({
    "Kontrol": "Feature Engineering Fırsatları",
    "Durum": "Yüksek Potansiyel",
    "Açıklama": "Çok sayıda interaction ve aggregation fırsatı var.",
    "Öneri": "tenure_group, is_new_customer, contract_remaining_months, total_services_count, is_fiber_customer, is_auto_pay, average_monthly_spending vb."
})

# 9. Multicollinearity
readiness_check.append({
    "Kontrol": "Multicollinearity",
    "Durum": "Orta Risk",
    "Açıklama": "tenure ↔ TotalCharges yüksek korelasyon (r=0.826). VIF: tenure=6.33, TotalCharges=8.09.",
    "Öneri": "TotalCharges çıkar, tenure kullan. Alternatif: average_monthly_spending feature'ı oluştur."
})

# 10. Model Hazırlık Kararı
readiness_check.append({
    "Kontrol": "FINAL KARAR",
    "Durum": "KISMEN HAZIR",
    "Açıklama": "Veri seti modelleme için kullanılabilir ama preprocessing gerekli.",
    "Öneri": "Data Prep Expert: imputasyon, encoding, scaling, feature engineering, TotalCharges çıkarma işlemlerini yapmalı. Sonra Model Expert devreye girmeli."
})

readiness_df = pd.DataFrame(readiness_check)
print(readiness_df[['Kontrol', 'Durum', 'Açıklama']].to_string(index=False))

readiness_df.to_csv('../reports/csv/phase7_model_readiness.csv', index=False)
print("\n✅ Model readiness raporu: reports/csv/phase7_model_readiness.csv")

# ========================================================================
# FINAL ÖZET
# ========================================================================

print("\n" + "="*80)
print("FINAL ÖZET - TÜM EDA SÜRECİ TAMAMLANDI")
print("="*80)

print("\n📊 ANALIZ İSTATİSTİKLERİ:")
print(f"  - Toplam satır: 7,043")
print(f"  - Toplam değişken: 21")
print(f"  - Sayısal değişken: 4 (SeniorCitizen, tenure, MonthlyCharges, TotalCharges)")
print(f"  - Kategorik değişken: 17 (customerID hariç)")
print(f"  - Hedef değişken: Churn (No: 73.46%, Yes: 26.54%)")

print("\n📈 ÜRETİLEN ÇIKTILAR:")
phase_files = [
    ('phase1', 'Data Overview', '1 CSV'),
    ('phase2', 'Univariate Analysis', '3 CSV + 23 grafik'),
    ('phase3', 'Bivariate Analysis', '3 CSV + 38 grafik'),
    ('phase4', 'Multivariate Analysis', '3 CSV + 4 grafik'),
    ('phase5', 'Data Quality', '1 CSV'),
    ('phase6', 'Insight Generation', '1 CSV'),
    ('phase7', 'Model Readiness', '1 CSV')
]

total_csvs = 13
total_graphs = 65

for prefix, name, output in phase_files:
    print(f"  - {name}: {output}")

print(f"\n  ✅ Toplam CSV rapor: {total_csvs}")
print(f"  ✅ Toplam grafik: {total_graphs}")

print("\n🎯 EN ÖNEMLİ 3 CHURN PREDICTOR:")
print("  1. Contract (Month-to-month %42.71 vs Two year %2.83)")
print("  2. tenure (Churn=Yes ort. 17.98 ay vs Churn=No 37.57 ay)")
print("  3. InternetService (Fiber optic %41.89 vs No internet %7.40)")

print("\n⚠️ KRİTİK DATA PREP GÖREVLERİ:")
print("  1. TotalCharges imputasyon (11 NaN)")
print("  2. TotalCharges değişkenini çıkar (multicollinearity)")
print("  3. customerID değişkenini çıkar (ID değişkeni)")
print("  4. Kategorik encoding (17 değişken)")
print("  5. Sayısal scaling (StandardScaler)")
print("  6. Feature engineering (8+ yeni feature)")

print("\n✅ VERİ SETİ MODELLEME İÇİN: KISMEN HAZIR")
print("   Data Prep Expert preprocessing yapmalı → Model Expert modelleme yapmalı")

print("\n" + "="*80)
print("EDA SÜRECİ BAŞARIYLA TAMAMLANDI")
print("="*80)
