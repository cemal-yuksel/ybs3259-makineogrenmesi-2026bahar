"""
PHASE 2: UNIVARIATE ANALYSIS
Her değişkenin tek başına davranışını anlamak
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

# Profesyonel renk paleti (net ve etkili tonlar - beyaz arka planda mükemmel görünür)
PROFESSIONAL_PALETTE = [
    "#2E86AB",  # Koyu mavi - güven, profesyonellik
    "#A23B72",  # Koyu pembe/mor - vurgu, önem
    "#F18F01",  # Turuncu - enerji, dikkat
    "#C73E1D",  # Koyu kırmızı - aciliyet, kritik
    "#6A994E",  # Orman yeşili - büyüme, pozitif
    "#BC4B51",  # Bordo - lüks, ciddiyet
    "#8E7DBE",  # Mor - yaratıcılık, premium
    "#F77F00",  # Koyu turuncu - eylem
    "#06A77D",  # Turkuaz - modern, teknoloji
    "#D4A574"   # Altın-bronz - değer, prestij
]

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
    """Profesyonel, net ve görkemli grafik düzeni uygula"""
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
    fig.update_xaxes(
        showgrid=True,
        gridcolor="#E5E7EB",
        zeroline=False
    )
    fig.update_yaxes(
        showgrid=True,
        gridcolor="#E5E7EB",
        zeroline=False
    )
    return fig

def save_figure(fig, file_base):
    """Grafik kaydet (HTML formatında)"""
    html_path = f"../figures/{file_base}.html"
    fig.write_html(html_path)
    print(f"  ✅ Grafik kaydedildi: {file_base}.html")
    return html_path

# Veri setini yükle
print("="*80)
print("PHASE 2: UNIVARIATE ANALYSIS")
print("="*80)

df = pd.read_csv('../data/raw/churn.csv')

# Sayısal ve kategorik değişkenleri ayır
numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
categorical_cols = df.select_dtypes(include=['object']).columns.tolist()

# customerID'yi kategorik listeden çıkar (ID değişkeni)
if 'customerID' in categorical_cols:
    categorical_cols.remove('customerID')
    print("\n⚠️ customerID değişkeni analizden çıkarıldı (ID değişkeni)")

print(f"\n📊 Analiz edilecek sayısal değişken sayısı: {len(numeric_cols)}")
print(f"📊 Analiz edilecek kategorik değişken sayısı: {len(categorical_cols)}")

# ========================================================================
# SAYISAL DEĞİŞKENLER ANALİZİ
# ========================================================================

print("\n" + "="*80)
print("1. SAYISAL DEĞİŞKENLER - UNİVARİATE ANALİZ")
print("="*80)

numeric_summary = []

for col in numeric_cols:
    print(f"\n{'='*80}")
    print(f"Değişken: {col}")
    print(f"{'='*80}")
    
    # İstatistiksel özetler
    mean_val = df[col].mean()
    median_val = df[col].median()
    std_val = df[col].std()
    min_val = df[col].min()
    max_val = df[col].max()
    
    # Skewness ve Kurtosis
    skewness = df[col].skew()
    kurtosis_val = df[col].kurtosis()
    
    # IQR ve outlier analizi
    q1 = df[col].quantile(0.25)
    q3 = df[col].quantile(0.75)
    iqr = q3 - q1
    lower_bound = q1 - 1.5 * iqr
    upper_bound = q3 + 1.5 * iqr
    outlier_count = ((df[col] < lower_bound) | (df[col] > upper_bound)).sum()
    outlier_ratio = (outlier_count / len(df) * 100)
    
    print(f"Ortalama: {mean_val:.2f}")
    print(f"Medyan: {median_val:.2f}")
    print(f"Std. Sapma: {std_val:.2f}")
    print(f"Min: {min_val:.2f} | Max: {max_val:.2f}")
    print(f"Skewness: {skewness:.3f}")
    print(f"Kurtosis: {kurtosis_val:.3f}")
    print(f"IQR Outlier Sayısı: {outlier_count} (%{outlier_ratio:.2f})")
    
    # Skewness yorumu
    if abs(skewness) > 1:
        skew_interpretation = "Yüksek çarpıklık - Dönüşüm önerilir"
        add_data_prep_recommendation(
            issue=f"{col} - Yüksek çarpıklık",
            evidence=f"Skewness: {skewness:.3f}",
            recommendation="Log, Box-Cox veya Yeo-Johnson dönüşümü değerlendirilmelidir.",
            priority="Orta"
        )
    elif abs(skewness) > 0.5:
        skew_interpretation = "Orta çarpıklık - İzlenmeli"
    else:
        skew_interpretation = "Düşük çarpıklık - Normal dağılıma yakın"
    
    print(f"Çarpıklık Yorumu: {skew_interpretation}")
    
    # Outlier yorumu
    if outlier_ratio > 5:
        add_data_prep_recommendation(
            issue=f"{col} - Yüksek outlier oranı",
            evidence=f"Outlier oranı: %{outlier_ratio:.2f}",
            recommendation="Winsorization, robust scaler veya log dönüşümü değerlendirilmelidir.",
            priority="Orta"
        )
    
    # Histogram
    fig_hist = px.histogram(
        df, 
        x=col,
        nbins=30,
        title=f"{col} - Dağılım Grafiği",
        color_discrete_sequence=[PROFESSIONAL_PALETTE[0]],
        labels={col: col}
    )
    fig_hist = apply_premium_layout(fig_hist, f"{col} - Dağılım Grafiği")
    save_figure(fig_hist, f"phase2_histogram_{col.lower()}")
    
    # Boxplot
    fig_box = px.box(
        df,
        y=col,
        title=f"{col} - Boxplot (Outlier Tespiti)",
        color_discrete_sequence=[PROFESSIONAL_PALETTE[1]]
    )
    fig_box = apply_premium_layout(fig_box, f"{col} - Boxplot (Outlier Tespiti)")
    save_figure(fig_box, f"phase2_boxplot_{col.lower()}")
    
    # Özet kaydet
    numeric_summary.append({
        "Değişken": col,
        "Ortalama": round(mean_val, 2),
        "Medyan": round(median_val, 2),
        "Std. Sapma": round(std_val, 2),
        "Min": round(min_val, 2),
        "Max": round(max_val, 2),
        "Skewness": round(skewness, 3),
        "Kurtosis": round(kurtosis_val, 3),
        "Outlier Sayısı": outlier_count,
        "Outlier Oranı (%)": round(outlier_ratio, 2)
    })

# Sayısal özet CSV kaydet
numeric_summary_df = pd.DataFrame(numeric_summary)
numeric_summary_df.to_csv('../reports/csv/phase2_numeric_summary.csv', index=False)
print("\n✅ Sayısal değişken özet raporu: reports/csv/phase2_numeric_summary.csv")

# ========================================================================
# KATEGORİK DEĞİŞKENLER ANALİZİ
# ========================================================================

print("\n" + "="*80)
print("2. KATEGORİK DEĞİŞKENLER - UNİVARİATE ANALİZ")
print("="*80)

categorical_summary = []

for col in categorical_cols:
    print(f"\n{'='*80}")
    print(f"Değişken: {col}")
    print(f"{'='*80}")
    
    # Frekans tablosu
    freq_table = df[col].value_counts()
    freq_ratio = (df[col].value_counts(normalize=True) * 100).round(2)
    unique_count = df[col].nunique()
    
    # Baskın kategori
    dominant_category = freq_table.index[0]
    dominant_ratio = freq_ratio.iloc[0]
    
    print(f"Eşsiz kategori sayısı: {unique_count}")
    print(f"Baskın kategori: {dominant_category} (%{dominant_ratio})")
    print("\nFrekans Tablosu:")
    print(pd.DataFrame({
        "Kategori": freq_table.index,
        "Frekans": freq_table.values,
        "Oran (%)": freq_ratio.values
    }).to_string(index=False))
    
    # Yüksek kardinalite kontrolü
    if unique_count > 30:
        add_data_prep_recommendation(
            issue=f"{col} - Yüksek kardinalite",
            evidence=f"Eşsiz kategori sayısı: {unique_count}",
            recommendation="Rare label encoding, target encoding veya frequency encoding değerlendirilmelidir.",
            priority="Yüksek"
        )
    
    # Bar chart
    freq_df = pd.DataFrame({
        col: freq_table.index,
        "Frekans": freq_table.values
    })
    
    fig_bar = px.bar(
        freq_df,
        x=col if unique_count <= 10 else "Frekans",
        y="Frekans" if unique_count <= 10 else col,
        orientation="v" if unique_count <= 10 else "h",
        title=f"{col} - Frekans Dağılımı",
        color=col,
        color_discrete_sequence=PROFESSIONAL_PALETTE
    )
    fig_bar = apply_premium_layout(fig_bar, f"{col} - Frekans Dağılımı")
    save_figure(fig_bar, f"phase2_barplot_{col.lower()}")
    
    # Özet kaydet
    categorical_summary.append({
        "Değişken": col,
        "Eşsiz Kategori": unique_count,
        "Baskın Kategori": dominant_category,
        "Baskın Oran (%)": dominant_ratio,
        "En Az Frekans": freq_table.min(),
        "En Çok Frekans": freq_table.max()
    })

# Kategorik özet CSV kaydet
categorical_summary_df = pd.DataFrame(categorical_summary)
categorical_summary_df.to_csv('../reports/csv/phase2_categorical_summary.csv', index=False)
print("\n✅ Kategorik değişken özet raporu: reports/csv/phase2_categorical_summary.csv")

# ========================================================================
# DATA PREP EXPERT ÖNERİLERİ
# ========================================================================

if data_prep_recommendations:
    print("\n" + "="*80)
    print("3. DATA PREP EXPERT İÇİN ÖNERİLER")
    print("="*80)
    
    recommendations_df = pd.DataFrame(data_prep_recommendations)
    print(recommendations_df.to_string(index=False))
    
    recommendations_df.to_csv('../reports/csv/phase2_data_prep_recommendations.csv', index=False)
    print("\n✅ Data Prep önerileri: reports/csv/phase2_data_prep_recommendations.csv")

print("\n" + "="*80)
print("PHASE 2 TAMAMLANDI")
print(f"Toplam {len(numeric_cols)} sayısal ve {len(categorical_cols)} kategorik değişken analiz edildi")
print(f"Toplam {len(numeric_cols) * 2 + len(categorical_cols)} grafik oluşturuldu")
print("="*80)
