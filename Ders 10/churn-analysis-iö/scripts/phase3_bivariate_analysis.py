# ================================================================
# PHASE 3: BIVARIATE ANALYSIS
# ================================================================
# Değişkenler arası ikili ilişkileri ve hedef değişkenle ilişkileri incelemek

import os
import warnings
from pathlib import Path
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from scipy import stats

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
print("PHASE 3: BIVARIATE ANALYSIS")
print("=" * 70)
print()

# Veri setini yükle
df = pd.read_csv('../data/raw/churn.csv')

# TotalCharges düzelt
if 'TotalCharges' in df.columns and df['TotalCharges'].dtype == 'object':
    df['TotalCharges'] = pd.to_numeric(df['TotalCharges'], errors='coerce')

print(f"✅ Veri seti yüklendi: {df.shape[0]} satır, {df.shape[1]} sütun\n")

# Sayısal ve kategorik ayrımı
numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
categorical_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()

# customerID çıkar
if 'customerID' in categorical_cols:
    categorical_cols.remove('customerID')

# Hedef değişken
target = 'Churn'

if target not in df.columns:
    print(f"⚠️  Hedef değişken '{target}' bulunamadı. Analiz durduruluyor.")
    exit()

# Hedef değişkeni kategoriklerden çıkar
if target in categorical_cols:
    categorical_cols.remove(target)

print("=" * 70)
print(f"A. SAYISAL DEĞİŞKENLER vs HEDEF ({target})")
print("=" * 70)
print()

numeric_vs_target_summary = []

for col in numeric_cols:
    print(f"📊 Analiz ediliyor: {col} vs {target}")
    print("-" * 70)
    
    # Grup bazlı istatistikler
    grouped = df.groupby(target)[col].agg(['mean', 'median', 'std', 'count'])
    print(grouped)
    print()
    
    # Boxplot
    fig_box = px.box(
        df,
        x=target,
        y=col,
        color=target,
        color_discrete_sequence=[PROFESSIONAL_PALETTE[0], PROFESSIONAL_PALETTE[1]],
        title=f"{col} Dağılımı ({target} Gruplarına Göre)"
    )
    fig_box = apply_premium_layout(fig_box, f"{col} Dağılımı ({target} Gruplarına Göre)")
    save_figure(fig_box, f"phase3_boxplot_{col}_vs_{target}")
    
    # Violin plot
    fig_violin = px.violin(
        df,
        x=target,
        y=col,
        color=target,
        box=True,
        color_discrete_sequence=[PROFESSIONAL_PALETTE[2], PROFESSIONAL_PALETTE[3]],
        title=f"{col} Violin Plot ({target} Gruplarına Göre)"
    )
    fig_violin = apply_premium_layout(fig_violin, f"{col} Violin Plot ({target} Gruplarına Göre)")
    save_figure(fig_violin, f"phase3_violin_{col}_vs_{target}")
    
    print()
    
    # T-testi
    churn_yes = df[df[target] == 'Yes'][col].dropna()
    churn_no = df[df[target] == 'No'][col].dropna()
    
    if len(churn_yes) > 0 and len(churn_no) > 0:
        t_stat, p_value = stats.ttest_ind(churn_yes, churn_no)
        print(f"  T-Test Sonucu:")
        print(f"    t-statistic: {t_stat:.4f}")
        print(f"    p-value: {p_value:.4f}")
        
        if p_value < 0.05:
            print(f"    ✅ {col} değişkeni {target} ile istatistiksel olarak anlamlı ilişkiye sahip (p<0.05)")
        else:
            print(f"    ⚠️  {col} değişkeni {target} ile istatistiksel olarak anlamlı ilişkiye sahip değil (p>=0.05)")
    
    print()
    
    # Özet kaydet
    numeric_vs_target_summary.append({
        'Değişken': col,
        'Churn=Yes Ortalama': round(churn_yes.mean(), 2) if len(churn_yes) > 0 else None,
        'Churn=No Ortalama': round(churn_no.mean(), 2) if len(churn_no) > 0 else None,
        'Fark (%)': round((churn_yes.mean() - churn_no.mean()) / churn_no.mean() * 100, 2) if len(churn_no) > 0 and churn_no.mean() != 0 else None,
        't-statistic': round(t_stat, 4) if len(churn_yes) > 0 and len(churn_no) > 0 else None,
        'p-value': round(p_value, 4) if len(churn_yes) > 0 and len(churn_no) > 0 else None,
        'Anlamlı': 'Evet' if (len(churn_yes) > 0 and len(churn_no) > 0 and p_value < 0.05) else 'Hayır'
    })

# Sayısal vs target özet kaydet
numeric_vs_target_df = pd.DataFrame(numeric_vs_target_summary)
numeric_vs_target_df.to_csv('../reports/csv/phase3_numeric_vs_target_summary.csv', index=False, encoding='utf-8-sig')
print(f"📄 Sayısal değişkenler vs {target} özet raporu kaydedildi\n")

print("=" * 70)
print(f"B. KATEGORİK DEĞİŞKENLER vs HEDEF ({target})")
print("=" * 70)
print()

categorical_vs_target_summary = []

for col in categorical_cols:
    print(f"📊 Analiz ediliyor: {col} vs {target}")
    print("-" * 70)
    
    # Çapraz tablo
    crosstab = pd.crosstab(df[col], df[target], normalize='index') * 100
    print("Satır Bazlı Yüzde Dağılım (%):")
    print(crosstab.round(2))
    print()
    
    # Grouped bar chart
    crosstab_counts = pd.crosstab(df[col], df[target])
    crosstab_reset = crosstab_counts.reset_index()
    crosstab_melted = crosstab_reset.melt(id_vars=col, var_name=target, value_name='Count')
    
    fig_bar = px.bar(
        crosstab_melted,
        x=col,
        y='Count',
        color=target,
        barmode='group',
        color_discrete_sequence=[PROFESSIONAL_PALETTE[4], PROFESSIONAL_PALETTE[5]],
        title=f"{col} ve {target} İlişkisi"
    )
    fig_bar = apply_premium_layout(fig_bar, f"{col} ve {target} İlişkisi")
    save_figure(fig_bar, f"phase3_grouped_bar_{col}_vs_{target}")
    
    # Stacked percentage bar
    fig_stacked = px.bar(
        crosstab.reset_index().melt(id_vars=col, var_name=target, value_name='Percentage'),
        x=col,
        y='Percentage',
        color=target,
        barmode='stack',
        color_discrete_sequence=[PROFESSIONAL_PALETTE[6], PROFESSIONAL_PALETTE[7]],
        title=f"{col} İçinde {target} Dağılımı (%)"
    )
    fig_stacked = apply_premium_layout(fig_stacked, f"{col} İçinde {target} Dağılımı (%)")
    save_figure(fig_stacked, f"phase3_stacked_bar_{col}_vs_{target}")
    
    print()
    
    # Chi-square test
    chi2, p_value_chi, dof, expected = stats.chi2_contingency(crosstab_counts)
    print(f"  Chi-Square Test Sonucu:")
    print(f"    chi2: {chi2:.4f}")
    print(f"    p-value: {p_value_chi:.4f}")
    print(f"    degrees of freedom: {dof}")
    
    if p_value_chi < 0.05:
        print(f"    ✅ {col} değişkeni {target} ile istatistiksel olarak anlamlı ilişkiye sahip (p<0.05)")
    else:
        print(f"    ⚠️  {col} değişkeni {target} ile istatistiksel olarak anlamlı ilişkiye sahip değil (p>=0.05)")
    
    print()
    
    # En yüksek churn oranına sahip kategori
    if 'Yes' in crosstab.columns:
        max_churn_category = crosstab['Yes'].idxmax()
        max_churn_rate = crosstab['Yes'].max()
        print(f"  🔍 En Yüksek Churn Oranı: {max_churn_category} (%{max_churn_rate:.2f})")
        print()
    
    # Özet kaydet
    categorical_vs_target_summary.append({
        'Değişken': col,
        'Eşsiz Kategori Sayısı': df[col].nunique(),
        'chi2': round(chi2, 4),
        'p-value': round(p_value_chi, 4),
        'Anlamlı': 'Evet' if p_value_chi < 0.05 else 'Hayır',
        'En Yüksek Churn Kategorisi': max_churn_category if 'Yes' in crosstab.columns else None,
        'En Yüksek Churn Oranı (%)': round(max_churn_rate, 2) if 'Yes' in crosstab.columns else None
    })

# Kategorik vs target özet kaydet
categorical_vs_target_df = pd.DataFrame(categorical_vs_target_summary)
categorical_vs_target_df.to_csv('../reports/csv/phase3_categorical_vs_target_summary.csv', index=False, encoding='utf-8-sig')
print(f"📄 Kategorik değişkenler vs {target} özet raporu kaydedildi\n")

print("=" * 70)
print("✅ PHASE 3 TAMAMLANDI")
print("=" * 70)
