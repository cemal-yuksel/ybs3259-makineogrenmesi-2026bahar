"""
PHASE 3: BIVARIATE ANALYSIS
Hedef değişken (Churn) ile diğer değişkenler arasındaki ilişkileri incelemek
"""

import os
import warnings
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
from scipy import stats

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

# Churn için özel renk paleti
CHURN_COLORS = {
    "No": PROFESSIONAL_PALETTE[4],   # Yeşil - kaldı
    "Yes": PROFESSIONAL_PALETTE[3]   # Kırmızı - ayrıldı
}

# Data Prep önerileri için liste
data_prep_recommendations = []

def add_data_prep_recommendation(issue, evidence, recommendation, priority="Orta"):
    """Data Prep Expert için öneri kaydet"""
    data_prep_recommendations.append({
        "Sorun": issue,
        "Kanıt": evidence,
        "Öneri": recommendation,
        "Öncelik": priority
    })

def apply_premium_layout(fig, title):
    """Profesyonel grafik düzeni uygula"""
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
    """Grafik kaydet"""
    html_path = f"../figures/{file_base}.html"
    fig.write_html(html_path)
    print(f"  ✅ Grafik kaydedildi: {file_base}.html")
    return html_path

# Veri setini yükle
print("="*80)
print("PHASE 3: BIVARIATE ANALYSIS")
print("="*80)

df = pd.read_csv('../data/raw/churn.csv')

# Hedef değişken
target_col = 'Churn'

# Sayısal ve kategorik değişkenleri ayır
numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
categorical_cols = df.select_dtypes(include=['object']).columns.tolist()

# customerID ve Churn'i kategorik listeden çıkar
if 'customerID' in categorical_cols:
    categorical_cols.remove('customerID')
if target_col in categorical_cols:
    categorical_cols.remove(target_col)

print(f"\n📊 Hedef değişken: {target_col}")
print(f"📊 Analiz edilecek sayısal değişken sayısı: {len(numeric_cols)}")
print(f"📊 Analiz edilecek kategorik değişken sayısı: {len(categorical_cols)}")

# ========================================================================
# SAYISAL DEĞİŞKENLER vs CHURN
# ========================================================================

print("\n" + "="*80)
print("1. SAYISAL DEĞİŞKENLER vs CHURN ANALİZİ")
print("="*80)

numeric_churn_summary = []

for col in numeric_cols:
    print(f"\n{'='*80}")
    print(f"Değişken: {col} vs {target_col}")
    print(f"{'='*80}")
    
    # Grup bazlı istatistikler
    grouped_stats = df.groupby(target_col)[col].agg(['mean', 'median', 'std', 'min', 'max']).round(2)
    print("\nGrup Bazlı İstatistikler:")
    print(grouped_stats)
    
    # T-test (bağımsız iki örnek)
    churn_no = df[df[target_col] == 'No'][col]
    churn_yes = df[df[target_col] == 'Yes'][col]
    
    t_stat, p_value = stats.ttest_ind(churn_no, churn_yes, nan_policy='omit')
    
    print(f"\nT-Test Sonucu:")
    print(f"  t-statistic: {t_stat:.4f}")
    print(f"  p-value: {p_value:.4e}")
    
    if p_value < 0.001:
        significance = "Çok güçlü istatistiksel fark (p < 0.001)"
    elif p_value < 0.01:
        significance = "Güçlü istatistiksel fark (p < 0.01)"
    elif p_value < 0.05:
        significance = "Anlamlı istatistiksel fark (p < 0.05)"
    else:
        significance = "İstatistiksel fark yok (p >= 0.05)"
    
    print(f"  Yorum: {significance}")
    
    # Boxplot
    fig_box = px.box(
        df,
        x=target_col,
        y=col,
        color=target_col,
        color_discrete_map=CHURN_COLORS,
        title=f"{col} vs {target_col} - Boxplot Karşılaştırması"
    )
    fig_box = apply_premium_layout(fig_box, f"{col} vs {target_col} - Boxplot Karşılaştırması")
    save_figure(fig_box, f"phase3_boxplot_{col.lower()}_vs_churn")
    
    # Violin plot
    fig_violin = px.violin(
        df,
        x=target_col,
        y=col,
        color=target_col,
        color_discrete_map=CHURN_COLORS,
        title=f"{col} vs {target_col} - Violin Plot (Dağılım Karşılaştırması)",
        box=True,
        points="outliers"
    )
    fig_violin = apply_premium_layout(fig_violin, f"{col} vs {target_col} - Violin Plot")
    save_figure(fig_violin, f"phase3_violin_{col.lower()}_vs_churn")
    
    # Özet kaydet
    numeric_churn_summary.append({
        "Değişken": col,
        "Churn=No Ortalama": grouped_stats.loc['No', 'mean'],
        "Churn=Yes Ortalama": grouped_stats.loc['Yes', 'mean'],
        "Ortalama Farkı": round(grouped_stats.loc['Yes', 'mean'] - grouped_stats.loc['No', 'mean'], 2),
        "T-Statistic": round(t_stat, 4),
        "P-Value": round(p_value, 6),
        "İstatistiksel Anlamlılık": "Evet" if p_value < 0.05 else "Hayır"
    })

# CSV kaydet
numeric_churn_df = pd.DataFrame(numeric_churn_summary)
numeric_churn_df.to_csv('../reports/csv/phase3_numeric_vs_churn.csv', index=False)
print("\n✅ Sayısal vs Churn raporu: reports/csv/phase3_numeric_vs_churn.csv")

# ========================================================================
# KATEGORİK DEĞİŞKENLER vs CHURN
# ========================================================================

print("\n" + "="*80)
print("2. KATEGORİK DEĞİŞKENLER vs CHURN ANALİZİ")
print("="*80)

categorical_churn_summary = []

for col in categorical_cols:
    print(f"\n{'='*80}")
    print(f"Değişken: {col} vs {target_col}")
    print(f"{'='*80}")
    
    # Çapraz tablo (crosstab)
    crosstab = pd.crosstab(df[col], df[target_col], normalize='index') * 100
    crosstab = crosstab.round(2)
    
    print(f"\nChurn Oranları (% - Satır bazlı):")
    print(crosstab)
    
    # En yüksek ve en düşük churn oranı
    churn_yes_rates = crosstab['Yes'].sort_values(ascending=False)
    highest_churn_category = churn_yes_rates.index[0]
    highest_churn_rate = churn_yes_rates.iloc[0]
    lowest_churn_category = churn_yes_rates.index[-1]
    lowest_churn_rate = churn_yes_rates.iloc[-1]
    
    print(f"\nEn yüksek churn: {highest_churn_category} (%{highest_churn_rate})")
    print(f"En düşük churn: {lowest_churn_category} (%{lowest_churn_rate})")
    
    # Chi-square test
    contingency_table = pd.crosstab(df[col], df[target_col])
    chi2, p_value, dof, expected = stats.chi2_contingency(contingency_table)
    
    print(f"\nChi-Square Test:")
    print(f"  Chi2: {chi2:.4f}")
    print(f"  p-value: {p_value:.4e}")
    
    if p_value < 0.001:
        significance = "Çok güçlü ilişki (p < 0.001)"
    elif p_value < 0.01:
        significance = "Güçlü ilişki (p < 0.01)"
    elif p_value < 0.05:
        significance = "Anlamlı ilişki (p < 0.05)"
    else:
        significance = "İlişki yok (p >= 0.05)"
    
    print(f"  Yorum: {significance}")
    
    # Grouped bar chart
    crosstab_counts = pd.crosstab(df[col], df[target_col])
    crosstab_plot = crosstab_counts.reset_index().melt(id_vars=col, var_name='Churn', value_name='Frekans')
    
    fig_bar = px.bar(
        crosstab_plot,
        x=col,
        y='Frekans',
        color='Churn',
        color_discrete_map=CHURN_COLORS,
        barmode='group',
        title=f"{col} vs {target_col} - Grouped Bar Chart"
    )
    fig_bar = apply_premium_layout(fig_bar, f"{col} vs {target_col} - Grouped Bar Chart")
    save_figure(fig_bar, f"phase3_grouped_bar_{col.lower()}_vs_churn")
    
    # Churn rate bar chart
    churn_rate_df = crosstab['Yes'].reset_index()
    churn_rate_df.columns = [col, 'Churn Rate (%)']
    
    fig_rate = px.bar(
        churn_rate_df,
        x=col,
        y='Churn Rate (%)',
        color='Churn Rate (%)',
        color_continuous_scale=['#6A994E', '#F18F01', '#C73E1D'],
        title=f"{col} - Churn Oranı Karşılaştırması"
    )
    fig_rate = apply_premium_layout(fig_rate, f"{col} - Churn Oranı Karşılaştırması")
    save_figure(fig_rate, f"phase3_churn_rate_{col.lower()}")
    
    # Özet kaydet
    categorical_churn_summary.append({
        "Değişken": col,
        "En Yüksek Churn Kategori": highest_churn_category,
        "En Yüksek Churn Oranı (%)": highest_churn_rate,
        "En Düşük Churn Kategori": lowest_churn_category,
        "En Düşük Churn Oranı (%)": lowest_churn_rate,
        "Churn Oranı Farkı (%)": round(highest_churn_rate - lowest_churn_rate, 2),
        "Chi2": round(chi2, 4),
        "P-Value": round(p_value, 6),
        "İstatistiksel Anlamlılık": "Evet" if p_value < 0.05 else "Hayır"
    })
    
    # Yüksek churn farkı varsa Data Prep Expert için öneri
    if highest_churn_rate - lowest_churn_rate > 30:
        add_data_prep_recommendation(
            issue=f"{col} - Yüksek churn rate farkı",
            evidence=f"En yüksek churn (%{highest_churn_rate:.2f}) ve en düşük churn (%{lowest_churn_rate:.2f}) arasında %{(highest_churn_rate - lowest_churn_rate):.2f} fark var.",
            recommendation=f"Bu değişken churn için güçlü bir predictor. Feature engineering'de {col} bazlı etkileşim özellikleri oluşturulabilir.",
            priority="Yüksek"
        )

# CSV kaydet
categorical_churn_df = pd.DataFrame(categorical_churn_summary)
categorical_churn_df.to_csv('../reports/csv/phase3_categorical_vs_churn.csv', index=False)
print("\n✅ Kategorik vs Churn raporu: reports/csv/phase3_categorical_vs_churn.csv")

# ========================================================================
# DATA PREP EXPERT ÖNERİLERİ
# ========================================================================

if data_prep_recommendations:
    print("\n" + "="*80)
    print("3. DATA PREP EXPERT İÇİN ÖNERİLER")
    print("="*80)
    
    recommendations_df = pd.DataFrame(data_prep_recommendations)
    print(recommendations_df.to_string(index=False))
    
    recommendations_df.to_csv('../reports/csv/phase3_data_prep_recommendations.csv', index=False)
    print("\n✅ Data Prep önerileri: reports/csv/phase3_data_prep_recommendations.csv")

print("\n" + "="*80)
print("PHASE 3 TAMAMLANDI")
print(f"Toplam {len(numeric_cols)} sayısal ve {len(categorical_cols)} kategorik değişken Churn ile karşılaştırıldı")
print(f"Toplam {len(numeric_cols) * 2 + len(categorical_cols) * 2} grafik oluşturuldu")
print("="*80)
