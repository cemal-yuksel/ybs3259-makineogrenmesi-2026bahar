"""
PHASE 1: DATA OVERVIEW
Veri setinin temel yapısını anlamak için ilk analiz
"""

import os
import warnings
import pandas as pd
import numpy as np
from pathlib import Path

warnings.filterwarnings("ignore")

# Klasörlerin varlığını garantile
Path('../data/processed').mkdir(parents=True, exist_ok=True)
Path('../figures').mkdir(parents=True, exist_ok=True)
Path('../reports/csv').mkdir(parents=True, exist_ok=True)
Path('../reports/markdown').mkdir(parents=True, exist_ok=True)

# Veri setini yükle
print("="*80)
print("PHASE 1: DATA OVERVIEW")
print("="*80)

df = pd.read_csv('../data/raw/churn.csv')

print("\n" + "="*80)
print("1. İLK 5 SATIR")
print("="*80)
print(df.head())

print("\n" + "="*80)
print("2. VERİ SETİ BOYUTU")
print("="*80)
print(f"Satır sayısı: {df.shape[0]:,}")
print(f"Sütun sayısı: {df.shape[1]}")
print(f"Toplam hücre sayısı: {df.shape[0] * df.shape[1]:,}")

print("\n" + "="*80)
print("3. VERİ TİPLERİ VE GENEL BİLGİ")
print("="*80)
print(df.info())

print("\n" + "="*80)
print("4. EKSİK DEĞER İLK GÖRÜNÜM")
print("="*80)
missing_summary = pd.DataFrame({
    'Eksik Değer Sayısı': df.isnull().sum(),
    'Eksik Değer Oranı (%)': (df.isnull().sum() / len(df) * 100).round(2)
}).sort_values('Eksik Değer Oranı (%)', ascending=False)
print(missing_summary[missing_summary['Eksik Değer Sayısı'] > 0])

print("\n" + "="*80)
print("5. SAYISAL DEĞİŞKENLER - İSTATİSTİKSEL ÖZET")
print("="*80)
numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
print(f"Sayısal değişken sayısı: {len(numeric_cols)}")
print("\nSayısal değişkenler:")
print(numeric_cols)
print("\nİstatistiksel özet:")
print(df[numeric_cols].describe())

print("\n" + "="*80)
print("6. KATEGORİK DEĞİŞKENLER")
print("="*80)
categorical_cols = df.select_dtypes(include=['object']).columns.tolist()
print(f"Kategorik değişken sayısı: {len(categorical_cols)}")
print("\nKategorik değişkenler:")
for col in categorical_cols:
    unique_count = df[col].nunique()
    print(f"  - {col}: {unique_count} eşsiz değer")

print("\n" + "="*80)
print("7. HEDEF DEĞİŞKEN BELİRLEME")
print("="*80)
# Churn veri setinde genellikle 'Churn' veya 'Exited' gibi hedef değişkenler vardır
possible_targets = ['Churn', 'churn', 'Exited', 'exited', 'Target', 'target']
target_col = None

for col in possible_targets:
    if col in df.columns:
        target_col = col
        break

if target_col:
    print(f"Tespit edilen hedef değişken: {target_col}")
    print(f"\nHedef değişken değer dağılımı:")
    print(df[target_col].value_counts())
    print(f"\nHedef değişken oran dağılımı:")
    print((df[target_col].value_counts(normalize=True) * 100).round(2))
else:
    print("Otomatik hedef değişken tespit edilemedi.")
    print("Tüm değişkenler:")
    print(df.columns.tolist())

print("\n" + "="*80)
print("8. TEMEL VERİ KALİTESİ KONTROLLARI")
print("="*80)

# Duplicate kontrolü
duplicate_count = df.duplicated().sum()
print(f"Duplicate satır sayısı: {duplicate_count}")

# Benzersiz değer oranları
print("\nBenzersiz değer oranları (kardinalite):")
for col in df.columns:
    unique_ratio = round(df[col].nunique() / len(df) * 100, 2)
    print(f"  - {col}: %{unique_ratio}")

# Özet CSV kaydet
overview_summary = pd.DataFrame({
    'Değişken': df.columns,
    'Veri Tipi': df.dtypes.values,
    'Eksik Değer': df.isnull().sum().values,
    'Eksik Oran (%)': [round(df[col].isnull().sum() / len(df) * 100, 2) for col in df.columns],
    'Eşsiz Değer': [df[col].nunique() for col in df.columns],
    'Kardinalite (%)': [round(df[col].nunique() / len(df) * 100, 2) for col in df.columns]
})

overview_summary.to_csv('../reports/csv/phase1_data_overview.csv', index=False)
print("\n✅ Özet rapor kaydedildi: reports/csv/phase1_data_overview.csv")

print("\n" + "="*80)
print("PHASE 1 TAMAMLANDI")
print("="*80)
