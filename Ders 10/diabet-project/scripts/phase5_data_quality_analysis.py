# PHASE 5: DATA QUALITY & ANOMALY DETECTION
# Veri kalitesi risklerini sistematik biçimde belirlemek

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
print("PHASE 5: DATA QUALITY & ANOMALY DETECTION")
print("="*80)
print()

# Veriyi yükle
df = pd.read_csv('../data/raw/diabetes.csv')
print(f"✓ Veri yüklendi: {df.shape[0]} satır, {df.shape[1]} sütun")
print()

# 1. EKSİK VERİ ANALİZİ (Teknik + Gizli)
print("="*80)
print("1. EKSİK VERİ ANALİZİ")
print("="*80)
print()

# Teknik eksik veri (NaN)
missing_count = df.isnull().sum()
missing_ratio = (missing_count / len(df) * 100).round(2)

print("📋 Teknik Eksik Veri (NaN):")
if missing_count.sum() == 0:
    print("✓ Teknik eksik veri bulunmamaktadır.")
else:
    print(missing_count[missing_count > 0])
print()

# Gizli eksik veri (0 değerleri)
print("🚨 Gizli Eksik Veri (0 Değerleri):")
print()

zero_columns = ['Glucose', 'BloodPressure', 'SkinThickness', 'Insulin', 'BMI']
zero_analysis = []

for col in zero_columns:
    zero_count = (df[col] == 0).sum()
    zero_ratio = (zero_count / len(df) * 100)
    
    zero_analysis.append({
        'Değişken': col,
        'Sıfır Sayısı': zero_count,
        'Sıfır Oranı (%)': round(zero_ratio, 2)
    })
    
    print(f"{col}:")
    print(f"  Sıfır Sayısı: {zero_count} (%{zero_ratio:.2f})")
    
    # Kritiklik seviyesi belirle
    if zero_ratio > 40:
        kritiklik = "🚨 ÇOK KRİTİK"
        priority = "Yüksek"
        add_data_prep_recommendation(
            issue=f"{col} değişkeninde çok yüksek oranda gizli eksik veri",
            evidence=f"0 değer oranı: %{zero_ratio:.2f}. Bu değişkende 0 değeri mantıksal olarak imkansızdır.",
            recommendation=f"Data Prep Expert, {col} için iki alternatif değerlendirmelidir:\n  1. Bu değişkeni modelden çıkar (önerilen)\n  2. İleri imputasyon (IterativeImputer) uygula, ancak overfitting riski yüksek.",
            priority=priority
        )
    elif zero_ratio > 20:
        kritiklik = "⚠️ KRİTİK"
        priority = "Yüksek"
        add_data_prep_recommendation(
            issue=f"{col} değişkeninde yüksek oranda gizli eksik veri",
            evidence=f"0 değer oranı: %{zero_ratio:.2f}. Bu değişkende 0 değeri mantıksal olarak imkansızdır.",
            recommendation=f"Data Prep Expert, {col} için 0 değerlerini NaN'a dönüştürüp IterativeImputer veya KNN Imputer kullanmalıdır. Alternatif olarak değişken modelden çıkarılabilir.",
            priority=priority
        )
    elif zero_ratio > 5:
        kritiklik = "⚠️ ORTA"
        priority = "Orta"
        add_data_prep_recommendation(
            issue=f"{col} değişkeninde orta düzeyde gizli eksik veri",
            evidence=f"0 değer oranı: %{zero_ratio:.2f}. Bu değişkende 0 değeri mantıksal olarak imkansızdır.",
            recommendation=f"Data Prep Expert, {col} için 0 değerlerini NaN'a dönüştürüp median veya KNN Imputer (k=5) kullanmalıdır.",
            priority=priority
        )
    else:
        kritiklik = "✓ DÜŞÜK"
        priority = "Düşük"
        add_data_prep_recommendation(
            issue=f"{col} değişkeninde düşük oranda gizli eksik veri",
            evidence=f"0 değer oranı: %{zero_ratio:.2f}. Bu değişkende 0 değeri mantıksal olarak imkansızdır.",
            recommendation=f"Data Prep Expert, {col} için 0 değerlerini NaN'a dönüştürüp median imputation yapmalıdır.",
            priority=priority
        )
    
    print(f"  Kritiklik: {kritiklik}")
    print()

# Gizli eksik veri görselleştirme
zero_df = pd.DataFrame(zero_analysis).sort_values('Sıfır Oranı (%)', ascending=True)

fig = go.Figure(data=[
    go.Bar(
        x=zero_df['Sıfır Oranı (%)'],
        y=zero_df['Değişken'],
        orientation='h',
        marker_color=[
            PROFESSIONAL_PALETTE[3] if x > 40 else 
            PROFESSIONAL_PALETTE[2] if x > 20 else 
            PROFESSIONAL_PALETTE[7] if x > 5 else 
            PROFESSIONAL_PALETTE[4] 
            for x in zero_df['Sıfır Oranı (%)']
        ],
        text=zero_df['Sıfır Oranı (%)'].apply(lambda x: f'%{x:.2f}'),
        textposition='outside'
    )
])

fig = apply_premium_layout(fig, "Gizli Eksik Veri Oranları (0 Değerleri)")
fig.update_xaxes(title_text="Gizli Eksik Veri Oranı (%)", title_font=dict(size=14, family="Arial", color="#1F2937"))
fig.update_yaxes(title_text="Değişken", title_font=dict(size=14, family="Arial", color="#1F2937"))
fig.add_vline(x=5, line_dash="dash", line_color="orange", annotation_text="Düşük Eşik (%5)")
fig.add_vline(x=20, line_dash="dash", line_color="red", annotation_text="Kritik Eşik (%20)")
fig.add_vline(x=40, line_dash="dash", line_color="darkred", annotation_text="Çok Kritik Eşik (%40)")
save_figure(fig, "phase5_hidden_missing_data")

zero_df.to_csv('../reports/csv/phase5_hidden_missing_data.csv', index=False)
print("✓ Gizli eksik veri raporu kaydedildi: reports/csv/phase5_hidden_missing_data.csv")
print()

# 2. DUPLICATE KONTROLÜ
print("\n" + "="*80)
print("2. DUPLICATE KONTROLÜ")
print("="*80)
print()

duplicate_count = df.duplicated().sum()
duplicate_ratio = (duplicate_count / len(df) * 100)

print(f"Duplicate Satır Sayısı: {duplicate_count} (%{duplicate_ratio:.2f})")

if duplicate_count > 0:
    print("⚠️ Duplicate satırlar tespit edildi.")
    add_data_prep_recommendation(
        issue="Duplicate satırlar mevcut",
        evidence=f"{duplicate_count} adet duplicate satır (%{duplicate_ratio:.2f}).",
        recommendation="Data Prep Expert duplicate satırları incelemeli ve veri kalitesine etkisini değerlendirmelidir. Gerekirse df.drop_duplicates() ile temizlenmelidir.",
        priority="Orta"
    )
else:
    print("✓ Duplicate satır bulunmamaktadır.")
print()

# 3. OUTLIER ANALİZİ (IQR Yöntemi)
print("\n" + "="*80)
print("3. OUTLIER ANALİZİ (IQR Yöntemi)")
print("="*80)
print()

numeric_columns = [col for col in df.select_dtypes(include=[np.number]).columns if col != 'Outcome']

outlier_summary = []

for col in numeric_columns:
    q1 = df[col].quantile(0.25)
    q3 = df[col].quantile(0.75)
    iqr = q3 - q1
    
    lower_bound = q1 - 1.5 * iqr
    upper_bound = q3 + 1.5 * iqr
    
    outlier_count = ((df[col] < lower_bound) | (df[col] > upper_bound)).sum()
    outlier_ratio = (outlier_count / len(df) * 100)
    
    outlier_summary.append({
        'Değişken': col,
        'Outlier Sayısı': outlier_count,
        'Outlier Oranı (%)': round(outlier_ratio, 2),
        'Q1': round(q1, 2),
        'Q3': round(q3, 2),
        'IQR': round(iqr, 2),
        'Alt Sınır': round(lower_bound, 2),
        'Üst Sınır': round(upper_bound, 2)
    })
    
    print(f"{col}:")
    print(f"  Outlier Sayısı: {outlier_count} (%{outlier_ratio:.2f})")
    print(f"  IQR: {iqr:.2f}, Alt Sınır: {lower_bound:.2f}, Üst Sınır: {upper_bound:.2f}")
    
    if outlier_ratio > 5:
        print(f"  ⚠️ Yüksek outlier oranı (>%5)")
        add_data_prep_recommendation(
            issue=f"{col} değişkeninde yüksek outlier oranı",
            evidence=f"IQR yöntemine göre outlier oranı %{outlier_ratio:.2f} (eşik: %5).",
            recommendation=f"Data Prep Expert, {col} için winsorization (%5-95 aralığına kırpma), log dönüşümü veya RobustScaler kullanmalıdır.",
            priority="Orta"
        )
    print()

# Outlier görselleştirme
outlier_df = pd.DataFrame(outlier_summary).sort_values('Outlier Oranı (%)', ascending=True)

fig = go.Figure(data=[
    go.Bar(
        x=outlier_df['Outlier Oranı (%)'],
        y=outlier_df['Değişken'],
        orientation='h',
        marker_color=[
            PROFESSIONAL_PALETTE[3] if x > 5 else PROFESSIONAL_PALETTE[4] 
            for x in outlier_df['Outlier Oranı (%)']
        ],
        text=outlier_df['Outlier Oranı (%)'].apply(lambda x: f'%{x:.2f}'),
        textposition='outside'
    )
])

fig = apply_premium_layout(fig, "Outlier Oranları (IQR Yöntemi)")
fig.update_xaxes(title_text="Outlier Oranı (%)", title_font=dict(size=14, family="Arial", color="#1F2937"))
fig.update_yaxes(title_text="Değişken", title_font=dict(size=14, family="Arial", color="#1F2937"))
fig.add_vline(x=5, line_dash="dash", line_color="red", annotation_text="Kritik Eşik (%5)")
save_figure(fig, "phase5_outlier_ratios")

outlier_df.to_csv('../reports/csv/phase5_outlier_summary.csv', index=False)
print("✓ Outlier özet raporu kaydedildi: reports/csv/phase5_outlier_summary.csv")
print()

# 4. VERİ KALİTESİ ÖZET RAPORU
print("\n" + "="*80)
print("4. VERİ KALİTESİ ÖZET RAPORU")
print("="*80)
print()

quality_summary = {
    'Metrik': [
        'Toplam Satır',
        'Toplam Sütun',
        'Teknik Eksik Veri (NaN)',
        'Gizli Eksik Veri (0 değerleri - kritik)',
        'Duplicate Satır',
        'Yüksek Outlier Oranı (>%5)'
    ],
    'Değer': [
        df.shape[0],
        df.shape[1],
        missing_count.sum(),
        f"{len([x for x in zero_analysis if x['Sıfır Oranı (%)'] > 0])} değişken",
        duplicate_count,
        len([x for x in outlier_summary if x['Outlier Oranı (%)'] > 5])
    ],
    'Durum': [
        '✓ Yeterli',
        '✓ Normal',
        '✓ Sorun Yok' if missing_count.sum() == 0 else '⚠️ Var',
        '🚨 Kritik Sorun' if any(x['Sıfır Oranı (%)'] > 20 for x in zero_analysis) else '⚠️ Sorun Var',
        '✓ Sorun Yok' if duplicate_count == 0 else '⚠️ Var',
        '✓ Sorun Yok' if len([x for x in outlier_summary if x['Outlier Oranı (%)'] > 5]) == 0 else '⚠️ Var'
    ]
}

quality_df = pd.DataFrame(quality_summary)
print(quality_df.to_string(index=False))
print()

quality_df.to_csv('../reports/csv/phase5_data_quality_summary.csv', index=False)
print("✓ Veri kalitesi özet raporu kaydedildi: reports/csv/phase5_data_quality_summary.csv")
print()

# Data Prep önerilerini kaydet
if len(data_prep_recommendations) > 0:
    recommendations_df = pd.DataFrame(data_prep_recommendations)
    recommendations_df.to_csv('../reports/csv/phase5_data_prep_recommendations.csv', index=False)
    print(f"✓ {len(data_prep_recommendations)} adet Data Prep önerisi kaydedildi.")
    print("\nData Prep Önerileri (Öncelik Sırasına Göre):")
    for i, rec in enumerate(recommendations_df.sort_values('Öncelik', ascending=False).to_dict('records'), 1):
        print(f"{i}. [{rec['Öncelik']}] {rec['Sorun']}")

print("\n" + "="*80)
print("PHASE 5 TAMAMLANDI")
print("="*80)
