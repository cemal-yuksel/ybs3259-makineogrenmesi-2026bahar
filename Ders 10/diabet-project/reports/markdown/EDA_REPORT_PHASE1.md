# Keşifsel Veri Analizi Raporu - Diabetes Dataset

**Proje:** Diabetes Tahmin Modeli  
**Veri Seti:** diabetes.csv  
**Analiz Tarihi:** 5 Mayıs 2026  
**Analyst:** EDA Expert (Agentik)  

---

## 📊 PHASE 1: DATA OVERVIEW

### Yapılan Analiz:

Bu aşamada diabetes.csv veri seti yüklenmiş, temel yapısal özellikler incelenmiş, veri tipleri analiz edilmiş, eksik veri durumu değerlendirilmiş ve potansiyel hedef değişken belirlenmiştir. Kod phase1_data_overview.py dosyasında üretilip çalıştırılmıştır.

---

### 🧠 Koddan Elde Edilen Bulgular:

**Veri Seti Boyutu:**
- **768 satır** ve **9 sütun** içeren orta ölçekli bir veri seti
- Tüm değişkenler sayısal tipte (7 int64, 2 float64)
- Kategorik değişken bulunmamaktadır

**Değişken Profili:**
1. `Pregnancies` (int64): Hamilelik sayısı
2. `Glucose` (int64): Glikoz seviyesi
3. `BloodPressure` (int64): Kan basıncı
4. `SkinThickness` (int64): Cilt kalınlığı
5. `Insulin` (int64): İnsülin seviyesi
6. `BMI` (float64): Vücut Kitle İndeksi
7. `DiabetesPedigreeFunction` (float64): Diyabet soy ağacı fonksiyonu
8. `Age` (int64): Yaş
9. `Outcome` (int64): **Hedef değişken** (0: Diyabet yok, 1: Diyabet var)

**Eksik Veri Durumu:**
- Teknik olarak **eksik veri bulunmamaktadır** (tüm hücreler dolu)
- Ancak bazı değişkenlerde **mantıksal olarak imkansız 0 değerleri** tespit edildi:
  - Glucose minimum: 0 (glikoz seviyesi 0 olamaz)
  - BloodPressure minimum: 0 (kan basıncı 0 olamaz)
  - SkinThickness minimum: 0
  - Insulin minimum: 0
  - BMI minimum: 0 (BMI 0 olamaz)

**Hedef Değişken Dağılımı:**
- **Outcome = 0 (Diyabet yok):** 500 kişi (%65.1)
- **Outcome = 1 (Diyabet var):** 268 kişi (%34.9)
- **Dengesiz dağılım** var; baskın sınıf %65.1

**Veri Kalitesi:**
- Duplicate satır: **0** (veri temiz)
- Tüm değişkenler sayısal olduğu için encoding ihtiyacı yok

---

### 💡 Analitik Yorum:

**Veri Seti Yapısı:**
- 768 gözlem, makine öğrenmesi için kabul edilebilir bir örneklem büyüklüğüdür. Ancak derin öğrenme için küçük kalabilir.
- Veri seti tamamı sayısal değişkenlerden oluştuğu için kategorik encoding ihtiyacı yoktur, bu bir avantajdır.
- Tüm değişkenler tıbbi ölçümler olduğu için birbiriyle ilişkili olma olasılığı yüksektir; multicollinearity kontrolü gerekecektir.

**Hedef Değişken Analizi:**
- Outcome değişkeni binary classification problemi için uygundur.
- %65-35 dağılımı, orta derecede dengesizlik gösterir. Model eğitiminde **class weighting** veya **SMOTE** gibi yöntemler düşünülmelidir.
- Baskın sınıf "Diyabet yok" olduğu için, model eğitiminde accuracy tek başına yeterli metrik olmayacak; **precision, recall, F1-score** gibi metrikler de kullanılmalıdır.

**Kritik Veri Kalitesi Sorunu:**
- Bazı tıbbi ölçümlerde (Glucose, BloodPressure, BMI, Insulin, SkinThickness) **0 değeri mantıksal olarak imkansızdır**.
- Bu durum, veri toplama aşamasında **eksik verilerin 0 ile kodlandığını** gösteriyor.
- Bu "gizli eksik veriler" phase 5'te detaylı analiz edilecek ve Data Prep Expert için yüksek öncelikli öneri oluşturulacaktır.

---

### ⚠️ Risk / Dikkat Edilmesi Gereken Nokta:

1. **Gizli Eksik Veri Riski (Kritik):**
   - Glucose, BloodPressure, BMI, Insulin, SkinThickness değişkenlerinde 0 değerleri eksik veri olarak ele alınmalıdır.
   - Bu değişkenlerde 0 değerlerinin oranı hesaplanmalı ve imputasyon stratejisi geliştirilmelidir.

2. **Hedef Değişken Dengesizliği (Orta):**
   - %65-35 oranı orta derecede dengesizlik gösterir.
   - Model eğitiminde class imbalance stratejileri uygulanmalıdır.

3. **Örneklem Büyüklüğü (Düşük Risk):**
   - 768 gözlem klasik ML için yeterli, ancak ensemble ve complex modeller için sınırlı olabilir.
   - Cross-validation stratejisi dikkatli seçilmelidir.

---

### 🔁 Agent Etkileşim Notu:

**Data Prep Expert için Öneriler:**

1. **Gizli Eksik Veri Yönetimi (Yüksek Öncelik):**
   - Glucose, BloodPressure, BMI, Insulin, SkinThickness değişkenlerinde 0 değerlerini NaN'a dönüştür.
   - Her değişken için 0 oranını hesapla.
   - %5'in altındaysa median/mean imputation, üzerindeyse advanced imputation (KNN, iterative) düşün.
   - Alternatif olarak "missing indicator" feature'ı oluşturulabilir.

2. **Class Imbalance Stratejisi (Orta Öncelik):**
   - SMOTE (Synthetic Minority Over-sampling Technique) değerlendirilebilir.
   - Class weighting uygulanabilir.
   - Stratified K-Fold CV kullanılmalıdır.

3. **Train-Test Split (Yüksek Öncelik):**
   - **Stratified split** kesinlikle kullanılmalıdır.
   - Test seti en az %20 olmalı (kabul edilebilir minimum örneklem için).

---

### 📁 Kaydedilen Dosyalar:

- `reports/csv/phase1_data_overview.csv`: Tüm değişkenlerin genel özeti

---

### ✅ Phase 1 Tamamlandı - Sırada: Phase 2 (Univariate Analysis)
