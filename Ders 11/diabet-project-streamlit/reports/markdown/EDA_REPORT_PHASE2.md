# PHASE 2: UNIVARIATE ANALYSIS - Detaylı Rapor

## 📊 Yapılan Analiz:

Bu aşamada 8 sayısal değişken (Outcome hariç) için tekil davranış analizi yapılmıştır. Her değişken için histogram ve boxplot görselleştirilmiş, temel istatistikler (ortalama, medyan, std, min, max), çarpıklık (skewness), basıklık (kurtosis), outlier oranı (IQR yöntemi) ve gizli eksik veri kontrolü (0 değerleri) hesaplanmıştır.

**Kod:** `phase2_univariate_analysis.py`  
**Görsel Sayısı:** 16 adet (her değişken için 2 grafik: histogram + boxplot)  
**Kaydedilen Rapor:** `reports/csv/phase2_univariate_summary.csv`

---

## 🧠 Koddan Elde Edilen Bulgular:

### 1. **Pregnancies (Hamilelik Sayısı)**
- **Ortalama:** 3.85, **Medyan:** 3.0
- **Dağılım:** 0-17 arası, hafif pozitif çarpık (skewness: 0.902)
- **Outlier:** %0.52 (çok düşük, sorun yok)
- **0 Değer:** %14.45 (111 kişi) - Bu mantıklıdır, hiç hamile kalmamış kadınlar
- **Yorum:** Sağlıklı dağılım, veri kalitesi iyi

### 2. **Glucose (Glikoz Seviyesi)** ⚠️
- **Ortalama:** 120.89, **Medyan:** 117.0
- **Dağılım:** Neredeyse normal (skewness: 0.174)
- **Outlier:** %0.65 (düşük)
- **❌ GİZLİ EKSİK VERİ:** 5 adet 0 değer (%0.65) - **Glikoz seviyesi 0 olamaz!**
- **Yorum:** Düşük oranda ama kritik gizli eksik veri var

### 3. **BloodPressure (Kan Basıncı)** ⚠️⚠️
- **Ortalama:** 69.11, **Medyan:** 72.0
- **Dağılım:** Negatif çarpık (skewness: -1.844), sola çekik
- **Kurtosis:** 5.180 (yüksek basıklık, uç değer yoğun)
- **Outlier:** %5.86 (45 kişi) - **Kritik eşiğin üzerinde (%5)**
- **❌ GİZLİ EKSİK VERİ:** 35 adet 0 değer (%4.56) - **Kan basıncı 0 olamaz!**
- **Yorum:** Hem gizli eksik veri, hem yüksek outlier, hem aşırı çarpıklık - üçlü sorun!

### 4. **SkinThickness (Cilt Kalınlığı)** 🚨 KRİTİK!
- **Ortalama:** 20.54, **Medyan:** 23.0
- **Outlier:** %0.13 (düşük)
- **❌❌ GİZLİ EKSİK VERİ:** 227 adet 0 değer (%29.56) - **Neredeyse %30!**
- **Yorum:** Bu değişken ciddi veri kalitesi sorunu yaşıyor. %30 oranında gizli eksik veri var. Model eğitiminde bu değişkenin kullanılabilirliği sorgulanmalı.

### 5. **Insulin (İnsülin Seviyesi)** 🚨🚨 ÇOK KRİTİK!
- **Ortalama:** 79.8, **Medyan:** 30.5 - **BÜYÜK FARK! Dağılım çok çarpık**
- **Skewness:** 2.272 (çok yüksek pozitif çarpıklık)
- **Kurtosis:** 7.214 (aşırı basıklık)
- **Outlier:** %4.43 (34 kişi)
- **❌❌❌ GİZLİ EKSİK VERİ:** 374 adet 0 değer (%48.70) - **VERİNİN NEREDEYSE YARISI!**
- **Yorum:** Bu değişken veri setinin en sorunlu değişkenidir. %48.7 oranında gizli eksik veri, aşırı çarpıklık ve yüksek basıklık var. İmputasyon stratejisi çok kritik. Alternatif olarak bu değişken modelden çıkarılması bile düşünülebilir.

### 6. **BMI (Vücut Kitle İndeksi)** ⚠️
- **Ortalama:** 31.99, **Medyan:** 32.0 (çok yakın, dengeli dağılım)
- **Skewness:** -0.429 (hafif negatif çarpık, sorun değil)
- **Outlier:** %2.47 (düşük)
- **❌ GİZLİ EKSİK VERİ:** 11 adet 0 değer (%1.43) - **BMI 0 olamaz!**
- **Yorum:** Düşük oranda gizli eksik veri, genel olarak sağlıklı dağılım

### 7. **DiabetesPedigreeFunction (Diyabet Soy Ağacı Fonksiyonu)** ⚠️
- **Ortalama:** 0.47, **Medyan:** 0.37
- **Skewness:** 1.920 (yüksek pozitif çarpıklık)
- **Kurtosis:** 5.595 (yüksek basıklık)
- **Outlier:** %3.78 (kabul edilebilir)
- **0 Değer:** Yok
- **Yorum:** Çarpıklık yüksek, log dönüşümü faydalı olabilir

### 8. **Age (Yaş)** ⚠️
- **Ortalama:** 33.24, **Medyan:** 29.0
- **Dağılım:** 21-81 arası, pozitif çarpık (skewness: 1.130)
- **Outlier:** %1.17 (çok düşük)
- **0 Değer:** Yok
- **Yorum:** Genç hasta ağırlıklı veri seti, hafif çarpıklık var

---

## 💡 Analitik Yorum:

### **Veri Kalitesi Krizi: Gizli Eksik Veri Sorunu**

Bu veri setinin en kritik sorunu **gizli eksik verilerdir**. Eksik değerler 0 olarak kodlanmış:

| Değişken | 0 Değer Sayısı | 0 Oranı | Kritiklik |
|----------|----------------|---------|-----------|
| **Insulin** | 374 | %48.70 | 🚨 ÇOK KRİTİK |
| **SkinThickness** | 227 | %29.56 | 🚨 KRİTİK |
| **BloodPressure** | 35 | %4.56 | ⚠️ Orta |
| **BMI** | 11 | %1.43 | ⚠️ Düşük |
| **Glucose** | 5 | %0.65 | ⚠️ Düşük |

**İş Değeri:**
- **Insulin ve SkinThickness** değişkenlerinin model performansına katkısı sorgulanmalıdır.
- Bu iki değişken, %30-50 oranında eksik veri içerdiği için imputasyon yapılsa bile model bias riski yüksektir.
- **Alternatif Strateji:** Bu iki değişken modelden çıkarılıp, geri kalan 6 değişkenle baseline model eğitilip sonuç karşılaştırılabilir.

### **Çarpıklık ve Dönüşüm İhtiyacı**

| Değişken | Skewness | Yorum |
|----------|----------|-------|
| **Insulin** | 2.272 | Çok yüksek pozitif çarpıklık - log dönüşümü kritik |
| **DiabetesPedigreeFunction** | 1.920 | Yüksek pozitif çarpıklık - log dönüşümü önerilir |
| **BloodPressure** | -1.844 | Yüksek negatif çarpıklık - Box-Cox veya Yeo-Johnson |
| **Age** | 1.130 | Orta pozitif çarpıklık - log veya sqrt dönüşümü |

**İş Değeri:**
- Çarpık dağılımlar, lineer modellerde (LogisticRegression, LinearSVC) performans kaybına neden olur.
- Tree-based modeller (RandomForest, XGBoost) çarpıklığa duyarsızdır, dönüşüm gerekmez.
- Stratejik Öneri: Hem dönüşümlü hem dönüşümsüz modeller eğitilip karşılaştırılmalıdır.

### **Outlier Durumu**

- **BloodPressure:** %5.86 outlier oranı kritik eşiğin üzerinde.
- Diğer değişkenlerde outlier oranı düşük (%0-4 arası).
- **Strateji:** Robust Scaler veya winsorization (örn. %95-99 aralığına kırpma) kullanılabilir.

---

## ⚠️ Risk / Dikkat Edilmesi Gereken Nokta:

### 1. **Insulin ve SkinThickness Değişkenleri (Yüksek Risk)**
- Bu iki değişken %30-50 oranında gizli eksik veri içeriyor.
- İmputasyon yapılsa bile model bias riski yüksek.
- **Öneri:** Bu değişkenler dahil ve hariç olmak üzere iki farklı model pipeline'ı oluştur, performansları karşılaştır.

### 2. **BloodPressure Üçlü Sorunu (Orta-Yüksek Risk)**
- Gizli eksik veri (%4.56)
- Yüksek outlier oranı (%5.86)
- Aşırı negatif çarpıklık (-1.844)
- **Öneri:** 0 değerleri NaN yap, robust imputation (median veya KNN), sonra Yeo-Johnson dönüşümü uygula.

### 3. **Çarpıklık ve Model Seçimi (Orta Risk)**
- Insulin, DiabetesPedigreeFunction, Age gibi değişkenlerde yüksek çarpıklık var.
- LogisticRegression gibi lineer modellerde performans düşebilir.
- **Öneri:** Tree-based modeller (RandomForest, XGBoost) ve lineer modelleri karşılaştır.

---

## 🔁 Agent Etkileşim Notu:

### **Data Prep Expert İçin Yüksek Öncelikli Öneriler:**

#### **1. Gizli Eksik Veri Yönetimi (Yüksek Öncelik)**

**Glucose, BloodPressure, SkinThickness, Insulin, BMI:**
```python
# 0 değerlerini NaN'a dönüştür
for col in ['Glucose', 'BloodPressure', 'SkinThickness', 'Insulin', 'BMI']:
    df[col] = df[col].replace(0, np.nan)
```

**İmputasyon Stratejisi:**
- **Düşük eksik veri (%0-5):** Glucose, BMI, BloodPressure → Median veya Mean imputation
- **Orta eksik veri (%5-15):** BloodPressure → KNN Imputer (k=5)
- **Yüksek eksik veri (%30+):** SkinThickness, Insulin → **İki alternatif dene:**
  - **Alternatif 1:** IterativeImputer (MICE) kullan
  - **Alternatif 2:** Bu değişkenleri modelden çıkar, performans karşılaştır

#### **2. Çarpıklık Dönüşümü (Orta Öncelik)**

**Pozitif çarpık değişkenler (Insulin, DiabetesPedigreeFunction, Age):**
```python
from sklearn.preprocessing import PowerTransformer

# Yeo-Johnson (negatif değerlere izin verir)
pt = PowerTransformer(method='yeo-johnson')
df[['Insulin', 'DiabetesPedigreeFunction', 'Age']] = pt.fit_transform(
    df[['Insulin', 'DiabetesPedigreeFunction', 'Age']]
)
```

**Negatif çarpık değişkenler (BloodPressure):**
- Yeo-Johnson dönüşümü önerilir.

#### **3. Outlier Yönetimi (Orta Öncelik)**

**BloodPressure için:**
```python
# Winsorization (%5-95 aralığına kırp)
from scipy.stats import mstats
df['BloodPressure'] = mstats.winsorize(df['BloodPressure'], limits=[0.05, 0.05])
```

Alternatif: RobustScaler kullan (IQR bazlı scaling):
```python
from sklearn.preprocessing import RobustScaler
scaler = RobustScaler()
df[['BloodPressure']] = scaler.fit_transform(df[['BloodPressure']])
```

#### **4. İki Pipeline Stratejisi (Yüksek Öncelik)**

**Pipeline 1: Tüm Değişkenler (İmputasyon Dahil)**
- Insulin ve SkinThickness dahil
- İleri imputasyon (IterativeImputer)
- Model: LogisticRegression, RandomForest, XGBoost

**Pipeline 2: Problemli Değişkenler Hariç**
- Insulin ve SkinThickness hariç (sadece 6 değişken)
- Basit imputation (median)
- Model: Aynı modeller

**Karşılaştırma:** Hangi pipeline daha iyi performans veriyor?

---

## 📁 Kaydedilen Görseller:

**Histogramlar (8 adet):**
- `figures/phase2_histogram_pregnancies.html/png`
- `figures/phase2_histogram_glucose.html/png`
- `figures/phase2_histogram_bloodpressure.html/png`
- `figures/phase2_histogram_skinthickness.html/png`
- `figures/phase2_histogram_insulin.html/png`
- `figures/phase2_histogram_bmi.html/png`
- `figures/phase2_histogram_diabetespedigreefunction.html/png`
- `figures/phase2_histogram_age.html/png`

**Boxplotlar (8 adet):**
- `figures/phase2_boxplot_pregnancies.html/png`
- `figures/phase2_boxplot_glucose.html/png`
- `figures/phase2_boxplot_bloodpressure.html/png`
- `figures/phase2_boxplot_skinthickness.html/png`
- `figures/phase2_boxplot_insulin.html/png`
- `figures/phase2_boxplot_bmi.html/png`
- `figures/phase2_boxplot_diabetespedigreefunction.html/png`
- `figures/phase2_boxplot_age.html/png`

**CSV Raporlar:**
- `reports/csv/phase2_univariate_summary.csv`
- `reports/csv/phase2_data_prep_recommendations.csv` (10 öneri)

---

## ✅ Phase 2 Tamamlandı - Sırada: Phase 3 (Bivariate Analysis)
