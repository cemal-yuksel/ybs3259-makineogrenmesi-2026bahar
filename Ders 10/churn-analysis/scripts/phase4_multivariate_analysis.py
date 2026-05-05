"""
PHASE 4: MULTIVARIATE ANALYSIS
Çok değişkenli yapıyı ve birlikte hareket eden değişkenleri incelemek
"""

import os
import warnings
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
from statsmodels.stats.outliers_influence import variance_inflation_factor

warnings.filterwarnings("ignore")

# Klasörlerin varlığını garantile
Path('../figures').mkdir(parents=True, exist_ok=True)
Path('../reports/csv').mkdir(parents=True, exist_ok=True)

# Profesyonel renk paleti
PROFESSIONAL_PALETTE = [
    "#2E86AB", "#A23B72", "#F18F01", "#C73E1D", "#6A994E",
    "#BC4B51", "#8E7DBE", "#F77F00", "#06A77D", "#D4A574"
]

# Data Prep önerileri
data_prep_recommendations = []

def add_data_prep_recommendation(issue, evidence, recommendation, priority="Orta"):
    data_prep_recommendations.append({
        "Sorun": issue,
        "Kanıt": evidence,
        "Öneri": recommendation,
        "Öncelik": priority
    })

def apply_premium_layout(fig, title):
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
    html_path = f"../figures/{file_base}.html"
    fig.write_html(html_path)
    print(f"  ✅ Grafik kaydedildi: {file_base}.html")
    return html_path

# Veri setini yükle
print("="*80)
print("PHASE 4: MULTIVARIATE ANALYSIS")
print("="*80)

df = pd.read_csv('../data/raw/churn.csv')

# ========================================================================
# TotalCharges VERİ KALİTESİ DÜZELTMESİ
# ========================================================================

print("\n" + "="*80)
print("1. TotalCharges VERİ KALİTESİ DÜZELTMESİ")
print("="*80)

print(f"\nÖnceki veri tipi: {df['TotalCharges'].dtype}")
print(f"Örnek değerler: {df['TotalCharges'].head().tolist()}")

# Boşluk kontrolü
empty_count = (df['TotalCharges'] == ' ').sum()
print(f"\nBoşluk karakteri içeren satır sayısı: {empty_count}")

if empty_count > 0:
    print(f"⚠️ {empty_count} satırda TotalCharges boşluk içeriyor")
    # Boşlukları NaN'a çevir
    df['TotalCharges'] = df['TotalCharges'].replace(' ', np.nan)
    print("✅ Boşluklar NaN'a çevrildi")

# Numeric'e çevir
try:
    df['TotalCharges'] = pd.to_numeric(df['TotalCharges'], errors='coerce')
    print("✅ TotalCharges numeric'e çevrildi")
    print(f"Yeni veri tipi: {df['TotalCharges'].dtype}")
    
    # NaN sayısı
    nan_count = df['TotalCharges'].isnull().sum()
    nan_ratio = (nan_count / len(df) * 100)
    print(f"\nDönüşüm sonrası NaN sayısı: {nan_count} (%{nan_ratio:.2f})")
    
    if nan_count > 0:
        add_data_prep_recommendation(
            issue="TotalCharges - NaN değerler",
            evidence=f"{nan_count} satırda TotalCharges NaN (%{nan_ratio:.2f})",
            recommendation="Data Prep Expert imputasyon stratejisi belirlemelidir (median, forward fill veya tenure × MonthlyCharges hesaplama).",
            priority="Yüksek"
        )
    
    # İstatistikler
    print(f"\nTotalCharges İstatistikleri:")
    print(df['TotalCharges'].describe())
    
except Exception as e:
    print(f"❌ Hata: {e}")

# ========================================================================
# SAYISAL DEĞİŞKENLER - KORELASYON MATRİSİ
# ========================================================================

print("\n" + "="*80)
print("2. SAYISAL DEĞİŞKENLER - KORELASYON ANALİZİ")
print("="*80)

# Sayısal değişkenleri seç (NaN olmadan)
numeric_cols = ['SeniorCitizen', 'tenure', 'MonthlyCharges', 'TotalCharges']
df_numeric = df[numeric_cols].copy()

# Korelasyon matrisi
corr_matrix = df_numeric.corr().round(3)
print("\nKorelasyon Matrisi:")
print(corr_matrix)

# Korelasyon heatmap
fig_corr = px.imshow(
    corr_matrix,
    text_auto=True,
    color_continuous_scale='RdBu_r',
    color_continuous_midpoint=0,
    title="Sayısal Değişkenler - Korelasyon Matrisi",
    labels=dict(color="Korelasyon"),
    zmin=-1,
    zmax=1
)
fig_corr = apply_premium_layout(fig_corr, "Sayısal Değişkenler - Korelasyon Matrisi")
save_figure(fig_corr, "phase4_correlation_matrix")

# Yüksek korelasyon kontrolü
print("\n⚠️ Yüksek Korelasyon Kontrol (|r| > 0.80):")
high_corr_found = False

for i in range(len(corr_matrix.columns)):
    for j in range(i+1, len(corr_matrix.columns)):
        col1 = corr_matrix.columns[i]
        col2 = corr_matrix.columns[j]
        corr_val = corr_matrix.iloc[i, j]
        
        if abs(corr_val) > 0.80:
            print(f"  - {col1} ↔ {col2}: r = {corr_val:.3f}")
            high_corr_found = True
            
            add_data_prep_recommendation(
                issue=f"Yüksek korelasyon: {col1} ↔ {col2}",
                evidence=f"Korelasyon katsayısı: {corr_val:.3f}",
                recommendation="Data Prep Expert multicollinearity riski için VIF analizi yapmalı ve değişken seçimi değerlendirmelidir.",
                priority="Yüksek"
            )

if not high_corr_found:
    print("  ✅ |r| > 0.80 olan korelasyon bulunamadı")

# Orta-yüksek korelasyon
print("\n📊 Orta-Yüksek Korelasyon (0.50 < |r| < 0.80):")
medium_corr_found = False

for i in range(len(corr_matrix.columns)):
    for j in range(i+1, len(corr_matrix.columns)):
        col1 = corr_matrix.columns[i]
        col2 = corr_matrix.columns[j]
        corr_val = corr_matrix.iloc[i, j]
        
        if 0.50 < abs(corr_val) < 0.80:
            print(f"  - {col1} ↔ {col2}: r = {corr_val:.3f}")
            medium_corr_found = True

if not medium_corr_found:
    print("  ✅ 0.50 < |r| < 0.80 korelasyon bulunamadı")

# ========================================================================
# VIF (VARIANCE INFLATION FACTOR) ANALİZİ
# ========================================================================

print("\n" + "="*80)
print("3. VIF (MULTICOLLINEARITY) ANALİZİ")
print("="*80)

# NaN olmayan satırları seç
df_numeric_clean = df_numeric.dropna()
print(f"\nVIF hesaplaması için kullanılan satır sayısı: {len(df_numeric_clean)} (NaN hariç)")

# VIF hesapla
vif_data = pd.DataFrame()
vif_data["Değişken"] = numeric_cols

vif_values = []
for i in range(len(numeric_cols)):
    try:
        vif = variance_inflation_factor(df_numeric_clean.values, i)
        vif_values.append(round(vif, 2))
    except:
        vif_values.append(np.nan)

vif_data["VIF"] = vif_values

print("\nVIF Değerleri:")
print(vif_data.to_string(index=False))

print("\n📖 VIF Yorumlama Kılavuzu:")
print("  - VIF < 5: Düşük multicollinearity ✅")
print("  - 5 ≤ VIF < 10: Orta multicollinearity ⚠️")
print("  - VIF ≥ 10: Yüksek multicollinearity 🔴")

# VIF önerileri
print("\n⚠️ VIF Bazlı Öneriler:")
high_vif_found = False

for idx, row in vif_data.iterrows():
    var = row['Değişken']
    vif = row['VIF']
    
    if pd.notna(vif):
        if vif >= 10:
            print(f"  🔴 {var}: VIF = {vif} → Yüksek multicollinearity")
            high_vif_found = True
            add_data_prep_recommendation(
                issue=f"{var} - Yüksek VIF",
                evidence=f"VIF = {vif}",
                recommendation="Data Prep Expert değişken seçimi veya regularization (Ridge, Lasso) değerlendirmelidir.",
                priority="Yüksek"
            )
        elif vif >= 5:
            print(f"  ⚠️ {var}: VIF = {vif} → Orta multicollinearity")
        else:
            print(f"  ✅ {var}: VIF = {vif} → Düşük multicollinearity")

if not high_vif_found:
    print("\n✅ Yüksek VIF (≥10) olan değişken bulunamadı")

# VIF CSV kaydet
vif_data.to_csv('../reports/csv/phase4_vif_analysis.csv', index=False)
print("\n✅ VIF raporu: reports/csv/phase4_vif_analysis.csv")

# ========================================================================
# SCATTER MATRIX (Önemli ilişkiler)
# ========================================================================

print("\n" + "="*80)
print("4. SCATTER MATRIX (IKILI ILISKILER)")
print("="*80)

# tenure vs MonthlyCharges
fig_scatter1 = px.scatter(
    df,
    x='tenure',
    y='MonthlyCharges',
    color='Churn',
    color_discrete_map={"No": PROFESSIONAL_PALETTE[4], "Yes": PROFESSIONAL_PALETTE[3]},
    title="tenure vs MonthlyCharges (Churn bazlı)",
    trendline="lowess",
    opacity=0.6
)
fig_scatter1 = apply_premium_layout(fig_scatter1, "tenure vs MonthlyCharges (Churn bazlı)")
save_figure(fig_scatter1, "phase4_scatter_tenure_vs_monthlycharges")

# tenure vs TotalCharges
fig_scatter2 = px.scatter(
    df.dropna(subset=['TotalCharges']),
    x='tenure',
    y='TotalCharges',
    color='Churn',
    color_discrete_map={"No": PROFESSIONAL_PALETTE[4], "Yes": PROFESSIONAL_PALETTE[3]},
    title="tenure vs TotalCharges (Churn bazlı)",
    trendline="lowess",
    opacity=0.6
)
fig_scatter2 = apply_premium_layout(fig_scatter2, "tenure vs TotalCharges (Churn bazlı)")
save_figure(fig_scatter2, "phase4_scatter_tenure_vs_totalcharges")

# MonthlyCharges vs TotalCharges
fig_scatter3 = px.scatter(
    df.dropna(subset=['TotalCharges']),
    x='MonthlyCharges',
    y='TotalCharges',
    color='Churn',
    color_discrete_map={"No": PROFESSIONAL_PALETTE[4], "Yes": PROFESSIONAL_PALETTE[3]},
    title="MonthlyCharges vs TotalCharges (Churn bazlı)",
    trendline="lowess",
    opacity=0.6
)
fig_scatter3 = apply_premium_layout(fig_scatter3, "MonthlyCharges vs TotalCharges (Churn bazlı)")
save_figure(fig_scatter3, "phase4_scatter_monthlycharges_vs_totalcharges")

print("\n✅ 3 scatter plot oluşturuldu")

# ========================================================================
# KORELASYON ÖZETİ CSV
# ========================================================================

corr_matrix.to_csv('../reports/csv/phase4_correlation_matrix.csv')
print("\n✅ Korelasyon matrisi: reports/csv/phase4_correlation_matrix.csv")

# ========================================================================
# DATA PREP EXPERT ÖNERİLERİ
# ========================================================================

if data_prep_recommendations:
    print("\n" + "="*80)
    print("5. DATA PREP EXPERT İÇİN ÖNERİLER")
    print("="*80)
    
    recommendations_df = pd.DataFrame(data_prep_recommendations)
    print(recommendations_df.to_string(index=False))
    
    recommendations_df.to_csv('../reports/csv/phase4_data_prep_recommendations.csv', index=False)
    print("\n✅ Data Prep önerileri: reports/csv/phase4_data_prep_recommendations.csv")

print("\n" + "="*80)
print("PHASE 4 TAMAMLANDI")
print("Korelasyon matrisi, VIF analizi ve scatter plotlar oluşturuldu")
print("="*80)
