# PHASE 2: UNIVARIATE ANALYSIS
# Her değişkenin tekil davranışını inceleme

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
        print(f"⚠ PNG kaydı yapılamadı (kaleido gerekebilir)")

print("="*80)
print("PHASE 2: UNIVARIATE ANALYSIS")
print("="*80)
print()

# Veriyi yükle
df = pd.read_csv('../data/raw/diabetes.csv')
print(f"✓ Veri yüklendi: {df.shape[0]} satır, {df.shape[1]} sütun")
print()

# Sayısal değişkenleri belirle (Outcome hariç)
numeric_columns = [col for col in df.select_dtypes(include=[np.number]).columns if col != 'Outcome']

print(f"📊 Analiz edilecek sayısal değişken sayısı: {len(numeric_columns)}")
print(f"Değişkenler: {numeric_columns}")
print()

# Her değişken için univariate analiz
univariate_summary = []

for col in numeric_columns:
    print(f"\n{'='*60}")
    print(f"Değişken: {col}")
    print(f"{'='*60}")
    
    # Temel istatistikler
    mean_val = df[col].mean()
    median_val = df[col].median()
    std_val = df[col].std()
    min_val = df[col].min()
    max_val = df[col].max()
    
    # Skewness ve Kurtosis
    skewness = df[col].skew()
    kurtosis = df[col].kurtosis()
    
    # IQR ve outlier kontrolü
    q1 = df[col].quantile(0.25)
    q3 = df[col].quantile(0.75)
    iqr = q3 - q1
    lower_bound = q1 - 1.5 * iqr
    upper_bound = q3 + 1.5 * iqr
    
    outlier_count = ((df[col] < lower_bound) | (df[col] > upper_bound)).sum()
    outlier_ratio = (outlier_count / len(df) * 100)
    
    # 0 değerlerini say (gizli eksik veri kontrolü)
    zero_count = (df[col] == 0).sum()
    zero_ratio = (zero_count / len(df) * 100)
    
    print(f"Ortalama: {mean_val:.2f}")
    print(f"Medyan: {median_val:.2f}")
    print(f"Standart Sapma: {std_val:.2f}")
    print(f"Min: {min_val:.2f}, Max: {max_val:.2f}")
    print(f"Skewness: {skewness:.3f}")
    print(f"Kurtosis: {kurtosis:.3f}")
    print(f"Outlier Sayısı (IQR): {outlier_count} (%{outlier_ratio:.2f})")
    print(f"Sıfır Değer Sayısı: {zero_count} (%{zero_ratio:.2f})")
    
    # Histogram
    fig = px.histogram(
        df, 
        x=col,
        nbins=30,
        title=f"{col} Dağılımı",
        color_discrete_sequence=[PROFESSIONAL_PALETTE[0]]
    )
    fig = apply_premium_layout(fig, f"{col} Dağılımı (Histogram)")
    fig.update_xaxes(title_text=col, title_font=dict(size=14, family="Arial", color="#1F2937"))
    fig.update_yaxes(title_text="Frekans", title_font=dict(size=14, family="Arial", color="#1F2937"))
    save_figure(fig, f"phase2_histogram_{col.lower()}")
    
    # Boxplot
    fig = go.Figure()
    fig.add_trace(go.Box(
        y=df[col],
        name=col,
        marker_color=PROFESSIONAL_PALETTE[1],
        boxmean='sd'
    ))
    fig = apply_premium_layout(fig, f"{col} Boxplot (Outlier Görünümü)")
    fig.update_yaxes(title_text=col, title_font=dict(size=14, family="Arial", color="#1F2937"))
    save_figure(fig, f"phase2_boxplot_{col.lower()}")
    
    # Özet tabloya ekle
    univariate_summary.append({
        'Değişken': col,
        'Ortalama': round(mean_val, 2),
        'Medyan': round(median_val, 2),
        'Std': round(std_val, 2),
        'Min': round(min_val, 2),
        'Max': round(max_val, 2),
        'Skewness': round(skewness, 3),
        'Kurtosis': round(kurtosis, 3),
        'Outlier Sayısı': outlier_count,
        'Outlier Oranı (%)': round(outlier_ratio, 2),
        'Sıfır Değer Sayısı': zero_count,
        'Sıfır Oranı (%)': round(zero_ratio, 2)
    })
    
    # Data Prep önerileri
    if abs(skewness) > 1:
        add_data_prep_recommendation(
            issue=f"{col} değişkeninde yüksek çarpıklık",
            evidence=f"Skewness değeri {skewness:.3f} (|skewness| > 1).",
            recommendation=f"Data Prep Expert, {col} için log, Box-Cox veya Yeo-Johnson dönüşümü değerlendirmelidir.",
            priority="Orta"
        )
    
    if outlier_ratio > 5:
        add_data_prep_recommendation(
            issue=f"{col} değişkeninde yüksek outlier oranı",
            evidence=f"IQR yöntemine göre outlier oranı %{outlier_ratio:.2f}.",
            recommendation=f"Data Prep Expert, {col} için winsorization, log dönüşümü veya robust scaler değerlendirmelidir.",
            priority="Orta"
        )
    
    # Gizli eksik veri kontrolü
    if col in ['Glucose', 'BloodPressure', 'SkinThickness', 'Insulin', 'BMI'] and zero_ratio > 0:
        add_data_prep_recommendation(
            issue=f"{col} değişkeninde mantıksal olarak imkansız 0 değerleri (gizli eksik veri)",
            evidence=f"0 değer sayısı: {zero_count} (%{zero_ratio:.2f}). Bu değişkende 0 değeri mantıksal olarak imkansızdır.",
            recommendation=f"Data Prep Expert, {col} için 0 değerlerini NaN'a dönüştürmeli ve uygun imputasyon stratejisi (median, mean, KNN, iterative) uygulamalıdır.",
            priority="Yüksek"
        )

print("\n" + "="*80)

# Özet tabloyu kaydet
summary_df = pd.DataFrame(univariate_summary)
summary_df.to_csv('../reports/csv/phase2_univariate_summary.csv', index=False)
print("\n✓ Univariate özet rapor kaydedildi: reports/csv/phase2_univariate_summary.csv")

# Data Prep önerilerini kaydet
if len(data_prep_recommendations) > 0:
    recommendations_df = pd.DataFrame(data_prep_recommendations)
    recommendations_df.to_csv('../reports/csv/phase2_data_prep_recommendations.csv', index=False)
    print(f"✓ {len(data_prep_recommendations)} adet Data Prep önerisi kaydedildi.")
    print("\nData Prep Önerileri:")
    for i, rec in enumerate(data_prep_recommendations, 1):
        print(f"{i}. [{rec['Öncelik']}] {rec['Sorun']}")

print("\n" + "="*80)
print("PHASE 2 TAMAMLANDI")
print("="*80)
