# PHASE 6: INSIGHT GENERATION - İçgörü ve Strateji Raporu

## 📊 Amaç:

Bu aşamada **Phase 1-5'ten elde edilen teknik bulgular**, iş değerine ve modelleme stratejisine dönüştürülmektedir. Teknik analizler yorumlanarak:
1. En önemli 5 içgörü
2. İş değeri yüksek 3 bulgu
3. Modelleme için kritik 5 değişken
4. Veri kalitesi açısından en riskli alanlar
5. Feature engineering fırsatları
6. Data Prep Expert için nihai öneri listesi

---

## 🎯 İÇGÖRÜ 1: Glucose, Diyabetin Altın Standart Öngörücüsü

**Kanıt:**
- Phase 3: Mann-Whitney U p<0.0001 (en güçlü istatistiksel ilişki)
- Phase 4: Pearson r=0.467 (en yüksek korelasyon)
- Ortalama fark: Diyabet var vs yok → 141.26 vs 109.98 (%28.4 artış)

**İş Değeri:**
- Glucose tek başına diyabet tahmini için kullanılabilir.
- Eğer modelde sadece 1 değişken seçilecek olsaydı, **Glucose** seçilmeliydi.
- Glucose eksikse veya güvenilir değilse, model performansı ciddi oranda düşecektir.

**Modelleme Etkisi:**
- Feature importance: En yüksek (muhtemelen %30-40 arası)
- Glikoz seviyesi >140 olan hastalarda diyabet riski çok yüksek
- Feature engineering: `High_Glucose` (>140) binary feature oluşturulabilir

**Öneri:**
- Glucose, kesinlikle tüm modellerde bulunmalı.
- %0.65 oranında gizli eksik veri var - median imputation yeterli.

---

## 🎯 İÇGÖRÜ 2: BMI ve Age, Diyabet Riskinin İkili Motor Değişkenleri

**Kanıt:**
- BMI: Pearson r=0.293, ortalama fark %16 (30.30 vs 35.14)
- Age: Pearson r=0.238, ortalama fark %18.8 (31.19 vs 37.07)
- BMI ve Age birlikte hareket ediyor (korelasyon: 0.036 - bağımsızlar)

**İş Değeri:**
- BMI >30 (obezite eşiği) ve Age >40 olan hastalarda diyabet riski katlanarak artıyor.
- Bu iki değişken **demografik risk profili** oluşturmak için kullanılabilir.
- Sağlık kuruluşları, bu risk grubuna **önleyici müdahale** yapabilir.

**Modelleme Etkisi:**
- Her iki değişken de güçlü öngörücü.
- **Interaction feature**: `BMI_Age = BMI * Age` oluşturulabilir.
- Feature engineering: `High_BMI_Old_Age` (BMI>30 AND Age>40) binary feature

**Öneri:**
- Bu iki değişken kesinlikle modelde olmalı.
- Interaction feature oluşturularak model performansı artırılabilir.

---

## 🎯 İÇGÖRÜ 3: Insulin ve SkinThickness, "Hayalet Değişkenler" - Modelden Çıkarılmalı

**Kanıt:**
- Insulin: %48.70 gizli eksik veri, istatistiksel olarak anlamsız (p=0.0657), zayıf korelasyon (r=0.131)
- SkinThickness: %29.56 gizli eksik veri, zayıf ilişki (p=0.0130), çok zayıf korelasyon (r=0.075)
- Bu iki değişkenin verilerinin çoğu **"uydurulmuş"** olacak (imputasyon yapılırsa)

**İş Değeri:**
- Model, gerçek veri yerine **tahmin edilen veriye göre öğrenecek**.
- Bu, **overfitting ve düşük test accuracy** demektir.
- Gerçek dünya uygulamasında model başarısız olacak.

**Modelleme Etkisi:**
- Bu değişkenler modelde tutulursa:
  - Training accuracy yüksek, test accuracy düşük olacak
  - Overfitting riski çok yüksek
  - Model genelleme yapamayacak
- Bu değişkenler modelden çıkarılırsa:
  - Daha sağlam model
  - Daha güvenilir genelleme
  - Daha yüksek test accuracy

**Öneri:**
- **Baseline model:** Insulin ve SkinThickness dahil değil (önerilen)
- **Advanced model:** İleri imputasyon denenebilir ama riskli
- **Karşılaştırma yapılmalı:** Hangi model daha iyi validation score veriyorsa o kullanılmalı

---

## 🎯 İÇGÖRÜ 4: BloodPressure, "Üçlü Sorunlu" Değişken - Dikkatli Kullanılmalı

**Kanıt:**
- %4.56 gizli eksik veri
- %5.86 outlier oranı (kritik eşiğin üzerinde)
- -1.844 negatif çarpıklık (aşırı)
- İstatistiksel olarak anlamlı (p<0.001) ama korelasyon çok düşük (r=0.065)

**İş Değeri:**
- BloodPressure, diyabet ile **non-lineer** bir ilişkiye sahip olabilir.
- Lineer modeller (LogisticRegression) bu ilişkiyi yakalayamayabilir.
- Tree-based modeller (RandomForest, XGBoost) bu ilişkiyi yakalayabilir.

**Modelleme Etkisi:**
- Lineer modeller: BloodPressure'dan yararlanamayabilir
- Tree-based modeller: BloodPressure'ı daha iyi kullanabilir
- **Preprocessing gerekli:** 0→NaN, outlier winsorization, Yeo-Johnson dönüşümü

**Öneri:**
- BloodPressure modelde tutulabilir ama **dikkatli preprocessing gerekli**.
- Tree-based modeller tercih edilmeli.

---

## 🎯 İÇGÖRÜ 5: Class Imbalance Orta Seviyede - Stratified CV Şart

**Kanıt:**
- Diyabet yok (0): 500 kişi (%65.1)
- Diyabet var (1): 268 kişi (%34.9)
- Baskın sınıf oranı: %65.1 (kritik eşik %70)

**İş Değeri:**
- Model, "her zaman 0 tahmin et" stratejisi ile %65.1 accuracy elde edebilir.
- Accuracy tek başına **yanıltıcı** bir metrik olacak.
- **Precision, Recall, F1-Score** gibi metrikler kullanılmalı.

**Modelleme Etkisi:**
- **Stratified K-Fold CV** kullanılmalı (her fold'da %65-35 oranı korunmalı)
- **Class weighting** uygulanmalı (azınlık sınıfına daha fazla ağırlık)
- **SMOTE** (Synthetic Minority Over-sampling) denenebilir (riskli)
- **Evaluation metrikleri:** Accuracy, Precision, Recall, F1-Score, ROC-AUC

**Öneri:**
- Stratified K-Fold CV kesinlikle kullanılmalı.
- Class weighting parametresi açılmalı (`class_weight='balanced'`).
- F1-Score ve ROC-AUC metriklerine odaklanılmalı.

---

## 💼 İŞ DEĞERİ YÜKSEK 3 BULGU

### **1. Risk Profili Segmentasyonu (Yüksek İş Değeri)**

**Bulgu:**
- Glucose >140, BMI >30, Age >40 olan hastalarda diyabet riski çok yüksek

**İş Değeri:**
- Sağlık kuruluşları, bu risk grubuna **önleyici müdahale** yapabilir
- Erken teşhis ve tedavi maliyetleri azaltır
- Hasta memnuniyeti artar

**Uygulama:**
```python
# Risk segmentasyonu
df['Risk_Segment'] = 'Düşük Risk'
df.loc[(df['Glucose'] > 140) & (df['BMI'] > 30), 'Risk_Segment'] = 'Orta Risk'
df.loc[(df['Glucose'] > 140) & (df['BMI'] > 30) & (df['Age'] > 40), 'Risk_Segment'] = 'Yüksek Risk'
```

### **2. Modelin Gerçek Dünya Uygulanabilirliği (Yüksek İş Değeri)**

**Bulgu:**
- Insulin ve SkinThickness ölçümleri güvenilir değil (yüksek eksik veri)
- Bu değişkenler modelden çıkarılırsa, model **daha az feature ile çalışacak**

**İş Değeri:**
- Model, **daha az ölçüm** ile tahmin yapabilecek
- Maliyet azalır (daha az test)
- Hasta konforu artar (daha az invaziv)
- **Pratik uygulanabilirlik** artar

**Uygulama:**
- Baseline model: 6 değişken (Glucose, Pregnancies, BMI, Age, DiabetesPedigreeFunction, BloodPressure)
- Bu model, **pratik ve güvenilir** bir tahmin aracı olabilir

### **3. Veri Toplama Sürecinin İyileştirilmesi (Yüksek İş Değeri)**

**Bulgu:**
- Eksik veriler **0 olarak kodlanmış** (veri kalitesi sorunu)
- Bu, veri toplama aşamasında sistematik bir sorunu gösteriyor

**İş Değeri:**
- Gelecekteki veri toplama süreçleri iyileştirilebilir
- Eksik veriler **NaN olarak kodlanmalı** (0 değil)
- Veri kalitesi artar, model performansı artar

**Öneri:**
- Veri toplama formları güncellenebilir
- Eksik veri alanları **"Bilinmiyor"** veya **NaN** olarak işaretlenebilir

---

## 🔑 MODELLEME İÇİN KRİTİK 5 DEĞİŞKEN

| Sıra | Değişken | Öncelik | Gerekçe |
|------|----------|---------|---------|
| 1 | **Glucose** | 🔴 Kritik | En güçlü öngörücü (r=0.467), istatistiksel olarak çok anlamlı |
| 2 | **BMI** | 🔴 Kritik | İkinci en güçlü öngörücü (r=0.293), obezite-diyabet ilişkisi |
| 3 | **Age** | 🟠 Yüksek | Üçüncü en güçlü öngörücü (r=0.238), yaş-risk ilişkisi |
| 4 | **Pregnancies** | 🟠 Yüksek | Dördüncü en güçlü öngörücü (r=0.222), gestational diabetes ilişkisi |
| 5 | **DiabetesPedigreeFunction** | 🟡 Orta | Beşinci en güçlü öngörücü (r=0.174), genetik risk |

**Ek Değişken (opsiyonel):**
- **BloodPressure** (🟡 Orta): Dikkatli preprocessing gerekliFinal Feature Set (Önerilen):
- `selected_features = ['Glucose', 'BMI', 'Age', 'Pregnancies', 'DiabetesPedigreeFunction', 'BloodPressure']`

---

## ⚠️ VERİ KALİTESİ AÇISINDAN EN RİSKLİ ALANLAR

### **1. Insulin (🚨 Çok Yüksek Risk)**
- %48.70 eksik veri
- İstatistiksel olarak anlamsız
- **Strateji:** Modelden çıkar

### **2. SkinThickness (⚠️ Yüksek Risk)**
- %29.56 eksik veri
- Zayıf ilişki
- **Strateji:** Modelden çıkar

### **3. BloodPressure (⚠️ Orta Risk)**
- Gizli eksik veri + Outlier + Çarpıklık
- **Strateji:** Dikkatli preprocessing

### **4. Class Imbalance (⚠️ Orta Risk)**
- %65-35 oranı
- **Strateji:** Stratified CV + Class weighting

---

## 🛠️ FEATURE ENGINEERING FIRSATLARI

### **1. Binary Features (Önerilen)**

```python
# Yüksek risk göstergeleri
df['High_Glucose'] = (df['Glucose'] > 140).astype(int)
df['High_BMI'] = (df['BMI'] > 30).astype(int)
df['Old_Age'] = (df['Age'] > 40).astype(int)
df['Many_Pregnancies'] = (df['Pregnancies'] > 5).astype(int)

# Kombine risk
df['High_Risk_Profile'] = (
    (df['Glucose'] > 140) & 
    (df['BMI'] > 30) & 
    (df['Age'] > 40)
).astype(int)
```

### **2. Interaction Features (Önerilen)**

```python
# En güçlü değişkenlerin interactionları
df['BMI_Age'] = df['BMI'] * df['Age']
df['Glucose_BMI'] = df['Glucose'] * df['BMI']
df['Glucose_Age'] = df['Glucose'] * df['Age']
df['Pregnancies_Age'] = df['Pregnancies'] * df['Age']
```

**Rationale:**
- BMI ve Age birlikte yüksekse, risk katlanarak artıyor olabilir
- Glucose ve BMI birlikte yüksekse, metabolik sendrom riski

### **3. Polynomial Features (Opsiyonel, Riskli)**

```python
from sklearn.preprocessing import PolynomialFeatures

# Sadece interaction terimler, quadratic değil
poly = PolynomialFeatures(degree=2, include_bias=False, interaction_only=True)
X_poly = poly.fit_transform(X)
```

**Risk:** Overfitting riski artırır, dikkatli kullanılmalı

---

## 📋 DATA PREP EXPERT İÇİN NİHAİ ÖNERİ LİSTESİ

### **Yüksek Öncelik (Kesinlikle Yapılmalı)**

1. **Gizli Eksik Veri Yönetimi:**
   - Glucose, BloodPressure, BMI: 0 → NaN → median imputation
   - Insulin ve SkinThickness: Modelden çıkar (önerilen)

2. **Feature Selection:**
   - Baseline: Glucose, Pregnancies, BMI, Age, DiabetesPedigreeFunction, BloodPressure

3. **Train-Test Split:**
   - Stratified split (80-20)
   - Random state: 42 (reproducibility)

4. **Cross-Validation:**
   - Stratified K-Fold (k=5)

### **Orta Öncelik (Önerilir)**

5. **Outlier Yönetimi:**
   - BloodPressure: Winsorization (%5-95)

6. **Çarpıklık Dönüşümü:**
   - Yeo-Johnson (tüm sayısal değişkenler)

7. **Feature Engineering:**
   - Binary features: High_Glucose, High_BMI, Old_Age
   - Interaction features: BMI_Age, Glucose_BMI

8. **Class Weighting:**
   - `class_weight='balanced'` (tüm modellerde)

### **Düşük Öncelik (Opsiyonel)**

9. **SMOTE:**
   - Synthetic minority over-sampling (riskli, overfitting olabilir)

10. **Advanced İmputasyon:**
    - Insulin ve SkinThickness için IterativeImputer (riskli, karşılaştırma yapılmalı)

---

## ✅ Phase 6 Tamamlandı - Sırada: Phase 7 (Model Readiness Assessment)
