# PHASE 2: UNIVARIATE ANALYSIS - TEK DEĞİŞKENLİ DAĞILIM ANALİZİ

## 📊 Yapılan Analiz

Bu aşamada her değişkenin tek başına davranışını anlamak için kod üretildi ve çalıştırıldı. Sayısal değişkenler için histogram, boxplot, skewness, kurtosis ve IQR outlier analizi yapıldı. Kategorik değişkenler için frekans tabloları oluşturuldu ve bar chart'lar çizildi.

**Analiz edilen değişken sayısı:**
- 3 sayısal değişken
- 17 kategorik değişken (customerID hariç)
- **Toplam 23 grafik** oluşturuldu

---

## 🧠 Koddan Elde Edilen Bulgular

### 1. Sayısal Değişkenler - İstatistiksel Özet

| Değişken | Ortalama | Medyan | Std. Sapma | Min | Max | Skewness | Kurtosis | Outlier Oranı (%) |
|---|---|---|---|---|---|---|---|---|
| **SeniorCitizen** | 0.16 | 0.0 | 0.37 | 0.0 | 1.0 | **1.834** | 1.363 | **16.21%** |
| **tenure** | 32.37 | 29.0 | 24.56 | 0.0 | 72.0 | 0.24 | -1.387 | 0.0% |
| **MonthlyCharges** | 64.76 | 70.35 | 30.09 | 18.25 | 118.75 | -0.221 | -1.257 | 0.0% |

### 2. Kategorik Değişkenler - Frekans Özeti

**17 kategorik değişken** analiz edildi. Önemli bulgular:

#### Hedef Değişken: Churn
- **No (Kaldı):** 5,174 (%73.46)
- **Yes (Ayrıldı):** 1,869 (%26.54)

#### Demografik Değişkenler
- **gender:** 2 kategori (dengeli dağılım bekleniyor)
- **Partner:** 2 kategori
- **Dependents:** 2 kategori
- **SeniorCitizen:** Binary (0/1) ama sayısal tipte

#### Hizmet Değişkenleri
- **PhoneService:** 2 kategori
- **MultipleLines:** 3 kategori (Yes, No, No phone service)
- **InternetService:** 3 kategori (DSL, Fiber optic, No)
- **OnlineSecurity, OnlineBackup, DeviceProtection, TechSupport, StreamingTV, StreamingMovies:** Her biri 3 kategori

#### Sözleşme ve Ödeme Değişkenleri
- **Contract:** 3 kategori (Month-to-month, One year, Two year)
- **PaperlessBilling:** 2 kategori
- **PaymentMethod:** 4 kategori

#### Kritik Bulgu: TotalCharges
- **Eşsiz değer sayısı:** 6,531 (veri setinin %92.73'ü)
- **Veri tipi:** Object (string) - **Sayısal olmalı!**
- Bu değişken PHASE 1'de tespit edilen veri kalitesi sorunu

---

## 💡 Analitik Yorum (YBS Uzmanı Perspektifi)

### Sayısal Değişkenler Yorumu

#### 1. SeniorCitizen - Yaşlı Müşteri Durumu
**📊 İstatistiksel Bulgular:**
- Ortalama: 0.16 → Müşterilerin **%16'sı yaşlı (65+ yaş)**
- Medyan: 0.0 → Çoğu müşteri yaşlı değil
- Skewness: **1.834** → **Yüksek sağa çarpıklık**
- Outlier oranı: **%16.21**

**💼 İş Değeri Yorumu:**
Bu değişken binary (0/1) olmasına rağmen sayısal tipte kodlanmış. Yüksek çarpıklık ve outlier oranı binary değişkenin doğal yapısından kaynaklanıyor - %84 müşteri yaşlı değil, %16'sı yaşlı. Bu dengesizlik modelleme için önemli:
- Yaşlı müşterilerin churn davranışı farklı olabilir
- Feature engineering'de "SeniorCitizen + Dependents" kombinasyonu değerli olabilir
- Binary değişken olduğu için log dönüşümü uygun değil, ancak class weighting veya SMOTE benzeri teknikler değerlendirilebilir

**🎯 Modelleme Etkisi:**
Binary değişken olduğu için dönüşüm gerekmez. Ancak dengesizlik nedeniyle model baskın sınıfa (yaşlı olmayan) bias gösterebilir.

#### 2. tenure - Müşteri Süresi (Ay)
**📊 İstatistiksel Bulgular:**
- Ortalama: 32.37 ay (yaklaşık 2.7 yıl)
- Medyan: 29 ay
- Min: 0 ay (yeni müşteriler) | Max: 72 ay (6 yıl)
- Skewness: **0.24** → Hafif sağa çarpık ama kabul edilebilir
- Outlier oranı: **%0** → Temiz dağılım

**💼 İş Değeri Yorumu:**
Bu değişken **müşteri sadakatinin en güçlü göstergelerinden biri**. Bulgular:
- Ortalama müşteri süresi 2.7 yıl → Makul bir müşteri ömrü
- 0 ay tenure olan müşteriler var → İlk ay churn riski kritik olabilir
- 72 ay maksimum → 6 yıl kalan müşteriler sadık segment
- Medyan (29) ve ortalama (32) yakın → Dengeli dağılım

**🎯 Modelleme Etkisi:**
- **En önemli churn predictor olması beklenir**
- Dönüşüm gerektirmiyor (düşük çarpıklık)
- Feature engineering fırsatı: "tenure_group" (0-12 ay, 13-24 ay, 25-48 ay, 49+ ay)
- Yeni müşteriler (tenure < 6 ay) için risk scoring modeli ayrı değerlendirilebilir

#### 3. MonthlyCharges - Aylık Ücret
**📊 İstatistiksel Bulgular:**
- Ortalama: $64.76
- Medyan: $70.35 (ortalamadan yüksek - sola çarpık işaret)
- Min: $18.25 | Max: $118.75
- Skewness: **-0.221** → Hafif sola çarpık
- Outlier oranı: **%0** → Temiz dağılım

**💼 İş Değeri Yorumu:**
Aylık ücret geniş bir aralıkta ($18.25 - $118.75) dağılmış. Bu:
- **Farklı paket/hizmet seviyeleri** olduğunu gösterir
- Medyan > Ortalama → Müşterilerin çoğunluğu **orta-yüksek fiyat segmentinde**
- Düşük fiyatlı segment ($18-35) muhtemelen basic hizmetler
- Yüksek fiyatlı segment ($90-118) muhtemelen premium/fiber hizmetler

**🎯 Modelleme Etkisi:**
- Churn ile ilişkisi güçlü olabilir (yüksek ücret → yüksek churn?)
- Dönüşüm gerektirmiyor (düşük çarpıklık)
- Feature engineering fırsatı: 
  - "MonthlyCharges / tenure" → Müşteri başına ortalama aylık gelir
  - "TotalCharges / MonthlyCharges" → Tahmin edilen müşteri süresi
  - Price sensitivity segmentation

### Kategorik Değişkenler Yorumu

#### Hedef Değişken: Churn (%73.46 - %26.54)
PHASE 1'de tespit ettiğimiz **hafif dengesizlik** görselleştirme ile doğrulandı. Bu oran:
- **Telekom sektörü için normal** kabul edilir
- **Modelleme için yönetilebilir** seviyede (kritik dengesizlik %90+ olurdu)
- Stratified sampling zorunlu
- Metrik seçimi kritik: **Accuracy değil, F1-score, Precision-Recall, ROC-AUC** kullanılmalı

#### Hizmet Değişkenleri Pattern'i
Çoğu hizmet değişkeni **3 kategori** içeriyor:
- **Yes** (hizmet var)
- **No** (hizmet yok)
- **"No internet service"** veya **"No phone service"** (ilgili altyapı yok)

Bu yapı **hiyerarşik bağımlılık** yaratıyor:
- InternetService = "No" ise → OnlineSecurity, OnlineBackup vb. otomatik olarak "No internet service"
- PhoneService = "No" ise → MultipleLines otomatik olarak "No phone service"

**Data Prep Expert önerisi:** Bu kategorileri **binary'ye (0/1) dönüştürürken** "No" ve "No service" aynı kategori olarak ele alınmalı.

#### TotalCharges - Kritik Veri Kalitesi Sorunu
**6,531 eşsiz değer** ile **%92.73 kardinalite** gösteren TotalCharges değişkeni:
- **Kategorik değil, sayısal olmalıdır**
- Object tipinde olması veri kalitesi sorunu (PHASE 1 bulgusunu doğruluyoruz)
- Muhtemelen boşluk, whitespace veya özel karakter içeren satırlar var
- **PHASE 5'te detaylı inceleme ve temizlik gerekli**

**İş Mantığı:** TotalCharges = MonthlyCharges × tenure olmalı (yaklaşık olarak). Bu ilişki PHASE 4'te kontrol edilecek.

---

## ⚠️ Risk / Dikkat Edilmesi Gereken Noktalar

### 1. SeniorCitizen - Yüksek Çarpıklık ve Dengesizlik
**Risk Seviyesi:** 🟡 Orta  
**Açıklama:** Binary değişken olduğu için çarpıklık doğal, ancak %16 minority class modelde underrepresented olabilir.  
**Öneri:** Feature importance düşükse değişken çıkarma değerlendirilebilir; yüksekse class-weighted model veya stratified cross-validation.

### 2. TotalCharges - Veri Tipi ve Kardinalite Sorunu
**Risk Seviyesi:** 🔴 Yüksek  
**Açıklama:** 6,531 eşsiz değer ile kategorik değişken gibi görünüyor ancak sayısal olmalı. Modelleme öncesi mutlaka düzeltilmeli.  
**Öneri:** Data Prep Expert string'den numeric'e dönüşüm yapmalı, parse hatası verenleri (boşluk, whitespace) tespit edip imputasyon veya silme kararı vermelidir.

### 3. Hizmet Değişkenlerinde Hiyerarşik Bağımlılık
**Risk Seviyesi:** 🟡 Orta  
**Açıklama:** "No internet service" kategorisi aslında "No" ile aynı anlama geliyor, bu multicollinearity yaratabilir.  
**Öneri:** Data Prep Expert encoding sırasında bu kategorileri birleştirmeli (Yes=1, No/No service=0).

### 4. Hedef Değişken Dengesizliği
**Risk Seviyesi:** 🟡 Orta  
**Açıklama:** %73-27 dağılımı hafif dengesiz, model No sınıfına bias gösterebilir.  
**Öneri:** Stratified split + uygun metrik (F1, ROC-AUC) kullanımı zorunlu. SMOTE şu aşamada gerekli görünmüyor.

---

## 🔁 Agent Etkileşim Notu

### Data Prep Expert İçin Öneriler

| Öncelik | Sorun | Kanıt | Öneri |
|---|---|---|---|
| 🔴 Yüksek | TotalCharges yüksek kardinalite | 6,531 eşsiz değer (%92.73 kardinalite) | Rare label encoding, target encoding veya frequency encoding değerlendirilmelidir. **ANCAK** bu değişken aslında sayısal olmalı - önce numeric dönüşüm denenmelidir. |
| 🟡 Orta | SeniorCitizen yüksek çarpıklık | Skewness: 1.834 | Log, Box-Cox veya Yeo-Johnson dönüşümü değerlendirilmelidir. **ANCAK** binary değişken olduğu için dönüşüm mantıklı değil - class weighting yeterlidir. |
| 🟡 Orta | SeniorCitizen yüksek outlier oranı | Outlier oranı: %16.21 | Winsorization, robust scaler veya log dönüşümü değerlendirilmelidir. **ANCAK** binary değişken için outlier mantıklı değil - bu öneriye gerek yok. |

**🔍 Yeniden Değerlendirme:**  
SeniorCitizen için yapılan öneriler **binary değişken yapısı göz önüne alınarak revize edilmelidir**. Binary değişkenlerde çarpıklık ve outlier doğaldır, dönüşüm gerektirmez.

---

## 📁 Kaydedilen Çıktılar

- ✅ **reports/csv/phase2_numeric_summary.csv** - Sayısal değişken istatistikleri
- ✅ **reports/csv/phase2_categorical_summary.csv** - Kategorik değişken frekans özeti
- ✅ **reports/csv/phase2_data_prep_recommendations.csv** - Data Prep önerileri
- ✅ **23 adet grafik** (figures/ klasörü):
  - 3 histogram (sayısal değişkenler)
  - 3 boxplot (sayısal değişkenler)
  - 17 bar chart (kategorik değişkenler)

---

## 🎯 Sonraki Adım

PHASE 3'te **bivariate analysis** yapılacak:
- Hedef değişken (Churn) ile diğer değişkenler arasındaki ilişki incelenecek
- Sayısal değişken vs. Churn (boxplot, violin plot)
- Kategorik değişken vs. Churn (grouped bar, stacked bar)
- Churn oranlarının değişkenlere göre nasıl değiştiği analiz edilecek

---

**Tarih:** 5 Mayıs 2026  
**Analiz Sorumlusu:** EDA Expert  
**Durum:** ✅ Tamamlandı
