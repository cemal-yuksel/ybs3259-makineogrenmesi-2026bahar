# ================================================================
# PHASE 1: DATA OVERVIEW
# ================================================================
# Veri setinin temel yapısını anlamak için ilk inceleme

import os
import warnings
from pathlib import Path
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

warnings.filterwarnings("ignore")

# Klasörlerin varlığını garantile
Path('../data/processed').mkdir(parents=True, exist_ok=True)
Path('../figures').mkdir(parents=True, exist_ok=True)
Path('../reports/csv').mkdir(parents=True, exist_ok=True)
Path('../reports/markdown').mkdir(parents=True, exist_ok=True)

# Profesyonel renk paleti
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

# Data Prep Expert için öneri listesi
data_prep_recommendations = []

def add_data_prep_recommendation(issue, evidence, recommendation, priority="Orta"):
    data_prep_recommendations.append({
        "Sorun": issue,
        "Kanıt": evidence,
        "Öneri": recommendation,
        "Öncelik": priority
    })

print("=" * 70)
print("PHASE 1: DATA OVERVIEW")
print("=" * 70)
print()

# Veri setini yükle
print("📁 Veri seti yükleniyor...")
df = pd.read_csv('../data/raw/churn.csv')
print("✅ Veri seti başarıyla yüklendi.\n")

# Temel bilgiler
print("=" * 70)
print("1. VERİ SETİ BOYUTU")
print("=" * 70)
n_rows, n_cols = df.shape
print(f"Satır Sayısı: {n_rows:,}")
print(f"Sütun Sayısı: {n_cols}")
print(f"Toplam Hücre: {n_rows * n_cols:,}\n")

# İlk 5 satır
print("=" * 70)
print("2. İLK 5 SATIRDAN ÖRNEK")
print("=" * 70)
print(df.head())
print()

# Veri tipleri
print("=" * 70)
print("3. VERİ TİPLERİ")
print("=" * 70)
dtype_df = pd.DataFrame({
    'Değişken': df.columns,
    'Veri Tipi': df.dtypes.values,
    'Null Sayısı': df.isnull().sum().values,
    'Null Oranı (%)': (df.isnull().sum() / len(df) * 100).round(2).values
})
print(dtype_df.to_string(index=False))
print()

# Sayısal ve kategorik değişken ayrımı
numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
categorical_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()

print("=" * 70)
print("4. DEĞİŞKEN TİP AYIRIMI")
print("=" * 70)
print(f"Sayısal Değişkenler ({len(numeric_cols)} adet):")
for col in numeric_cols:
    print(f"  - {col}")
print()
print(f"Kategorik Değişkenler ({len(categorical_cols)} adet):")
for col in categorical_cols:
    print(f"  - {col}")
print()

# Özet istatistikler - Sayısal
print("=" * 70)
print("5. SAYISAL DEĞİŞKENLER - ÖZET İSTATİSTİKLER")
print("=" * 70)
print(df[numeric_cols].describe().T)
print()

# Kategorik değişken özet
if len(categorical_cols) > 0:
    print("=" * 70)
    print("6. KATEGORİK DEĞİŞKENLER - EŞSİZ DEĞER SAYILARI")
    print("=" * 70)
    cat_summary = pd.DataFrame({
        'Değişken': categorical_cols,
        'Eşsiz Değer Sayısı': [df[col].nunique() for col in categorical_cols],
        'En Sık Değer': [df[col].mode()[0] if len(df[col].mode()) > 0 else None for col in categorical_cols],
        'En Sık Değer Frekansı': [df[col].value_counts().iloc[0] if len(df[col]) > 0 else 0 for col in categorical_cols]
    })
    print(cat_summary.to_string(index=False))
    print()

# Hedef değişken tespiti (Churn olabilir)
potential_target = None
if 'Churn' in df.columns:
    potential_target = 'Churn'
elif 'churn' in df.columns:
    potential_target = 'churn'
elif 'target' in df.columns:
    potential_target = 'target'
elif 'Target' in df.columns:
    potential_target = 'Target'

if potential_target:
    print("=" * 70)
    print(f"7. HEDEF DEĞİŞKEN TESPİTİ: '{potential_target}'")
    print("=" * 70)
    print(f"Hedef değişken '{potential_target}' olarak tespit edildi.")
    print(f"Dağılım:")
    print(df[potential_target].value_counts())
    print()
    print(f"Oran (%):")
    print((df[potential_target].value_counts(normalize=True) * 100).round(2))
    print()

# Özet rapor kaydet
summary_report = {
    'Metrik': [
        'Toplam Satır Sayısı',
        'Toplam Sütun Sayısı',
        'Sayısal Değişken Sayısı',
        'Kategorik Değişken Sayısı',
        'Toplam Eksik Değer',
        'Eksik Veri Oranı (%)',
        'Hedef Değişken'
    ],
    'Değer': [
        n_rows,
        n_cols,
        len(numeric_cols),
        len(categorical_cols),
        df.isnull().sum().sum(),
        round(df.isnull().sum().sum() / (n_rows * n_cols) * 100, 2),
        potential_target if potential_target else 'Belirlenmedi'
    ]
}

summary_df = pd.DataFrame(summary_report)
summary_df.to_csv('../reports/csv/phase1_data_overview_summary.csv', index=False, encoding='utf-8-sig')

print("=" * 70)
print("📊 Phase 1 Özet Raporu Kaydedildi")
print("=" * 70)
print(f"📄 ../reports/csv/phase1_data_overview_summary.csv")
print()

print("✅ PHASE 1 TAMAMLANDI")
print()
