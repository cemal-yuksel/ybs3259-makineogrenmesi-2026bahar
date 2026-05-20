# PHASE 1: DATA OVERVIEW - VERİ SETİ GENEL YAPISI

## 📊 Yapılan Analiz

Bu aşamada veri setinin temel yapısını anlamak için kod üretildi ve çalıştırıldı. Veri boyutu, veri tipleri, eksik değer durumu, değişken yapısı ve hedef değişken belirleme işlemleri gerçekleştirildi.

---

## 🧠 Koddan Elde Edilen Bulgular

### 1. Veri Seti Boyutu
- **Satır sayısı:** 7,043
- **Sütun sayısı:** 21
- **Toplam hücre sayısı:** 147,903

### 2. Veri Tipleri ve Yapısı
- **Sayısal değişken:** 3 adet (`SeniorCitizen`, `tenure`, `MonthlyCharges`)
- **Kategorik değişken:** 18 adet
- **Bellek kullanımı:** 1.1+ MB

### 3. Eksik Değer Durumu
- İlk bakışta **hiçbir değişkende eksik değer görünmüyor**
- Tüm değişkenler 7,043 non-null değer içeriyor

### 4. Hedef Değişken: `Churn`
- **No (Müşteri kaldı):** 5,174 (73.46%)
- **Yes (Müşteri ayrıldı):** 1,869 (26.54%)
- **Dağılım:** Hafif dengesiz, baskın sınıf "No"

### 5. Sayısal Değişkenler İstatistikleri

| Değişken | Ortalama | Std. Sapma | Min | Max | Medyan |
|---|---|---|---|---|---|
| SeniorCitizen | 0.16 | 0.37 | 0 | 1 | 0 |
| tenure | 32.37 | 24.56 | 0 | 72 | 29 |
| MonthlyCharges | 64.76 | 30.09 | 18.25 | 118.75 | 70.35 |

### 6. Kategorik Değişkenler Kardinalitesi

| Değişken | Eşsiz Değer Sayısı | Kardinalite |
|---|---|---|
| customerID | 7,043 | %100 (Her satır benzersiz) |
| TotalCharges | 6,531 | %92.73 (Şüpheli - object tipinde) |
| MonthlyCharges | 1,585 | %22.50 |
| tenure | 73 | %1.04 |
| PaymentMethod | 4 | %0.06 |
| MultipleLines, InternetService, Contract | 3 | %0.04 |
| gender, Partner, Dependents, PhoneService, PaperlessBilling, Churn | 2 | %0.03 |

### 7. Veri Kalitesi Kontrolleri
- **Duplicate satır sayısı:** 0 ✅
- **customerID:** Her satır için benzersiz (ID değişkeni, modellemeden çıkarılmalı)
- **TotalCharges:** Object tipinde ama sayısal olmalı ⚠️

---

## 💡 Analitik Yorum (YBS Uzmanı Perspektifi)

### Veri Seti Büyüklüğü ve Yeterliliği
Veri seti **7,043 satır** içeriyor. Bu boyut, geleneksel makine öğrenmesi modelleri için yeterli kabul edilebilir; ancak derin öğrenme için sınırlı olabilir. **21 değişken** ile feature-to-sample oranı makul düzeydedir ve overfitting riski düşüktür.

### Hedef Değişken Dengesizliği
Hedef değişken `Churn` değişkeninde **%73.46 No - %26.54 Yes** dağılımı gözlendi. Bu oran **hafif dengesizlik** gösteriyor ancak kritik seviyede değil. Ancak modelleme aşamasında:
- **Sınıf ağırlıklandırma (class weighting)**
- **Stratified sampling**
- **Uygun metrik seçimi (F1-score, Precision-Recall, ROC-AUC)** 

değerlendirilmelidir. SMOTE gibi oversampling teknikleri şu aşamada gerekli görünmüyor; ancak model performansına göre Data Prep Expert tarafından değerlendirilebilir.

### Sayısal Değişkenlerin Yapısı
- **SeniorCitizen:** Binary değişken (0/1), ortalama 0.16 → %16 müşteri yaşlı
- **tenure:** 0-72 ay arası müşteri süresi, ortalama 32 ay, medyan 29 → Sağa çarpık dağılım olabilir
- **MonthlyCharges:** 18.25-118.75 arası aylık ücret, ortalama 64.76 → Geniş bir fiyat aralığı

### Kategorik Değişkenlerin Yapısı
Kategorik değişkenler genellikle **2-4 kategori** içeriyor, bu da **düşük kardinalite** anlamına gelir ve encoding işlemi kolay olacaktır. Ancak:
- **customerID** her satır için benzersizdir → **ID değişkeni, modellemeden çıkarılmalıdır**
- **TotalCharges** değişkeni **object tipinde** ancak mantıksal olarak sayısal olmalıdır → **Veri kalitesi sorunu olabilir**

### Kritik Veri Kalitesi Bulgusu: TotalCharges
`TotalCharges` değişkeni **object (string) tipinde** görünüyor ancak **sayısal** bir değişken olmalıdır (toplam ücret). Bu durum şu sebeplerden olabilir:
- Boş değerler veya whitespace karakterleri
- Sayısal olmayan karakterler (örn: "$", ",", " ")
- Gerçek eksik değerler boşluk olarak kodlanmış olabilir

**Bu değişken PHASE 5'te detaylı incelenmelidir.** Dönüşüm ve temizlik işlemi Data Prep Expert tarafından yapılmalıdır.

### İş Değeri Açısından İçgörüler
- **Müşteri kaybı oranı %26.54**, bu telekom sektörü için normal kabul edilebilir bir churn oranıdır
- **tenure (müşteri süresi)** değişkeninin geniş aralığı (0-72 ay) güçlü bir churn göstergesi olabilir
- **MonthlyCharges** değişkeninin yüksek standart sapması (30.09), farklı fiyatlandırma stratejilerinin varlığına işaret ediyor

---

## ⚠️ Risk / Dikkat Edilmesi Gereken Noktalar

### 1. TotalCharges Veri Tipi Sorunu
**Risk Seviyesi:** 🔴 Yüksek  
**Açıklama:** TotalCharges değişkeni object tipinde ancak sayısal olmalıdır. Bu durum modelleme öncesi mutlaka çözülmelidir.

### 2. Hedef Değişken Dengesizliği
**Risk Seviyesi:** 🟡 Orta  
**Açıklama:** %73.46 - %26.54 dağılımı hafif dengesizlik gösteriyor. Model bias'ı baskın sınıf yönünde olabilir.

### 3. customerID Değişkeni
**Risk Seviyesi:** 🟢 Düşük (kolay çözüm)  
**Açıklama:** ID değişkeni modellemede kullanılmamalıdır, aksi takdirde model unique ID'leri öğrenmeye çalışır (data leakage).

---

## 🔁 Agent Etkileşim Notu

### Data Prep Expert İçin Öneriler

| Öncelik | Sorun | Kanıt | Öneri |
|---|---|---|---|
| 🔴 Yüksek | TotalCharges veri tipi uyumsuzluğu | TotalCharges değişkeni object tipinde ancak sayısal olmalıdır | Data Prep Expert bu değişkeni numeric'e dönüştürmeli, dönüşüm hatası verenleri tespit edip uygun şekilde işlemelidir (imputasyon veya satır silme) |
| 🟡 Orta | Hedef değişken dengesizliği | Churn değişkeninde %73.46 No - %26.54 Yes dağılımı | Modelleme aşamasında stratified split, class weighting veya uygun metrik seçimi (F1-score, ROC-AUC) değerlendirilmelidir |
| 🟢 Düşük | ID değişkeni | customerID her satır için benzersiz, %100 kardinalite | customerID değişkeni modellemeden çıkarılmalıdır |

---

## 📁 Kaydedilen Çıktılar

- ✅ **reports/csv/phase1_data_overview.csv** - Değişken özet tablosu

---

## 🎯 Sonraki Adım

PHASE 2'de **univariate analysis** yapılacak, her değişkenin tek başına dağılımı, skewness, outlier yapısı ve kategorik değişkenlerin frekans dağılımları incelenecektir.

---

**Tarih:** 5 Mayıs 2026  
**Analiz Sorumlusu:** EDA Expert  
**Durum:** ✅ Tamamlandı
