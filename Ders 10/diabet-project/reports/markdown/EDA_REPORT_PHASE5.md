# PHASE 5: DATA QUALITY & ANOMALY DETECTION - Detaylı Rapor

## 📊 Yapılan Analiz:

Bu aşamada veri setinin kalite durumu sistematik olarak incelenmiştir:
1. **Teknik Eksik Veri (NaN)** kontrolü
2. **Gizli Eksik Veri (0 değerleri)** analizi ve görselleştirmesi
3. **Duplicate satır** kontrolü
4. **Outlier analizi** (IQR yöntemi)
5. **Veri kalitesi özet raporu** oluşturma

**Kod:** `phase5_data_quality_analysis.py`  
**Görsel Sayısı:** 2 adet (gizli eksik veri + outlier oranları)  
**Kaydedilen Raporlar:**
- `reports/csv/phase5_hidden_missing_data.csv`
- `reports/csv/phase5_outlier_summary.csv`
- `reports/csv/phase5_data_quality_summary.csv`
- `reports/csv/phase5_data_prep_recommendations.csv`

---

## 🧠 Koddan Elde Edilen Bulgular:

### **1. Teknik Eksik Veri (NaN) Durumu**

- ✅ **0 adet NaN** değer
- Veri seti teknik olarak eksik veri içermiyor
- Ancak bu yanıltıcı! Eksik veriler **0 olarak kodlanmış**.

---

### **2. Gizli Eksik Veri (0 Değerleri) - KRİTİK SORUN**

Tıbbi ölçümlerde **0 değeri mantıksal olarak imkansızdır**. Bu değerler aslında eksik veridir.

| Değişken | Sıfır Sayısı | Sıfır Oranı (%) | Kritiklik | Durum |
|----------|--------------|-----------------|-----------|-------|
| **Insulin** | 374 | **%48.70** | 🚨 ÇOK KRİTİK | Verinin yarısı eksik! |
| **SkinThickness** | 227 | **%29.56** | ⚠️ KRİTİK | Verinin 1/3'ü eksik! |
| BloodPressure | 35 | %4.56 | ✓ DÜŞÜK | Kabul edilebilir |
| Glucose | 5 | %0.65 | ✓ DÜŞÜK | Kabul edilebilir |
| BMI | 11 | %1.43 | ✓ DÜŞÜK | Kabul edilebilir |

**Kritiklik Sınırları:**
- ✓ Düşük: %0-5 arası
- ⚠️ Orta: %5-20 arası
- ⚠️ Kritik: %20-40 arası
- 🚨 Çok Kritik: %40 üzeri

---

### **3. Duplicate Satır Kontrolü**

- ✅ **0 adet duplicate** satır
- Veri seti temiz ve tutarlı

---

### **4. Outlier Analizi (IQR Yöntemi)**

IQR (Interquartile Range) yöntemiyle outlier tespit edilmiştir:

| Değişken | Outlier Sayısı | Outlier Oranı (%) | Durum |
|----------|----------------|-------------------|-------|
| **BloodPressure** | 45 | **%5.86** | ⚠️ Kritik eşiğin üzerinde (>%5) |
| Insulin | 34 | %4.43 | ✓ Kabul edilebilir |
| DiabetesPedigreeFunction | 29 | %3.78 | ✓ Kabul edilebilir |
| BMI | 19 | %2.47 | ✓ Kabul edilebilir |
| Age | 9 | %1.17 | ✓ Kabul edilebilir |
| Glucose | 5 | %0.65 | ✓ Kabul edilebilir |
| Pregnancies | 4 | %0.52 | ✓ Kabul edilebilir |
| SkinThickness | 1 | %0.13 | ✓ Kabul edilebilir |

**Önemli Gözlem:**
- **BloodPressure** tek başına kritik eşiği (%5) aşan değişken
- Bu değişken aynı zamanda %4.56 gizli eksik veri ve yüksek negatif çarpıklık (-1.844) içeriyor
- **BloodPressure üçlü sorun yaşıyor**: Gizli eksik veri + Outlier + Çarpıklık

---

### **5. Veri Kalitesi Özet Raporu**

| Metrik | Değer | Durum |
|--------|-------|-------|
| Toplam Satır | 768 | ✓ Yeterli |
| Toplam Sütun | 9 | ✓ Normal |
| Teknik Eksik Veri (NaN) | 0 | ✓ Sorun Yok |
| **Gizli Eksik Veri (kritik)** | **5 değişken** | 🚨 **Kritik Sorun** |
| Duplicate Satır | 0 | ✓ Sorun Yok |
| Yüksek Outlier Oranı (>%5) | 1 değişken | ⚠️ Var |

**Genel Değerlendirme:**
- Veri seti genel olarak temiz (duplicate yok, NaN yok)
- **Ancak gizli eksik veri ciddi bir sorun**
- Insulin ve SkinThickness %20'nin üzerinde eksik veri içeriyor

---

## 💡 Analitik Yorum:

### **1. Insulin ve SkinThickness: Model Dışı Bırakılmalı (Önerilen)**

**Insulin:**
- %48.70 eksik veri - **Verinin neredeyse yarısı yok!**
- Phase 3: İstatistiksel olarak anlamsız (p=0.0657)
- Phase 4: Zayıf korelasyon (r=0.131)
- **Sonuç:** Bu değişken **modelden çıkarılmalı**.

**SkinThickness:**
- %29.56 eksik veri - **Verinin 1/3'ü yok!**
- Phase 3: Zayıf ilişki (p=0.0130)
- Phase 4: Çok zayıf korelasyon (r=0.075)
- **Sonuç:** Bu değişken **modelden çıkarılmalı**.

**İmputasyon Riski:**
- %30-50 oranında imputasyon yapılırsa, **model "uydurulmuş" veriye göre öğrenecek**.
- Bu, **overfitting ve bias riskini çok artırır**.
- İmputasyon, eksik veri %5-15 arasında olduğunda güvenlidir.

---

### **2. BloodPressure: Dikkatli İmputasyon Gerekli**

**Sorunlar:**
- %4.56 gizli eksik veri
- %5.86 outlier oranı (kritik eşiğin üzerinde)
- -1.844 negatif çarpıklık (aşırı)

**Strateji:**
1. 0 değerlerini NaN'a dönüştür
2. Outlier'ları winsorize et (%5-95 aralığına kırp)
3. Median veya KNN Imputer (k=5) ile imputasyon yap
4. Yeo-Johnson dönüşümü uygula (çarpıklık için)

---

### **3. Glucose ve BMI: Basit İmputasyon Yeterli**

**Glucose:**
- %0.65 eksik veri (5 adet) - Çok düşük
- Median imputation yeterli

**BMI:**
- %1.43 eksik veri (11 adet) - Çok düşük
- Median imputation yeterli

---

### **4. Veri Kalitesi Skoru**

Veri setine 1-10 arası kalite skoru verirsek:

| Kategori | Skor | Açıklama |
|----------|------|----------|
| Teknik Temizlik | 10/10 | NaN yok, duplicate yok |
| Gizli Eksik Veri | 3/10 | Insulin ve SkinThickness çok sorunlu |
| Outlier Yönetimi | 7/10 | BloodPressure hariç kabul edilebilir |
| Multicollinearity | 10/10 | Sorun yok |
| **Genel Kalite** | **6/10** | Gizli eksik veri çok ciddi sorun |

**Yorum:**
- Veri seti orta kalitede.
- Gizli eksik veri sorunu çözülürse kalite 8-9/10'a çıkar.

---

## ⚠️ Risk / Dikkat Edilmesi Gereken Nokta:

### **1. İmputasyon Stratejisi Kritik (Yüksek Risk)**

**Yanlış Yaklaşım:**
```python
# BU YANLIŞ! %50 eksik veriyi IterativeImputer ile doldurmak
df['Insulin'].replace(0, np.nan, inplace=True)
imputer = IterativeImputer()
df[['Insulin']] = imputer.fit_transform(df[['Insulin']])
```
**Neden Yanlış:**
- Model, gerçek veri yerine "tahmin edilen" veriye göre öğrenecek.
- Overfitting riski çok yüksek.
- Test setinde performans çok düşebilir.

**Doğru Yaklaşım:**
```python
# DOĞRU: Problematic features'ları çıkar
baseline_features = ['Glucose', 'BMI', 'Age', 'Pregnancies', 
                     'DiabetesPedigreeFunction', 'BloodPressure']
# Insulin ve SkinThickness dahil değil
```

---

### **2. BloodPressure Üçlü Sorunu (Orta-Yüksek Risk)**

- Gizli eksik veri + Outlier + Çarpıklık
- **Pipeline gerekli:**
  1. 0 → NaN
  2. Outlier winsorization
  3. Median/KNN imputation
  4. Yeo-Johnson transformation

---

### **3. Model Performans Beklentisi**

**Insulin ve SkinThickness dahil (riskli):**
- İmputasyon nedeniyle overfitting riski
- Validation accuracy düşük olabilir
- Test accuracy daha da düşük olabilir

**Insulin ve SkinThickness hariç (önerilen):**
- Daha sağlam model
- Daha güvenilir genelleme
- Daha yüksek test accuracy

**Öneri:**
- **İki pipeline yan yana eğit:**
  - Pipeline 1: Baseline (6 değişken)
  - Pipeline 2: Advanced (8 değişken + ileri imputasyon)
- **Cross-validation ile karşılaştır**
- Hangi pipeline daha iyi validation score veriyorsa onu kullan

---

## 🔁 Agent Etkileşim Notu:

### **Data Prep Expert İçin Yüksek Öncelikli Öneriler:**

#### **1. Gizli Eksik Veri Yönetimi (Yüksek Öncelik)**

**Adım 1: 0 Değerlerini NaN'a Dönüştür**
```python
# Mantıksal olarak 0 olamayacak değişkenler
zero_to_nan_cols = ['Glucose', 'BloodPressure', 'SkinThickness', 'Insulin', 'BMI']

for col in zero_to_nan_cols:
    df[col] = df[col].replace(0, np.nan)
```

**Adım 2: İmputasyon Stratejisi**

**Düşük eksik veri (%0-5):**
```python
from sklearn.impute import SimpleImputer

# Glucose, BMI, BloodPressure
simple_imputer = SimpleImputer(strategy='median')
df[['Glucose', 'BMI', 'BloodPressure']] = simple_imputer.fit_transform(
    df[['Glucose', 'BMI', 'BloodPressure']]
)
```

**Yüksek eksik veri (%29-49) - İKİ ALTERNATİF:**

**Alternatif 1: Modelden Çıkar (ÖNERİLEN)**
```python
# Baseline model
selected_features = ['Glucose', 'Pregnancies', 'BMI', 'Age', 
                     'DiabetesPedigreeFunction', 'BloodPressure']
X = df[selected_features]
y = df['Outcome']
```

**Alternatif 2: İleri İmputasyon (RİSKLİ)**
```python
from sklearn.experimental import enable_iterative_imputer
from sklearn.impute import IterativeImputer

# SkinThickness, Insulin
iter_imputer = IterativeImputer(max_iter=10, random_state=42)
df[['SkinThickness', 'Insulin']] = iter_imputer.fit_transform(
    df[['SkinThickness', 'Insulin']]
)
```

#### **2. Outlier Yönetimi (Orta Öncelik)**

**BloodPressure için Winsorization:**
```python
from scipy.stats import mstats

# %5-95 aralığına kırp
df['BloodPressure'] = mstats.winsorize(df['BloodPressure'], limits=[0.05, 0.05])
```

**Alternatif: RobustScaler (IQR bazlı scaling)**
```python
from sklearn.preprocessing import RobustScaler

scaler = RobustScaler()
df[['BloodPressure']] = scaler.fit_transform(df[['BloodPressure']])
```

#### **3. Final Preprocessing Pipeline (Yüksek Öncelik)**

**Baseline Pipeline (Önerilen):**
```python
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, PowerTransformer

# 1. 0 → NaN
zero_to_nan_cols = ['Glucose', 'BloodPressure', 'BMI']
for col in zero_to_nan_cols:
    df[col] = df[col].replace(0, np.nan)

# 2. Feature selection
selected_features = ['Glucose', 'Pregnancies', 'BMI', 'Age', 
                     'DiabetesPedigreeFunction', 'BloodPressure']

# 3. Pipeline
preprocessing_pipeline = Pipeline([
    ('imputer', SimpleImputer(strategy='median')),
    ('transformer', PowerTransformer(method='yeo-johnson')),  # Çarpıklık için
    ('scaler', StandardScaler())
])

X = df[selected_features]
y = df['Outcome']

X_processed = preprocessing_pipeline.fit_transform(X)
```

#### **4. Data Prep Handoff Raporu**

Data Prep Expert, Model Expert'e şu raporu iletmelidir:

```
VERİ HAZIRLAMA TAMAMLANDI

1. GİZLİ EKSİK VERİ YÖNETİMİ:
   - Insulin ve SkinThickness modelden çıkarıldı (yüksek eksik veri)
   - Glucose, BloodPressure, BMI: 0 → NaN → median imputation

2. OUTLIER YÖNETİMİ:
   - BloodPressure: Winsorization (%5-95 aralığı)

3. ÇARPIKLIK DÖNÜŞÜMLERİ:
   - Yeo-Johnson dönüşümü uygulandı (tüm sayısal değişkenler)

4. FİNAL FEATURE SET (6 değişken):
   - Glucose, Pregnancies, BMI, Age, DiabetesPedigreeFunction, BloodPressure

5. TRAIN-TEST SPLIT:
   - Stratified split (80-20)
   - Random state: 42

6. ÖNERİLEN MODELLER:
   - LogisticRegression (baseline)
   - RandomForestClassifier
   - XGBoostClassifier
   - VotingClassifier (ensemble)

7. DEĞERLENDİRME METRİKLERİ:
   - Accuracy, Precision, Recall, F1-Score
   - ROC-AUC
   - Confusion Matrix
   - Class imbalance var (%65-35), bu nedenle accuracy tek başına yeterli değil
```

---

## 📁 Kaydedilen Görseller:

- `figures/phase5_hidden_missing_data.html/png` - Gizli eksik veri oranları (0 değerleri)
- `figures/phase5_outlier_ratios.html/png` - Outlier oranları (IQR yöntemi)

**CSV Raporlar:**
- `reports/csv/phase5_hidden_missing_data.csv` - Gizli eksik veri detayları
- `reports/csv/phase5_outlier_summary.csv` - Outlier analiz detayları
- `reports/csv/phase5_data_quality_summary.csv` - Genel veri kalitesi özeti
- `reports/csv/phase5_data_prep_recommendations.csv` - 6 öneri

---

## ✅ Phase 5 Tamamlandı - Sırada: Phase 6 (Insight Generation)
