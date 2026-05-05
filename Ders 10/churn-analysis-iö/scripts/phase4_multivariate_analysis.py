# ================================================================
# PHASE 4: MULTIVARIATE ANALYSIS
# ================================================================
# Çok değişkenli yapıyı ve birlikte hareket eden değişkenleri incelemek

import os
import warnings
from pathlib import Path
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from scipy import stats
from statsmodels.stats.outliers_influence import variance_inflation_factor

warnings.filterwarnings("ignore")

# Profesyonel renk paleti
PROFESSIONAL_PALETTE = [
    "#2E86AB", "#A23B72", "#F18F01", "#C73E1D", "#6A994E",
    "#BC4B51", "#8E7DBE", "#F77F00", "#06A77D", "#D4A574"
]

# Data Prep Expert için öneri listesi
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
        margin=dict(l=60, r=40, t=80, b=60),
        legend_title_text="Kategori",
        hoverlabel=dict(
            bgcolor="white",
            font_size=12,
            font_family="Arial"
        )
    )
    fig.update_xaxes(showgrid=True, gridcolor="#E5E7EB", zeroline=False)
    fig.update_yaxes(showgrid=True, gridcolor="#E5E7EB", zeroline=False)
    return fig

def save_figure(fig, file_base):
    """Grafiği HTML ve PNG olarak kaydet"""
    html_path = f"../figures/{file_base}.html"
    png_path = f"../figures/{file_base}.png"
    
    fig.write_html(html_path)
    print(f"  ✅ Kaydedildi: {html_path}")
    
    try:
        fig.write_image(png_path)
        print(f"  ✅ Kaydedildi: {png_path}")
    except Exception as e:
        print(f"  ⚠️  PNG kaydı yapılamadı (kaleido gerekli): {png_path}")

print("=" * 70)
print("PHASE 4: MULTIVARIATE ANALYSIS")
print("=" * 70)
print()

# Veri setini yükle
df = pd.read_csv('../data/raw/churn.csv')

# TotalCharges düzelt
if 'TotalCharges' in df.columns and df['TotalCharges'].dtype == 'object':
    df['TotalCharges'] = pd.to_numeric(df['TotalCharges'], errors='coerce')

print(f"✅ Veri seti yüklendi: {df.shape[0]} satır, {df.shape[1]} sütun\n")

# Sayısal değişkenler
numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()

print("=" * 70)
print("A. KORELASYON MATRİSİ ANALİZİ")
print("=" * 70)
print()

# Korelasyon matrisi hesapla
correlation_matrix = df[numeric_cols].corr()

print("Sayısal Değişkenler Korelasyon Matrisi:")
print(correlation_matrix.round(3))
print()

# Plotly Heatmap
fig_corr = go.Figure(data=go.Heatmap(
    z=correlation_matrix.values,
    x=correlation_matrix.columns,
    y=correlation_matrix.columns,
    colorscale='RdBu_r',
    zmid=0,
    text=correlation_matrix.values.round(3),
    texttemplate='%{text}',
    textfont={"size": 14, "color": "white"},
    colorbar=dict(title="Korelasyon")
))

fig_corr.update_layout(
    title={
        "text": "Sayısal Değişkenler Korelasyon Matrisi",
        "x": 0.03,
        "xanchor": "left",
        "font": {"size": 24, "family": "Arial Black", "color": "#1F2937"}
    },
    template="plotly_white",
    paper_bgcolor="#FBFBF8",
    font={"family": "Arial", "size": 13, "color": "#374151"},
    xaxis_title="",
    yaxis_title="",
    width=800,
    height=800
)

save_figure(fig_corr, "phase4_correlation_matrix")
print()

# Yüksek korelasyonlar tespit et
print("=" * 70)
print("B. YÜKSEK KORELASYON TESPİTİ")
print("=" * 70)
print()

high_correlations = []
for i in range(len(correlation_matrix.columns)):
    for j in range(i+1, len(correlation_matrix.columns)):
        corr_value = correlation_matrix.iloc[i, j]
        if abs(corr_value) > 0.80:
            high_correlations.append({
                'Değişken 1': correlation_matrix.columns[i],
                'Değişken 2': correlation_matrix.columns[j],
                'Korelasyon': round(corr_value, 4)
            })
            print(f"⚠️  Yüksek Korelasyon Tespit Edildi:")
            print(f"    {correlation_matrix.columns[i]} <-> {correlation_matrix.columns[j]}: {corr_value:.4f}")
            
            add_data_prep_recommendation(
                issue=f"Yüksek korelasyon: {correlation_matrix.columns[i]} - {correlation_matrix.columns[j]}",
                evidence=f"Korelasyon değeri {corr_value:.4f} olarak hesaplandı.",
                recommendation="Data Prep Expert bu değişkenlerden birini modelden çıkarma veya PCA/feature selection uygulamayı değerlendirmelidir. Multicollinearity riski modelleme performansını düşürebilir.",
                priority="Yüksek"
            )

if len(high_correlations) == 0:
    print("✅ Sayısal değişkenler arasında 0.80 üzeri korelasyon tespit edilmedi.")
else:
    high_corr_df = pd.DataFrame(high_correlations)
    high_corr_df.to_csv('../reports/csv/phase4_high_correlations.csv', index=False, encoding='utf-8-sig')
    print(f"\n📄 Yüksek korelasyon raporu kaydedildi: ../reports/csv/phase4_high_correlations.csv")

print()

# VIF analizi
print("=" * 70)
print("C. VARIANCE INFLATION FACTOR (VIF) ANALİZİ")
print("=" * 70)
print()

# VIF için eksik değerleri doldur (geçici)
df_vif = df[numeric_cols].copy()
df_vif = df_vif.fillna(df_vif.median())

# VIF hesapla
vif_data = pd.DataFrame()
vif_data["Değişken"] = numeric_cols
vif_data["VIF"] = [variance_inflation_factor(df_vif.values, i) for i in range(len(numeric_cols))]
vif_data = vif_data.sort_values('VIF', ascending=False).reset_index(drop=True)

print("Variance Inflation Factor (VIF) Değerleri:")
print(vif_data.to_string(index=False))
print()

# VIF yorumlama
print("VIF Yorumlama:")
print("  VIF < 5   : Multicollinearity riski düşük")
print("  5 ≤ VIF < 10 : Orta düzey multicollinearity riski")
print("  VIF ≥ 10  : Yüksek multicollinearity riski")
print()

# Yüksek VIF tespiti
for idx, row in vif_data.iterrows():
    if row['VIF'] >= 10:
        print(f"⚠️  {row['Değişken']} değişkeninde yüksek VIF tespit edildi: {row['VIF']:.2f}")
        add_data_prep_recommendation(
            issue=f"{row['Değişken']} değişkeninde yüksek VIF",
            evidence=f"VIF değeri {row['VIF']:.2f} olarak hesaplandı.",
            recommendation="Data Prep Expert bu değişkeni modelden çıkarmayı veya regularization (Ridge/Lasso) tekniklerini uygulamayı değerlendirmelidir.",
            priority="Yüksek"
        )

# VIF bar chart
fig_vif = px.bar(
    vif_data,
    x='VIF',
    y='Değişken',
    orientation='h',
    color='VIF',
    color_continuous_scale=['#D5F5E3', '#F7D9A3', '#F6C6C6'],
    title="Variance Inflation Factor (VIF) Değerleri"
)
fig_vif = apply_premium_layout(fig_vif, "Variance Inflation Factor (VIF) Değerleri")
save_figure(fig_vif, "phase4_vif_analysis")

# VIF raporu kaydet
vif_data.to_csv('../reports/csv/phase4_vif_analysis.csv', index=False, encoding='utf-8-sig')
print(f"\n📄 VIF analiz raporu kaydedildi: ../reports/csv/phase4_vif_analysis.csv")
print()

# Pairwise scatter matrix (kritik değişkenler için)
print("=" * 70)
print("D. PAIRWISE SCATTER MATRIX (KRİTİK DEĞİŞKENLER)")
print("=" * 70)
print()

# Hedef değişken varsa scatter matrix oluştur
if 'Churn' in df.columns:
    # En önemli 4 değişken için scatter matrix
    important_vars = ['tenure', 'MonthlyCharges', 'TotalCharges', 'SeniorCitizen']
    
    df_scatter = df[important_vars + ['Churn']].copy()
    df_scatter = df_scatter.dropna()
    
    fig_scatter = px.scatter_matrix(
        df_scatter,
        dimensions=important_vars,
        color='Churn',
        color_discrete_sequence=[PROFESSIONAL_PALETTE[0], PROFESSIONAL_PALETTE[1]],
        title="Kritik Sayısal Değişkenler - Pairwise Scatter Matrix",
        height=1000,
        width=1000
    )
    
    fig_scatter.update_traces(diagonal_visible=False, showupperhalf=False)
    fig_scatter.update_layout(
        title={
            "text": "Kritik Sayısal Değişkenler - Pairwise Scatter Matrix",
            "x": 0.03,
            "font": {"size": 22, "family": "Arial Black", "color": "#1F2937"}
        },
        template="plotly_white",
        paper_bgcolor="#FBFBF8",
        font={"family": "Arial", "size": 11, "color": "#374151"}
    )
    
    save_figure(fig_scatter, "phase4_scatter_matrix")
    print("✅ Scatter matrix oluşturuldu ve kaydedildi.")
else:
    print("⚠️  Hedef değişken bulunamadı, scatter matrix oluşturulamadı.")

print()

# Data Prep önerileri kaydet
if len(data_prep_recommendations) > 0:
    recommendations_df = pd.DataFrame(data_prep_recommendations)
    recommendations_df.to_csv('../reports/csv/phase4_data_prep_recommendations.csv', index=False, encoding='utf-8-sig')
    print(f"📄 Data Prep Expert için {len(data_prep_recommendations)} öneri kaydedildi.\n")

print("=" * 70)
print("✅ PHASE 4 TAMAMLANDI")
print("=" * 70)
