# PHASE 4: MULTIVARIATE ANALYSIS
# Çok değişkenli ilişkiler ve multicollinearity kontrolü

import os
import warnings
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from scipy import stats
from pathlib import Path

warnings.filterwarnings("ignore")

# Klasörlerin varlığını garantile
Path('../figures').mkdir(parents=True, exist_ok=True)
Path('../reports/csv').mkdir(parents=True, exist_ok=True)

# Profesyonel renk paleti
PROFESSIONAL_PALETTE = [
    "#2E86AB",  # Koyu mavi
    "#A23B72",  # Koyu pembe/mor
    "#F18F01",  # Turuncu
    "#C73E1D",  # Koyu kırmızı
    "#6A994E",  # Orman yeşili
    "#BC4B51",  # Bordo
    "#8E7DBE",  # Mor
    "#F77F00",  # Koyu turuncu
    "#06A77D",  # Turkuaz
    "#D4A574"   # Altın-bronz
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
    """Profesyonel, net ve görkemli grafik düzeni uygular"""
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
        margin=dict(l=60, r=40, t=100, b=60),
        hoverlabel=dict(
            bgcolor="white",
            font_size=12,
            font_family="Arial"
        )
    )
    return fig

def save_figure(fig, file_base):
    html_path = f"../figures/{file_base}.html"
    fig.write_html(html_path)
    print(f"✓ Grafik kaydedildi: {html_path}")
    try:
        png_path = f"../figures/{file_base}.png"
        fig.write_image(png_path)
        print(f"✓ PNG kaydedildi: {png_path}")
    except Exception as e:
        pass

print("="*80)
print("PHASE 4: MULTIVARIATE ANALYSIS")
print("="*80)
print()

# Veriyi yükle
df = pd.read_csv('../data/raw/diabetes.csv')
print(f"✓ Veri yüklendi: {df.shape[0]} satır, {df.shape[1]} sütun")
print()

# Tüm sayısal değişkenleri al (Outcome dahil)
numeric_columns = df.select_dtypes(include=[np.number]).columns.tolist()

print(f"📊 Korelasyon analizi için değişken sayısı: {len(numeric_columns)}")
print(f"Değişkenler: {numeric_columns}")
print()

# Korelasyon matrisi hesapla
print("="*80)
print("KORELASYON MATRİSİ (Pearson)")
print("="*80)
print()

corr_matrix = df[numeric_columns].corr()
print(corr_matrix.round(3))
print()

# Korelasyon matrisini CSV olarak kaydet
corr_matrix.to_csv('../reports/csv/phase4_correlation_matrix.csv')
print("✓ Korelasyon matrisi kaydedildi: reports/csv/phase4_correlation_matrix.csv")
print()

# Korelasyon heatmap (Plotly)
fig = go.Figure(data=go.Heatmap(
    z=corr_matrix.values,
    x=corr_matrix.columns,
    y=corr_matrix.columns,
    colorscale=[
        [0, '#2E86AB'],      # Negatif korelasyon (mavi)
        [0.5, '#FBFBF8'],    # Sıfır korelasyon (beyaz)
        [1, '#C73E1D']       # Pozitif korelasyon (kırmızı)
    ],
    zmid=0,
    text=corr_matrix.values.round(2),
    texttemplate='%{text}',
    textfont={"size": 10},
    colorbar=dict(title="Korelasyon")
))

fig = apply_premium_layout(fig, "Korelasyon Matrisi (Pearson)")
fig.update_xaxes(tickangle=-45)
save_figure(fig, "phase4_correlation_heatmap")

# Yüksek korelasyonları bul (>0.70 veya <-0.70, diagonal hariç)
print("\n" + "="*80)
print("YÜKSEK KORELASYONLAR (|r| > 0.70)")
print("="*80)
print()

high_corr_pairs = []
for i in range(len(corr_matrix.columns)):
    for j in range(i+1, len(corr_matrix.columns)):
        corr_value = corr_matrix.iloc[i, j]
        if abs(corr_value) > 0.70:
            var1 = corr_matrix.columns[i]
            var2 = corr_matrix.columns[j]
            high_corr_pairs.append({
                'Değişken 1': var1,
                'Değişken 2': var2,
                'Korelasyon': round(corr_value, 3)
            })
            print(f"{var1} <-> {var2}: {corr_value:.3f}")

if len(high_corr_pairs) == 0:
    print("✓ |r| > 0.70 olan korelasyon çifti bulunmadı.")
    print("✓ Multicollinearity riski düşük.")
else:
    high_corr_df = pd.DataFrame(high_corr_pairs)
    high_corr_df.to_csv('../reports/csv/phase4_high_correlations.csv', index=False)
    print(f"\n✓ {len(high_corr_pairs)} adet yüksek korelasyon çifti kaydedildi.")
    
    # Data Prep önerisi
    for pair in high_corr_pairs:
        add_data_prep_recommendation(
            issue=f"Yüksek korelasyon: {pair['Değişken 1']} <-> {pair['Değişken 2']}",
            evidence=f"Korelasyon katsayısı: {pair['Korelasyon']:.3f} (|r| > 0.70).",
            recommendation=f"Data Prep Expert veya Modeling Expert, bu iki değişkenden birini çıkarmayı veya regularization (Ridge/Lasso) kullanmayı değerlendirmelidir.",
            priority="Orta"
        )

print()

# Orta düzeyde korelasyonlar (0.50-0.70 arası)
print("\n" + "="*80)
print("ORTA DÜZEYDE KORELASYONLAR (0.50 < |r| < 0.70)")
print("="*80)
print()

medium_corr_pairs = []
for i in range(len(corr_matrix.columns)):
    for j in range(i+1, len(corr_matrix.columns)):
        corr_value = corr_matrix.iloc[i, j]
        if 0.50 < abs(corr_value) <= 0.70:
            var1 = corr_matrix.columns[i]
            var2 = corr_matrix.columns[j]
            medium_corr_pairs.append({
                'Değişken 1': var1,
                'Değişken 2': var2,
                'Korelasyon': round(corr_value, 3)
            })
            print(f"{var1} <-> {var2}: {corr_value:.3f}")

if len(medium_corr_pairs) == 0:
    print("✓ 0.50 < |r| < 0.70 aralığında korelasyon bulunmadı.")
else:
    print(f"\n✓ {len(medium_corr_pairs)} adet orta düzeyde korelasyon çifti tespit edildi.")

print()

# Outcome ile korelasyonlar (hedef değişken ilişkisi)
print("\n" + "="*80)
print("OUTCOME İLE KORELASYONLAR (Feature Importance)")
print("="*80)
print()

outcome_corr = corr_matrix['Outcome'].drop('Outcome').sort_values(ascending=False)
print(outcome_corr)
print()

# Outcome korelasyonlarını görselleştir
fig = go.Figure(data=[
    go.Bar(
        x=outcome_corr.index,
        y=outcome_corr.values,
        marker_color=[PROFESSIONAL_PALETTE[0] if val > 0 else PROFESSIONAL_PALETTE[3] for val in outcome_corr.values],
        text=outcome_corr.values.round(3),
        textposition='outside'
    )
])

fig = apply_premium_layout(fig, "Outcome ile Korelasyonlar (Feature Importance)")
fig.update_xaxes(title_text="Değişken", tickangle=-45, title_font=dict(size=14, family="Arial", color="#1F2937"))
fig.update_yaxes(title_text="Korelasyon Katsayısı", title_font=dict(size=14, family="Arial", color="#1F2937"))
fig.add_hline(y=0, line_dash="dash", line_color="gray")
save_figure(fig, "phase4_outcome_correlations")

# Outcome korelasyonunu CSV olarak kaydet
outcome_corr_df = pd.DataFrame({
    'Değişken': outcome_corr.index,
    'Korelasyon': outcome_corr.values.round(3)
})
outcome_corr_df.to_csv('../reports/csv/phase4_outcome_correlations.csv', index=False)
print("✓ Outcome korelasyonları kaydedildi: reports/csv/phase4_outcome_correlations.csv")
print()

# En güçlü korelasyonları işaretle
strong_outcome_corr = outcome_corr[abs(outcome_corr) > 0.3]
if len(strong_outcome_corr) > 0:
    print("📌 Outcome ile güçlü korelasyona sahip değişkenler (|r| > 0.3):")
    for var, corr_val in strong_outcome_corr.items():
        print(f"  - {var}: {corr_val:.3f}")
    print()

# Scatter matrix (en önemli 4-5 değişken için)
print("\n" + "="*80)
print("SCATTER MATRIX (Top 5 Değişken + Outcome)")
print("="*80)
print()

top_vars = outcome_corr.head(5).index.tolist()
scatter_vars = top_vars + ['Outcome']

print(f"Seçilen değişkenler: {scatter_vars}")
print()

# Plotly scatter matrix
fig = px.scatter_matrix(
    df[scatter_vars],
    dimensions=scatter_vars,
    color='Outcome',
    color_discrete_map={0: PROFESSIONAL_PALETTE[4], 1: PROFESSIONAL_PALETTE[3]},
    labels={col: col for col in scatter_vars},
    title="Scatter Matrix (Top 5 Değişken + Outcome)"
)

fig.update_traces(diagonal_visible=False, showupperhalf=False)
fig = apply_premium_layout(fig, "Scatter Matrix (Top 5 Değişken + Outcome)")
save_figure(fig, "phase4_scatter_matrix")

# Data Prep önerilerini kaydet
if len(data_prep_recommendations) > 0:
    recommendations_df = pd.DataFrame(data_prep_recommendations)
    recommendations_df.to_csv('../reports/csv/phase4_data_prep_recommendations.csv', index=False)
    print(f"\n✓ {len(data_prep_recommendations)} adet Data Prep önerisi kaydedildi.")

print("\n" + "="*80)
print("PHASE 4 TAMAMLANDI")
print("="*80)
