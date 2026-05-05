# ================================================================
# PHASE 2: UNIVARIATE ANALYSIS
# ================================================================
# Her değişkenin tek başına davranışını incelemek

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
print("PHASE 2: UNIVARIATE ANALYSIS")
print("=" * 70)
print()

# Veri setini yükle
df = pd.read_csv('../data/raw/churn.csv')
print(f"✅ Veri seti yüklendi: {df.shape[0]} satır, {df.shape[1]} sütun\n")

# Sayısal ve kategorik ayrımı
numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
categorical_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()

# customerID modelleme için kullanılmamalı - çıkar
if 'customerID' in categorical_cols:
    categorical_cols.remove('customerID')

# TotalCharges numeric olmalı ama object - düzelt
if 'TotalCharges' in df.columns and df['TotalCharges'].dtype == 'object':
    print("⚠️  TotalCharges değişkeni 'object' tipinde tespit edildi.")
    print("    Sayısal değere dönüştürülüyor...")
    df['TotalCharges'] = pd.to_numeric(df['TotalCharges'], errors='coerce')
    numeric_cols.append('TotalCharges')
    if 'TotalCharges' in categorical_cols:
        categorical_cols.remove('TotalCharges')
    print(f"    ✅ TotalCharges sayısal değişkene dönüştürüldü. NaN sayısı: {df['TotalCharges'].isna().sum()}\n")
    
    if df['TotalCharges'].isna().sum() > 0:
        add_data_prep_recommendation(
            issue="TotalCharges değişkeninde eksik veri",
            evidence=f"TotalCharges değişkeninde {df['TotalCharges'].isna().sum()} adet eksik değer tespit edildi.",
            recommendation="Data Prep Expert tenure ve MonthlyCharges kullanarak imputasyon stratejisi geliştirmelidir.",
            priority="Orta"
        )

print("=" * 70)
print("A. SAYISAL DEĞİŞKENLER ANALİZİ")
print("=" * 70)
print()

univariate_numeric_summary = []

for col in numeric_cols:
    print(f"📊 Analiz ediliyor: {col}")
    print("-" * 70)
    
    # İstatistikler
    mean_val = df[col].mean()
    median_val = df[col].median()
    std_val = df[col].std()
    skewness = df[col].skew()
    kurtosis_val = df[col].kurtosis()
    
    # IQR Outlier
    q1 = df[col].quantile(0.25)
    q3 = df[col].quantile(0.75)
    iqr = q3 - q1
    lower_bound = q1 - 1.5 * iqr
    upper_bound = q3 + 1.5 * iqr
    outlier_count = ((df[col] < lower_bound) | (df[col] > upper_bound)).sum()
    outlier_ratio = outlier_count / len(df) * 100
    
    print(f"  Ortalama: {mean_val:.2f}")
    print(f"  Medyan: {median_val:.2f}")
    print(f"  Std Sapma: {std_val:.2f}")
    print(f"  Skewness: {skewness:.2f}")
    print(f"  Kurtosis: {kurtosis_val:.2f}")
    print(f"  IQR Outlier Sayısı: {outlier_count}")
    print(f"  IQR Outlier Oranı: {outlier_ratio:.2f}%")
    print()
    
    # Histogram
    fig_hist = px.histogram(
        df, 
        x=col, 
        nbins=50,
        color_discrete_sequence=[PROFESSIONAL_PALETTE[0]],
        title=f"{col} Değişkeni Dağılımı (Histogram)"
    )
    fig_hist = apply_premium_layout(fig_hist, f"{col} Değişkeni Dağılımı (Histogram)")
    save_figure(fig_hist, f"phase2_histogram_{col}")
    
    # Boxplot
    fig_box = px.box(
        df, 
        y=col,
        color_discrete_sequence=[PROFESSIONAL_PALETTE[1]],
        title=f"{col} Değişkeni Boxplot"
    )
    fig_box = apply_premium_layout(fig_box, f"{col} Değişkeni Boxplot")
    save_figure(fig_box, f"phase2_boxplot_{col}")
    
    print()
    
    # Özet kaydet
    univariate_numeric_summary.append({
        'Değişken': col,
        'Ortalama': round(mean_val, 2),
        'Medyan': round(median_val, 2),
        'Std Sapma': round(std_val, 2),
        'Skewness': round(skewness, 2),
        'Kurtosis': round(kurtosis_val, 2),
        'Outlier Sayısı': outlier_count,
        'Outlier Oranı (%)': round(outlier_ratio, 2)
    })
    
    # Agent etkileşimi
    if abs(skewness) > 1:
        add_data_prep_recommendation(
            issue=f"{col} değişkeninde yüksek çarpıklık",
            evidence=f"Skewness değeri {skewness:.2f} olarak hesaplandı.",
            recommendation="Data Prep Expert log, Box-Cox veya Yeo-Johnson dönüşümü değerlendirmelidir.",
            priority="Orta"
        )
    
    if outlier_ratio > 5:
        add_data_prep_recommendation(
            issue=f"{col} değişkeninde yüksek outlier oranı",
            evidence=f"IQR yöntemine göre outlier oranı %{outlier_ratio:.2f}.",
            recommendation="Data Prep Expert winsorization, log dönüşümü veya robust scaler değerlendirmelidir.",
            priority="Orta"
        )

# Sayısal özet kaydet
numeric_summary_df = pd.DataFrame(univariate_numeric_summary)
numeric_summary_df.to_csv('../reports/csv/phase2_univariate_numeric_summary.csv', index=False, encoding='utf-8-sig')
print(f"📄 Sayısal değişkenler özet raporu kaydedildi: ../reports/csv/phase2_univariate_numeric_summary.csv\n")

print("=" * 70)
print("B. KATEGORİK DEĞİŞKENLER ANALİZİ")
print("=" * 70)
print()

univariate_categorical_summary = []

for col in categorical_cols:
    print(f"📊 Analiz ediliyor: {col}")
    print("-" * 70)
    
    # Frekans tablosu
    freq_table = df[col].value_counts()
    ratio_table = (df[col].value_counts(normalize=True) * 100).round(2)
    n_unique = df[col].nunique()
    dominant_category = freq_table.index[0]
    dominant_ratio = ratio_table.iloc[0]
    
    print(f"  Eşsiz Kategori Sayısı: {n_unique}")
    print(f"  Baskın Kategori: {dominant_category} (%{dominant_ratio})")
    print(f"\n  Frekans Tablosu:")
    freq_df = pd.DataFrame({
        'Kategori': freq_table.index,
        'Frekans': freq_table.values,
        'Oran (%)': ratio_table.values
    })
    print(freq_df.to_string(index=False))
    print()
    
    # Bar chart
    fig_bar = px.bar(
        freq_df,
        x='Kategori',
        y='Frekans',
        color='Kategori',
        color_discrete_sequence=PROFESSIONAL_PALETTE,
        title=f"{col} Değişkeni Dağılımı"
    )
    fig_bar = apply_premium_layout(fig_bar, f"{col} Değişkeni Dağılımı")
    save_figure(fig_bar, f"phase2_barplot_{col}")
    
    print()
    
    # Özet kaydet
    univariate_categorical_summary.append({
        'Değişken': col,
        'Eşsiz Kategori Sayısı': n_unique,
        'Baskın Kategori': dominant_category,
        'Baskın Kategori Oranı (%)': dominant_ratio
    })
    
    # Agent etkileşimi
    if n_unique > 30:
        add_data_prep_recommendation(
            issue=f"{col} değişkeninde yüksek kardinalite",
            evidence=f"Eşsiz kategori sayısı {n_unique}.",
            recommendation="Data Prep Expert rare label encoding veya target encoding değerlendirmelidir.",
            priority="Orta"
        )
    
    if dominant_ratio > 80:
        add_data_prep_recommendation(
            issue=f"{col} değişkeninde aşırı dengesizlik",
            evidence=f"Baskın kategori oranı %{dominant_ratio}.",
            recommendation="Data Prep Expert bu değişkenin modellemeye katkısını değerlendirmeli veya özel encoding stratejisi uygulamalıdır.",
            priority="Düşük"
        )

# Kategorik özet kaydet
categorical_summary_df = pd.DataFrame(univariate_categorical_summary)
categorical_summary_df.to_csv('../reports/csv/phase2_univariate_categorical_summary.csv', index=False, encoding='utf-8-sig')
print(f"📄 Kategorik değişkenler özet raporu kaydedildi: ../reports/csv/phase2_univariate_categorical_summary.csv\n")

# Data Prep önerileri kaydet
if len(data_prep_recommendations) > 0:
    recommendations_df = pd.DataFrame(data_prep_recommendations)
    recommendations_df.to_csv('../reports/csv/phase2_data_prep_recommendations.csv', index=False, encoding='utf-8-sig')
    print(f"📄 Data Prep Expert için {len(data_prep_recommendations)} öneri kaydedildi.\n")

print("=" * 70)
print("✅ PHASE 2 TAMAMLANDI")
print("=" * 70)
