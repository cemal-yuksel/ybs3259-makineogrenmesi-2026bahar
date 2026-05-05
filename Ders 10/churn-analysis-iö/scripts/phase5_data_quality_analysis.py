# ================================================================
# PHASE 5: DATA QUALITY & ANOMALY DETECTION
# ================================================================
# Veri kalitesi risklerini sistematik biçimde belirlemek

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
print("PHASE 5: DATA QUALITY & ANOMALY DETECTION")
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

print("=" * 70)
print("A. EKSİK VERİ ANALİZİ")
print("=" * 70)
print()

# Eksik veri hesapla
missing_count = df.isnull().sum()
missing_ratio = (missing_count / len(df) * 100).round(2)

missing_summary = pd.DataFrame({
    'Değişken': df.columns,
    'Eksik Değer Sayısı': missing_count.values,
    'Eksik Değer Oranı (%)': missing_ratio.values
}).sort_values('Eksik Değer Oranı (%)', ascending=False)

print("Eksik Veri Özeti:")
print(missing_summary.to_string(index=False))
print()

# Eksik veri görselleştirme
missing_plot_data = missing_summary[missing_summary['Eksik Değer Oranı (%)'] > 0].copy()

if len(missing_plot_data) > 0:
    print(f"⚠️  {len(missing_plot_data)} değişkende eksik veri tespit edildi.")
    print()
    
    fig_missing = px.bar(
        missing_plot_data,
        x='Eksik Değer Oranı (%)',
        y='Değişken',
        orientation='h',
        color='Eksik Değer Oranı (%)',
        color_continuous_scale=['#D5F5E3', '#F7D9A3', '#F6C6C6'],
        title="Değişken Bazında Eksik Veri Oranları"
    )
    fig_missing = apply_premium_layout(fig_missing, "Değişken Bazında Eksik Veri Oranları")
    save_figure(fig_missing, "phase5_missing_values")
    print()
    
    # Kritik eksik veri kontrolü
    risky_columns = missing_summary[missing_summary['Eksik Değer Oranı (%)'] > 30]
    if len(risky_columns) > 0:
        print("⚠️  Kritik Seviyede Eksik Veri:")
        for idx, row in risky_columns.iterrows():
            print(f"    {row['Değişken']}: %{row['Eksik Değer Oranı (%)']}")
            add_data_prep_recommendation(
                issue=f"{row['Değişken']} değişkeninde kritik seviyede eksik veri",
                evidence=f"Eksik veri oranı %{row['Eksik Değer Oranı (%)']}.",
                recommendation="Data Prep Expert bu değişken için domain temelli imputasyon, ileri imputasyon yöntemleri veya değişken çıkarma seçeneklerini değerlendirmelidir.",
                priority="Yüksek"
            )
        print()
    
    # Orta seviye eksik veri
    medium_missing = missing_summary[(missing_summary['Eksik Değer Oranı (%)'] > 5) & 
                                     (missing_summary['Eksik Değer Oranı (%)'] <= 30)]
    if len(medium_missing) > 0:
        print("⚠️  Orta Seviyede Eksik Veri:")
        for idx, row in medium_missing.iterrows():
            print(f"    {row['Değişken']}: %{row['Eksik Değer Oranı (%)']}")
            add_data_prep_recommendation(
                issue=f"{row['Değişken']} değişkeninde eksik veri",
                evidence=f"Eksik veri oranı %{row['Eksik Değer Oranı (%)']}.",
                recommendation="Data Prep Expert median/mode imputasyon, KNN imputasyon veya ileri yöntemler değerlendirmelidir.",
                priority="Orta"
            )
        print()
else:
    print("✅ Hiç eksik veri tespit edilmedi.")
    print()

# Eksik veri özet kaydet
missing_summary.to_csv('../reports/csv/phase5_missing_values_summary.csv', index=False, encoding='utf-8-sig')
print(f"📄 Eksik veri özet raporu kaydedildi\n")

print("=" * 70)
print("B. DUPLICATE ROW KONTROLÜ")
print("=" * 70)
print()

# Duplicate satırlar
duplicate_count = df.duplicated().sum()
duplicate_ratio = (duplicate_count / len(df) * 100).round(2)

print(f"Duplicate Satır Sayısı: {duplicate_count}")
print(f"Duplicate Satır Oranı: %{duplicate_ratio}")
print()

if duplicate_count > 0:
    print(f"⚠️  {duplicate_count} duplicate satır tespit edildi.")
    add_data_prep_recommendation(
        issue="Duplicate satırlar tespit edildi",
        evidence=f"{duplicate_count} adet duplicate satır bulundu (%{duplicate_ratio}).",
        recommendation="Data Prep Expert duplicate satırları temizlemeyi değerlendirmelidir. Gerçek duplicate mi yoksa veri girişi hatası mı incelenmeli.",
        priority="Yüksek"
    )
else:
    print("✅ Duplicate satır tespit edilmedi.")

print()

print("=" * 70)
print("C. IQR OUTLIER ANALİZİ")
print("=" * 70)
print()

outlier_records = []

for col in numeric_cols:
    q1 = df[col].quantile(0.25)
    q3 = df[col].quantile(0.75)
    iqr = q3 - q1
    
    lower_bound = q1 - 1.5 * iqr
    upper_bound = q3 + 1.5 * iqr
    
    outlier_count = ((df[col] < lower_bound) | (df[col] > upper_bound)).sum()
    outlier_ratio = (outlier_count / len(df) * 100).round(2)
    
    outlier_records.append({
        'Değişken': col,
        'Outlier Sayısı': outlier_count,
        'Outlier Oranı (%)': outlier_ratio,
        'Lower Bound': round(lower_bound, 2),
        'Upper Bound': round(upper_bound, 2)
    })
    
    if outlier_ratio > 5:
        add_data_prep_recommendation(
            issue=f"{col} değişkeninde yüksek outlier oranı",
            evidence=f"IQR yöntemine göre outlier oranı %{outlier_ratio}.",
            recommendation="Data Prep Expert winsorization, log dönüşümü, robust scaler veya outlier incelemesi yapmalıdır.",
            priority="Orta"
        )

outlier_summary_df = pd.DataFrame(outlier_records).sort_values('Outlier Oranı (%)', ascending=False)

print("IQR Outlier Özeti:")
print(outlier_summary_df.to_string(index=False))
print()

# Outlier görselleştirme
fig_outlier = px.bar(
    outlier_summary_df,
    x='Outlier Oranı (%)',
    y='Değişken',
    orientation='h',
    color='Outlier Oranı (%)',
    color_continuous_scale=['#D5F5E3', '#F7D9A3', '#F6C6C6'],
    title="Sayısal Değişkenlerde Outlier Oranları (IQR Yöntemi)"
)
fig_outlier = apply_premium_layout(fig_outlier, "Sayısal Değişkenlerde Outlier Oranları (IQR Yöntemi)")
save_figure(fig_outlier, "phase5_outlier_ratios")
print()

# Outlier özet kaydet
outlier_summary_df.to_csv('../reports/csv/phase5_outlier_summary.csv', index=False, encoding='utf-8-sig')
print(f"📄 Outlier özet raporu kaydedildi\n")

print("=" * 70)
print("D. Z-SCORE OUTLIER ANALİZİ")
print("=" * 70)
print()

z_outlier_records = []

for col in numeric_cols:
    z_scores = np.abs(stats.zscore(df[col].dropna()))
    z_outlier_count = (z_scores > 3).sum()
    z_outlier_ratio = (z_outlier_count / len(df) * 100).round(2)
    
    z_outlier_records.append({
        'Değişken': col,
        'Z-Score Outlier Sayısı': z_outlier_count,
        'Z-Score Outlier Oranı (%)': z_outlier_ratio
    })

z_outlier_df = pd.DataFrame(z_outlier_records).sort_values('Z-Score Outlier Oranı (%)', ascending=False)

print("Z-Score Outlier Özeti (|z| > 3):")
print(z_outlier_df.to_string(index=False))
print()

# Z-score özet kaydet
z_outlier_df.to_csv('../reports/csv/phase5_z_score_outlier_summary.csv', index=False, encoding='utf-8-sig')
print(f"📄 Z-Score outlier özet raporu kaydedildi\n")

print("=" * 70)
print("E. KATEGORİK DEĞİŞKEN TUTARLILIK KONTROLÜ")
print("=" * 70)
print()

# customerID çıkar
if 'customerID' in categorical_cols:
    categorical_cols.remove('customerID')

# Tutarlılık sorunları
print("Kategorik Değişken Eşsiz Değer Kontrolü:")
for col in categorical_cols:
    unique_count = df[col].nunique()
    print(f"  {col}: {unique_count} eşsiz değer")

print()

# Veri tutarlılığı için özel kontroller
print("=" * 70)
print("F. ÖZEL VERİ TUTARLILIK KONTROLLARI")
print("=" * 70)
print()

# Negatif değer kontrolü
print("Negatif Değer Kontrolü (Sayısal Değişkenler):")
for col in numeric_cols:
    negative_count = (df[col] < 0).sum()
    if negative_count > 0:
        print(f"  ⚠️  {col}: {negative_count} adet negatif değer")
        add_data_prep_recommendation(
            issue=f"{col} değişkeninde negatif değer",
            evidence=f"{negative_count} adet negatif değer tespit edildi.",
            recommendation="Data Prep Expert bu değerlerin mantıksal olup olmadığını kontrol etmeli ve gerekirse düzeltme yapmalıdır.",
            priority="Yüksek"
        )
    else:
        print(f"  ✅ {col}: Negatif değer yok")

print()

# Data Prep önerileri kaydet
if len(data_prep_recommendations) > 0:
    recommendations_df = pd.DataFrame(data_prep_recommendations)
    recommendations_df.to_csv('../reports/csv/phase5_data_prep_recommendations.csv', index=False, encoding='utf-8-sig')
    print(f"📄 Data Prep Expert için {len(data_prep_recommendations)} öneri kaydedildi.\n")

print("=" * 70)
print("✅ PHASE 5 TAMAMLANDI")
print("=" * 70)
