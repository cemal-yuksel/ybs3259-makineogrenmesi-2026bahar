# PHASE 3: BIVARIATE ANALYSIS
# Hedef değişken (Outcome) ile diğer değişkenler arasındaki ilişkileri inceleme

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
print("PHASE 3: BIVARIATE ANALYSIS")
print("="*80)
print()

# Veriyi yükle
df = pd.read_csv('../data/raw/diabetes.csv')
print(f"✓ Veri yüklendi: {df.shape[0]} satır, {df.shape[1]} sütun")
print()

# Hedef değişken
target = 'Outcome'
print(f"🎯 Hedef Değişken: {target}")
print(f"Dağılım: {df[target].value_counts().to_dict()}")
print()

# Sayısal değişkenleri belirle (Outcome hariç)
numeric_columns = [col for col in df.select_dtypes(include=[np.number]).columns if col != target]

print(f"📊 Analiz edilecek değişken sayısı: {len(numeric_columns)}")
print()

# Hedef değişken dağılımı görselleştir
target_counts = df[target].value_counts().sort_index()
fig = go.Figure(data=[
    go.Bar(
        x=['Diyabet Yok (0)', 'Diyabet Var (1)'],
        y=target_counts.values,
        text=[f'{count} (%{count/len(df)*100:.1f})' for count in target_counts.values],
        textposition='outside',
        marker_color=[PROFESSIONAL_PALETTE[4], PROFESSIONAL_PALETTE[3]]
    )
])
fig = apply_premium_layout(fig, "Hedef Değişken (Outcome) Dağılımı")
fig.update_xaxes(title_text="Outcome", title_font=dict(size=14, family="Arial", color="#1F2937"))
fig.update_yaxes(title_text="Frekans", title_font=dict(size=14, family="Arial", color="#1F2937"))
save_figure(fig, "phase3_target_distribution")

# Class imbalance kontrolü
dominant_ratio = (target_counts.max() / len(df) * 100)
if dominant_ratio > 70:
    add_data_prep_recommendation(
        issue="Hedef değişkende dengesiz dağılım",
        evidence=f"Baskın sınıf oranı %{dominant_ratio:.2f}.",
        recommendation="Data Prep Expert; SMOTE, class weighting, undersampling veya stratified split seçeneklerini değerlendirmelidir.",
        priority="Yüksek"
    )
elif dominant_ratio > 60:
    add_data_prep_recommendation(
        issue="Hedef değişkende orta düzey dengesizlik",
        evidence=f"Baskın sınıf oranı %{dominant_ratio:.2f}.",
        recommendation="Data Prep Expert; stratified K-Fold CV ve class weighting kullanmalıdır.",
        priority="Orta"
    )

print("\n" + "="*80)
print("HER DEĞİŞKEN İÇİN OUTCOME İLE İLİŞKİ ANALİZİ")
print("="*80)

# Bivariate analiz özeti
bivariate_summary = []

for col in numeric_columns:
    print(f"\n{'='*60}")
    print(f"Değişken: {col} vs {target}")
    print(f"{'='*60}")
    
    # Grup bazlı istatistikler
    group_stats = df.groupby(target)[col].agg(['mean', 'median', 'std', 'min', 'max'])
    print("\nGrup Bazlı İstatistikler:")
    print(group_stats)
    
    # Grup farkları
    mean_0 = df[df[target] == 0][col].mean()
    mean_1 = df[df[target] == 1][col].mean()
    mean_diff = abs(mean_1 - mean_0)
    mean_diff_pct = (mean_diff / mean_0 * 100) if mean_0 != 0 else 0
    
    print(f"\nOrtalama Farkı:")
    print(f"  Diyabet Yok (0): {mean_0:.2f}")
    print(f"  Diyabet Var (1): {mean_1:.2f}")
    print(f"  Mutlak Fark: {mean_diff:.2f} (%{mean_diff_pct:.1f})")
    
    # İstatistiksel test (Mann-Whitney U - non-parametric)
    group_0 = df[df[target] == 0][col]
    group_1 = df[df[target] == 1][col]
    
    # Mann-Whitney U test
    u_stat, p_value = stats.mannwhitneyu(group_0, group_1, alternative='two-sided')
    
    print(f"\nMann-Whitney U Test:")
    print(f"  U-statistic: {u_stat:.2f}")
    print(f"  p-value: {p_value:.4f}")
    
    if p_value < 0.001:
        significance = "Çok Güçlü İlişki (p<0.001)"
    elif p_value < 0.01:
        significance = "Güçlü İlişki (p<0.01)"
    elif p_value < 0.05:
        significance = "Anlamlı İlişki (p<0.05)"
    else:
        significance = "İlişki Yok (p>=0.05)"
    
    print(f"  Yorum: {significance}")
    
    # Boxplot
    fig = go.Figure()
    fig.add_trace(go.Box(
        y=df[df[target] == 0][col],
        name='Diyabet Yok (0)',
        marker_color=PROFESSIONAL_PALETTE[4],
        boxmean='sd'
    ))
    fig.add_trace(go.Box(
        y=df[df[target] == 1][col],
        name='Diyabet Var (1)',
        marker_color=PROFESSIONAL_PALETTE[3],
        boxmean='sd'
    ))
    fig = apply_premium_layout(fig, f"{col} vs Outcome (Boxplot)")
    fig.update_yaxes(title_text=col, title_font=dict(size=14, family="Arial", color="#1F2937"))
    fig.update_xaxes(title_text="Outcome", title_font=dict(size=14, family="Arial", color="#1F2937"))
    save_figure(fig, f"phase3_boxplot_{col.lower()}_vs_outcome")
    
    # Violin plot
    fig = go.Figure()
    fig.add_trace(go.Violin(
        y=df[df[target] == 0][col],
        name='Diyabet Yok (0)',
        marker_color=PROFESSIONAL_PALETTE[4],
        box_visible=True,
        meanline_visible=True
    ))
    fig.add_trace(go.Violin(
        y=df[df[target] == 1][col],
        name='Diyabet Var (1)',
        marker_color=PROFESSIONAL_PALETTE[3],
        box_visible=True,
        meanline_visible=True
    ))
    fig = apply_premium_layout(fig, f"{col} vs Outcome (Violin Plot)")
    fig.update_yaxes(title_text=col, title_font=dict(size=14, family="Arial", color="#1F2937"))
    fig.update_xaxes(title_text="Outcome", title_font=dict(size=14, family="Arial", color="#1F2937"))
    save_figure(fig, f"phase3_violin_{col.lower()}_vs_outcome")
    
    # Özet tabloya ekle
    bivariate_summary.append({
        'Değişken': col,
        'Ortalama (0)': round(mean_0, 2),
        'Ortalama (1)': round(mean_1, 2),
        'Fark': round(mean_diff, 2),
        'Fark (%)': round(mean_diff_pct, 1),
        'Mann-Whitney U': round(u_stat, 2),
        'p-value': round(p_value, 4),
        'Anlamlılık': significance
    })
    
    # Feature importance için işaretle
    if p_value < 0.001:
        add_data_prep_recommendation(
            issue=f"{col} değişkeni hedef değişkenle çok güçlü ilişkili",
            evidence=f"Mann-Whitney U test p-value: {p_value:.4f} (p<0.001).",
            recommendation=f"Feature Engineering Expert, {col} değişkenini öne çıkarmalı ve interaction feature'lar oluşturmalıdır.",
            priority="Yüksek"
        )

print("\n" + "="*80)

# Özet tabloyu kaydet
summary_df = pd.DataFrame(bivariate_summary)
summary_df = summary_df.sort_values('p-value')  # p-value'ya göre sırala (en güçlü ilişki en üstte)
summary_df.to_csv('../reports/csv/phase3_bivariate_summary.csv', index=False)
print("\n✓ Bivariate özet rapor kaydedildi: reports/csv/phase3_bivariate_summary.csv")

# Feature importance ranking
print("\n" + "="*80)
print("FEATURE IMPORTANCE RANKING (p-value bazlı)")
print("="*80)
print(summary_df[['Değişken', 'Fark (%)', 'p-value', 'Anlamlılık']])

# Data Prep önerilerini kaydet
if len(data_prep_recommendations) > 0:
    recommendations_df = pd.DataFrame(data_prep_recommendations)
    recommendations_df.to_csv('../reports/csv/phase3_data_prep_recommendations.csv', index=False)
    print(f"\n✓ {len(data_prep_recommendations)} adet Data Prep önerisi kaydedildi.")

print("\n" + "="*80)
print("PHASE 3 TAMAMLANDI")
print("="*80)
