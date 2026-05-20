# PHASE 1: DATA OVERVIEW
# Veri setinin temel yapısını anlamak için ilk bakış

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

# Data Prep Expert için öneri listesi
data_prep_recommendations = []

def add_data_prep_recommendation(issue, evidence, recommendation, priority="Orta"):
    data_prep_recommendations.append({
        "Sorun": issue,
        "Kanıt": evidence,
        "Öneri": recommendation,
        "Öncelik": priority
    })

# Veri setini yükle
print("="*80)
print("PHASE 1: DATA OVERVIEW")
print("="*80)
print()

df = pd.read_csv('../data/raw/diabetes.csv')

print("✓ Veri seti yüklendi.")
print()

# İlk 5 satır
print("📋 İlk 5 Satır:")
print(df.head())
print()

# Boyut bilgisi
print(f"📊 Veri Seti Boyutu: {df.shape[0]} satır, {df.shape[1]} sütun")
print()

# Veri tipleri
print("🔍 Veri Tipleri:")
print(df.dtypes)
print()

# Genel bilgi
print("ℹ️ Genel Bilgi:")
df.info()
print()

# Eksik değer ilk görünüm
print("⚠️ Eksik Değer İlk Görünümü:")
missing_counts = df.isnull().sum()
missing_ratios = (df.isnull().sum() / len(df) * 100).round(2)
missing_summary = pd.DataFrame({
    'Eksik Sayı': missing_counts,
    'Eksik Oran (%)': missing_ratios
})
print(missing_summary[missing_summary['Eksik Sayı'] > 0])
if missing_summary['Eksik Sayı'].sum() == 0:
    print("✓ Eksik veri bulunmamaktadır.")
print()

# Sayısal değişkenler için özet istatistikler
print("📈 Sayısal Değişkenler İçin Özet İstatistikler:")
print(df.describe())
print()

# Kategorik ve sayısal değişkenleri ayır
numeric_columns = df.select_dtypes(include=[np.number]).columns.tolist()
categorical_columns = df.select_dtypes(include=['object', 'category']).columns.tolist()

print(f"🔢 Sayısal Değişken Sayısı: {len(numeric_columns)}")
print(f"Sayısal Değişkenler: {numeric_columns}")
print()

print(f"📂 Kategorik Değişken Sayısı: {len(categorical_columns)}")
if len(categorical_columns) > 0:
    print(f"Kategorik Değişkenler: {categorical_columns}")
else:
    print("Kategorik değişken bulunmamaktadır.")
print()

# Potansiyel hedef değişken belirle
# Genellikle "Outcome", "Target", "Label" gibi isimler hedef değişken olabilir
# Veya binary (0/1) değerlere sahip son sütun
potential_target = None
if 'Outcome' in df.columns:
    potential_target = 'Outcome'
elif 'Target' in df.columns:
    potential_target = 'Target'
elif 'Label' in df.columns:
    potential_target = 'Label'
else:
    # Son sütun binary ise
    last_col = df.columns[-1]
    if df[last_col].nunique() == 2:
        potential_target = last_col

if potential_target:
    print(f"🎯 Potansiyel Hedef Değişken: {potential_target}")
    print(f"Hedef Değişken Dağılımı:")
    print(df[potential_target].value_counts())
    print()
else:
    print("🎯 Belirgin hedef değişken tespit edilemedi.")
    print()

# Duplicate kontrolü
duplicate_count = df.duplicated().sum()
print(f"🔁 Duplicate Satır Sayısı: {duplicate_count}")
if duplicate_count > 0:
    print(f"⚠️ Duplicate oranı: %{(duplicate_count/len(df)*100):.2f}")
    add_data_prep_recommendation(
        issue="Duplicate satırlar mevcut",
        evidence=f"{duplicate_count} adet duplicate satır tespit edildi (%{(duplicate_count/len(df)*100):.2f}).",
        recommendation="Data Prep Expert duplicate satırların veri kalitesine etkisini değerlendirmeli ve gerekirse temizlik yapmalıdır.",
        priority="Orta"
    )
print()

# Özet CSV kaydet
summary_df = pd.DataFrame({
    'Değişken': df.columns,
    'Veri Tipi': df.dtypes.values,
    'Eksik Sayı': df.isnull().sum().values,
    'Eksik Oran (%)': (df.isnull().sum() / len(df) * 100).round(2).values,
    'Eşsiz Değer': [df[col].nunique() for col in df.columns]
})
summary_df.to_csv('../reports/csv/phase1_data_overview.csv', index=False)
print("✓ Özet rapor kaydedildi: reports/csv/phase1_data_overview.csv")
print()

print("="*80)
print("PHASE 1 TAMAMLANDI")
print("="*80)
