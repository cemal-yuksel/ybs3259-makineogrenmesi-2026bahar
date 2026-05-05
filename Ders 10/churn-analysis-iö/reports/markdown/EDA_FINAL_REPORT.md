# 📊 Keşifsel Veri Analizi (EDA) Final Raporu

**Proje:** Telekom Müşteri Churn Analizi  
**Veri Seti:** churn.csv  
**Tarih:** 5 Mayıs 2026  
**Analiz Türü:** 7 Aşamalı Agentik EDA (CRISP-DM Metodolojisi)  
**Hazırlayan:** EDA Expert

---

## 📋 İçindekiler

1. [Yönetici Özeti](#yönetici-özeti)
2. [Veri Setinin Genel Profili](#veri-setinin-genel-profili)
3. [Kritik Teknik Bulgular](#kritik-teknik-bulgular)
4. [İş Değeri Açısından İçgörüler](#iş-değeri-açısından-içgörüler)
5. [Data Prep Expert İçin Öneriler](#data-prep-expert-için-öneriler)
6. [Model Hazırlık Değerlendirmesi](#model-hazırlık-değerlendirmesi)
7. [Sonuç ve Yol Haritası](#sonuç-ve-yol-haritası)

---

## 1. Yönetici Özeti

### 🎯 Temel Bulgular

Bu analiz, 7,043 telekom müşterisini kapsayan churn veri seti üzerinde gerçekleştirilmiştir. Veri kalitesi **çok yüksek** olup, sadece 11 eksik değer (%0.16) ve hiç duplicate satır bulunmamaktadır.

**Kritik İş Bulguları:**

- **Churn Oranı:** %26.54 (1,869 müşteri) - iş açısından kritik bir seviye
- **En Riskli Segment:** Month-to-month sözleşme + Fiber optic internet kullanan müşteriler (%42.71 churn)
- **En Güvenli Segment:** Two year sözleşmeli müşteriler (%2.83 churn - 15 kat daha düşük)
- **Kritik Risk Dönemi:** İlk 18 ay (churn eden müşterilerin ortalama tenure'u 18 ay)
- **Fiyatlandırma Etkisi:** Churn eden müşteriler ortalama $13 daha fazla ödüyor ($74.44 vs $61.27)

**Modelleme Potansiyeli:**

- En güçlü prediktörler: **tenure, Contract, InternetService, MonthlyCharges, PaymentMethod**
- Veri minimal preprocessing gerektiriyor
- Kritik öneri: **TotalCharges değişkenini çıkar** (leakage + multicollinearity riski)

---

## 2. Veri Setinin Genel Profili

### 📐 Boyut ve Yapı

| Metrik | Değer |
|--------|-------|
| Toplam Satır | 7,043 |
| Toplam Sütun | 21 |
| Sayısal Değişken | 4 (SeniorCitizen, tenure, MonthlyCharges, TotalCharges) |
| Kategorik Değişken | 17 |
| Hedef Değişken | Churn (Binary: Yes/No) |
| Eksik Veri | 11 değer (sadece TotalCharges) - %0.16 |
| Duplicate Satır | 0 |

### 🎯 Hedef Değişken Dağılımı

| Sınıf | Frekans | Oran |
|-------|---------|------|
| No (Kalan Müşteri) | 5,174 | %73.46 |
| Yes (Churn Eden) | 1,869 | %26.54 |

**Yorum:** Hedef değişken makul dengede. SMOTE/ADASYN gibi aggressive sampling tekniklerine gerek yok, stratified split yeterli.

---

## 3. Kritik Teknik Bulgular

### 🔢 3.1. Sayısal Değişkenler Analizi

#### **tenure (Müşteri Süresi)**

| Metrik | Churn=No | Churn=Yes | Fark |
|--------|----------|-----------|------|
| Ortalama | 37.57 ay | 17.98 ay | **-52%** |
| Medyan | 38.0 ay | 10.0 ay | -74% |
| t-statistic | -31.58 | | |
| p-value | <0.0001 | | ✅ Anlamlı |

**Kritik Bulgu:** Churn eden müşterilerin ortalama tenure'u yarı yarıya daha düşük. İlk 18 ay **kritik risk dönemi**.

**İş Etkisi:** Yeni müşterilere özel sadakat programları ve onboarding süreçleri tasarlanmalı.

---

#### **MonthlyCharges (Aylık Ücret)**

| Metrik | Churn=No | Churn=Yes | Fark |
|--------|----------|-----------|------|
| Ortalama | $61.27 | $74.44 | **+21%** |
| Medyan | $64.43 | $79.65 | +24% |
| t-statistic | 16.54 | | |
| p-value | <0.0001 | | ✅ Anlamlı |

**Kritik Bulgu:** Churn eden müşteriler ortalama $13.17 daha fazla ödüyor.

**İş Etkisi:** Yüksek ücretlendirme churn riskini artırıyor. Premium segment için value proposition gözden geçirilmeli.

---

#### **TotalCharges - ⚠️ LEAKAGE RİSKİ**

| Analiz | Sonuç |
|--------|-------|
| tenure ile Korelasyon | **0.8259** (çok yüksek) |
| VIF Değeri | **8.08** (orta-yüksek) |
| İlişki | TotalCharges ≈ tenure × MonthlyCharges |

**Kritik Öneri:** TotalCharges **modelden çıkarılmalı**. Bağımsız bilgi taşımıyor ve leakage riski var.

---

### 📊 3.2. Kategorik Değişkenler Analizi

#### **Contract (Sözleşme Tipi) - EN KRİTİK DEĞİŞKEN**

| Kategori | Churn Oranı | Chi-Square |
|----------|-------------|------------|
| Month-to-month | **%42.71** | 1184.60 |
| One year | %11.27 | (p<0.0001) |
| Two year | **%2.83** | ✅ Çok Anlamlı |

**Kritik Bulgu:** Two year sözleşmelerde churn oranı **15 kat daha düşük**.

**İş Etkisi:** Uzun vadeli sözleşmeye geçiş teşvikleri en etkili churn azaltma stratejisi olabilir.

---

#### **InternetService - FİBER OPTİC SORUNU**

| Kategori | Churn Oranı | Chi-Square |
|----------|-------------|------------|
| Fiber optic | **%41.89** | 732.31 |
| DSL | %18.96 | (p<0.0001) |
| No | %7.40 | ✅ Çok Anlamlı |

**Kritik Bulgu:** Fiber optic müşterileri beklenmedik şekilde en yüksek churn oranına sahip.

**İş Etkisi:** Fiber optic hizmet kalitesi, beklenti yönetimi veya rekabet durumu araştırılmalı.

---

#### **PaymentMethod - ÖDEME YÖNTEM ETKİSİ**

| Kategori | Churn Oranı | Chi-Square |
|----------|-------------|------------|
| Electronic check | **%45.29** | 648.14 |
| Mailed check | %19.11 | (p<0.0001) |
| Bank transfer (auto) | %16.71 | ✅ Çok Anlamlı |
| Credit card (auto) | %15.24 | |

**Kritik Bulgu:** Manuel ödeme yöntemi (electronic check) churn riskini **3 kat** artırıyor.

**İş Etkisi:** Otomatik ödeme teşvikleri churn'ü önemli ölçüde azaltabilir.

---

#### **OnlineSecurity & TechSupport - EK HİZMET ETKİSİ**

| Hizmet | No (Churn) | Yes (Churn) | Fark |
|--------|------------|-------------|------|
| OnlineSecurity | %41.77 | %14.61 | **-65%** |
| TechSupport | %41.64 | %15.17 | **-64%** |

**Kritik Bulgu:** Value-added services müşteri bağlılığını dramatik şekilde artırıyor.

**İş Etkisi:** Cross-sell ve bundle stratejileri churn azaltmanın etkili yolu.

---

### 🔗 3.3. Multivariate Analiz

#### Korelasyon Matrisi (Sayısal Değişkenler)

|  | SeniorCitizen | tenure | MonthlyCharges | TotalCharges |
|---|---|---|---|---|
| SeniorCitizen | 1.000 | 0.017 | 0.220 | 0.102 |
| tenure | 0.017 | 1.000 | 0.248 | **0.826** |
| MonthlyCharges | 0.220 | 0.248 | 1.000 | 0.651 |
| TotalCharges | 0.102 | **0.826** | 0.651 | 1.000 |

**Kritik Uyarı:** tenure ve TotalCharges arasında yüksek korelasyon (0.826) - multicollinearity riski.

---

#### VIF (Variance Inflation Factor) Analizi

| Değişken | VIF | Risk Seviyesi |
|----------|-----|---------------|
| TotalCharges | **8.08** | ⚠️ Orta-Yüksek |
| tenure | **6.32** | ⚠️ Orta |
| MonthlyCharges | 3.70 | ✅ Düşük |
| SeniorCitizen | 1.26 | ✅ Çok Düşük |

**Yorum:** TotalCharges ve tenure arasında orta düzey multicollinearity var. TotalCharges modelden çıkarılmalı.

---

### 🔍 3.4. Veri Kalitesi Değerlendirmesi

#### Eksik Veri

| Değişken | Eksik Sayı | Oran |
|----------|------------|------|
| TotalCharges | 11 | %0.16 |
| Diğer tüm değişkenler | 0 | %0.00 |

**Durum:** ✅ Çok iyi. Minimal eksik veri.

---

#### Outlier Analizi (IQR Yöntemi)

| Değişken | Outlier Oranı | Durum |
|----------|---------------|-------|
| SeniorCitizen | %16.21 | ⚠️ Yüksek (ama binary değişken - normal) |
| tenure | %0.00 | ✅ Yok |
| MonthlyCharges | %0.00 | ✅ Yok |
| TotalCharges | %0.00 | ✅ Yok |

**Durum:** ✅ Çok iyi. SeniorCitizen binary olduğu için outlier tanımı burada mantıklı değil.

---

#### Duplicate & Tutarlılık

| Kontrol | Sonuç |
|---------|-------|
| Duplicate Satır | ✅ 0 |
| Negatif Değerler | ✅ Yok |
| Kategorik Tutarlılık | ✅ Tutarlı |

**Durum:** ✅ Mükemmel. Veri kalitesi çok yüksek.

---

## 4. İş Değeri Açısından İçgörüler

### 💼 4.1. İlk 18 Ay Kritik Risk Dönemi

**Bulgu:** Churn eden müşterilerin ortalama tenure'u 18 ay, kalanların 38 ay.

**Açıklama:** İlk 18 ay müşteri kazanma maliyetini (CAC) karşılamadan kaybediliyor. Bu dönemde müşteri deneyimi ve bağlılık oluşturulamıyor.

**Aksiyon Önerileri:**
- İlk 6 ay özel onboarding programı
- 12-18. ayda sadakat programı başlatma
- Erken risk tespiti ve proaktif müdahale
- İlk yıl için özel fiyatlandırma/teşvik paketi

**Beklenen Etki:** İlk 18 aydaki churn %10 azalırsa, LTV önemli ölçüde artacak ve CAC payback süresi kısalacak.

---

### 💼 4.2. Fiber Optic Müşteri Memnuniyetsizliği

**Bulgu:** Fiber optic müşterileri %41.89 churn gösteriyor. DSL müşterileri sadece %18.96.

**Açıklama:** Premium hizmet olan fiber optic beklenmedik şekilde yüksek churn gösteriyor. Bu hizmet kalitesi, beklenti yönetimi, fiyatlandırma veya rekabet sorununa işaret ediyor.

**Aksiyon Önerileri:**
- Fiber optic hizmet kalitesi ve hız garantisi araştırması
- Müşteri beklentileri vs gerçek performans analizi
- Rekabetçi karşılaştırma (fiyat/performans)
- Fiber optic müşterilerine özel retention programı

**Beklenen Etki:** Fiber optic churn %10 puan azalırsa, yıllık ~300 müşteri kaybı önlenebilir.

---

### 💼 4.3. Uzun Vadeli Sözleşme = Düşük Churn

**Bulgu:** Two year sözleşmelerde churn %2.83, month-to-month'da %42.71. **15 kat fark**.

**Açıklama:** Uzun vadeli sözleşmeler müşteri bağlılığını dramatik şekilde artırıyor. Commitment barrier oluşturuyor ve switching cost yaratıyor.

**Aksiyon Önerileri:**
- Uzun vadeli sözleşmeye geçiş teşvikleri (ilk 3 ay %20 indirim)
- Ek hizmet bundling (OnlineSecurity + TechSupport + uzun vadeli sözleşme paketi)
- Early renewal incentive (sözleşme bitmeden 6 ay önce yenileme bonusu)
- Loyalty rewards programı

**Beklenen Etki:** Month-to-month müşterilerin %20'si 1-2 yıllık sözleşmeye geçerse, genel churn %5-7 azalabilir.

---

### 💼 4.4. Otomatik Ödeme Yöntemi Bağlılık Göstergesi

**Bulgu:** Electronic check kullananlar %45.29 churn, otomatik ödeme yapanlar ~%16 churn. **3 kat fark**.

**Açıklama:** Otomatik ödeme hem kolaylık hem de bağlılık (commitment) sağlıyor. Manuel ödeme her ay "churn kararı" fırsatı yaratıyor.

**Aksiyon Önerileri:**
- Otomatik ödeme kurulumuna teşvik (ilk 3 ay $5 indirim)
- Setup sürecini kolaylaştırma (tek tıkla otomatik ödeme)
- Güvenlik ve veri koruma mesajlaşması
- Otomatik ödeme kullanan müşterilere exclusive avantajlar

**Beklenen Etki:** Electronic check müşterilerinin %30'u otomatik ödemeye geçerse, ~150 müşteri kaybı önlenebilir.

---

### 💼 4.5. Value-Added Services Müşteri Tutma Aracı

**Bulgu:** OnlineSecurity, TechSupport, DeviceProtection gibi ek hizmetler churn'ü %20-25 puan azaltıyor.

**Açıklama:** Ek hizmetler müşteri bağlılığını artırıyor, switching cost yaratıyor ve perceived value artırıyor.

**Aksiyon Önerileri:**
- Cross-sell kampanyaları (churn risk skoru yüksek müşterilere hedefli)
- Bundle paketler (internet + security + support = %15 indirim)
- İlk ay ücretsiz deneme (commitment barrier azaltma)
- Value messaging ve education (müşteriler bu hizmetlerin değerini anlamalı)

**Beklenen Etki:** Ek hizmet penetrasyonu %10 artarsa, genel churn %2-3 puan azalabilir.

---

## 5. Data Prep Expert İçin Öneriler

### 🔴 5.1. Kritik Öncelikli Öneriler

#### **1. TotalCharges Değişkenini Çıkar**

**Sorun:** Yüksek korelasyon (0.8259) ve yüksek VIF (8.08). Leakage riski.

**Kanıt:**
- tenure ile korelasyon: 0.8259
- VIF: 8.08
- İlişki: TotalCharges = tenure × MonthlyCharges

**Öneri:** TotalCharges değişkenini kesinlikle modelden çıkar. Bağımsız bilgi taşımıyor ve modelde bias yaratabilir.

---

#### **2. Contract için Ordinal Encoding Kullan**

**Sorun:** Contract kategorik değişken ama mantıksal sırası var (month < year < two year).

**Kanıt:**
- Month-to-month: %42.71 churn
- One year: %11.27 churn
- Two year: %2.83 churn
- Doğrusal azalma var

**Öneri:** Ordinal Encoding kullan:
- month-to-month = 0
- one year = 1
- two year = 2

Bu, one-hot encoding'den daha efficient ve model için daha anlamlı.

---

### 🟡 5.2. Yüksek Öncelikli Öneriler

#### **3. Scaling Uygula**

**Sorun:** tenure (0-72) ve MonthlyCharges ($18-118) farklı ölçeklerde.

**Öneri:**
- StandardScaler veya MinMaxScaler kullan
- Tree-based modeller için opsiyonel, linear modeller için zorunlu

---

#### **4. Stratified Train-Test Split**

**Sorun:** Hedef değişkende hafif dengesizlik var (%26.54 churn).

**Öneri:**
```python
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, stratify=y, random_state=42
)
```

SMOTE gerekli değil - stratified split yeterli.

---

### 🟢 5.3. Orta Öncelikli Öneriler

#### **5. Eksik Değer İmputasyonu**

**Sorun:** TotalCharges'da 11 eksik değer (%0.16).

**Öneri:** TotalCharges modelden çıkarılacak, bu nedenle imputasyon gerekmeyebilir. Eğer kullanılacaksa:
```python
df['TotalCharges'] = df['tenure'] * df['MonthlyCharges']
```

---

#### **6. Feature Engineering**

**Öneri 1: tenure_group**
```python
def tenure_group(tenure):
    if tenure <= 12:
        return 'new'
    elif tenure <= 24:
        return 'medium'
    else:
        return 'loyal'
```

**Öneri 2: Interaction Features**
```python
# Fiber optic + No Security = yüksek risk
df['fiber_no_security'] = (
    (df['InternetService'] == 'Fiber optic') & 
    (df['OnlineSecurity'] == 'No')
).astype(int)
```

---

#### **7. Kategorik Encoding Stratejisi**

| Değişken Tipi | Encoding Yöntemi |
|---------------|------------------|
| Binary (Yes/No) | Label Encoding (0/1) |
| Contract | Ordinal Encoding (0,1,2) |
| Diğer kategorikler | One-Hot Encoding |
| InternetService | One-Hot Encoding |

---

### ⚪ 5.4. Düşük Öncelikli Öneriler

#### **8. Feature Selection**

**Sorun:** gender ve PhoneService churn ile anlamlı ilişkiye sahip değil (p>0.05).

**Öneri:** Model simplicity için bu değişkenler çıkarılabilir. Ancak tree-based modellerde tutulabilir (model kendisi önemsizse ignore eder).

---

## 6. Model Hazırlık Değerlendirmesi

### 📊 6.1. Hazırlık Skoru

| Kriter | Durum | Aksiyon Gerekli mi? |
|--------|-------|---------------------|
| Eksik Veri | ✅ Hazır | Hayır (minimal) |
| Encoding | ⚠️ Gerekli | Evet |
| Scaling | ⚠️ Gerekli | Evet |
| Outlier | ✅ Hazır | Hayır |
| Target Imbalance | ✅ Hazır | Hayır (stratified split yeterli) |
| Leakage Riski | ⚠️ Dikkat | Evet (TotalCharges çıkar) |
| Train-Test Split | ⚠️ Planlama | Evet (stratified) |
| Feature Selection | ⚠️ Opsiyonel | İsteğe bağlı |
| Multicollinearity | ⚠️ Dikkat | Evet (TotalCharges çıkar) |
| Veri Kalitesi | ✅ Çok İyi | Hayır |

**Hazırlık Skoru:** 4/10 ✅ Hazır, 6/10 ⚠️ Aksiyon Gerekli

---

### 🔴 6.2. Model Hazırlık Kararı: **HAZIR DEĞİL**

**Sebep:** Preprocessing gereksinimleri fazla. Data Prep Expert ile çalışmadan modelleme yapılmamalı.

**Ancak:**
- Veri kalitesi çok yüksek
- Güçlü prediktörler tespit edildi
- Preprocessing adımları net ve uygulanabilir

**Beklenen Hazırlık Süresi:** 1-2 gün (Data Prep Expert ile)

---

## 7. Sonuç ve Yol Haritası

### 🎯 7.1. Özet

| Metrik | Değer |
|--------|-------|
| Veri Seti Boyutu | 7,043 satır × 21 sütun |
| Veri Kalitesi | ✅ Çok Yüksek |
| Churn Oranı | %26.54 (kritik seviye) |
| En Güçlü Prediktörler | tenure, Contract, InternetService, MonthlyCharges, PaymentMethod |
| Model Hazırlık Durumu | 🔴 Hazır Değil (preprocessing gerekli) |
| Kritik Aksiyon | TotalCharges çıkar, encoding/scaling uygula |

---

### 🗺️ 7.2. Yol Haritası

#### **Adım 1: Data Prep Expert (1-2 gün)**

**Görevler:**
1. TotalCharges değişkenini modelden çıkar
2. customerID değişkenini modelden çıkar
3. Kategorik değişkenlere encoding uygula:
   - Contract: Ordinal (0,1,2)
   - Binary değişkenler: Label (0,1)
   - Diğerleri: One-Hot
4. Sayısal değişkenlere scaling uygula (StandardScaler)
5. Feature engineering:
   - tenure_group
   - fiber_no_security interaction
6. Stratified 80-20 train-test split

**Beklenen Çıktı:** X_train, X_test, y_train, y_test (model-ready format)

---

#### **Adım 2: Model Expert (3-5 gün)**

**Görevler:**
1. Baseline model: Logistic Regression
2. En az 12 model karşılaştırma:
   - Logistic Regression
   - Decision Tree
   - Random Forest
   - Gradient Boosting
   - XGBoost
   - LightGBM
   - CatBoost
   - SVM
   - KNN
   - Naive Bayes
   - Neural Network
   - Ensemble (Voting/Stacking)
3. Hyperparameter tuning (GridSearchCV / RandomizedSearchCV)
4. Cross-validation (5-fold)
5. Model evaluation:
   - Confusion Matrix
   - ROC-AUC
   - Precision/Recall/F1
   - Feature Importance

**Beklenen Çıktı:** Final model (pickle), performance report, feature importance

---

#### **Adım 3: Deployment Expert (2-3 gün)**

**Görevler:**
1. Model deployment (Streamlit app)
2. Real-time prediction interface
3. Churn risk dashboard
4. Actionable insights (müşteri bazlı öneri)
5. HCI ilkeleri ile kullanıcı dostu UI

**Beklenen Çıktı:** Production-ready churn prediction app

---

### 📈 7.3. Beklenen İş Etkileri

Eğer bu analizden çıkan öneriler uygulanırsa:

| Aksiyon | Beklenen Etki |
|---------|---------------|
| İlk 18 ay retention programı | Churn %2-3 puan azalma |
| Fiber optic hizmet iyileştirme | Churn %2-3 puan azalma |
| Uzun vadeli sözleşme teşvikleri | Churn %5-7 puan azalma |
| Otomatik ödeme geçiş kampanyası | Churn %1-2 puan azalma |
| Value-added services cross-sell | Churn %2-3 puan azalma |
| **Toplam Beklenen Etki** | **Churn %12-18 puan azalma** |

**Finansal Etki Tahmini:**
- Mevcut churn: %26.54
- Hedef churn: %10-15
- Korunan müşteri sayısı: ~840-1,260 müşteri/yıl
- Müşteri LTV: Ortalama $2,000 (tahmin)
- **Yıllık gelir korunması: $1.7M - $2.5M**

---

### 🎉 7.4. Final Mesaj

Bu veri seti **yüksek kalite** ve **güçlü prediktif sinyallere** sahip. Minimal preprocessing ile çok başarılı churn prediction modelleri geliştirilebilir.

**En kritik bulgular:**
1. **İlk 18 ay kritik risk dönemi** - retention stratejileri buraya odaklanmalı
2. **Contract tipi en güçlü prediktör** - uzun vadeli sözleşme teşvikleri priorite
3. **Fiber optic müşteri memnuniyetsizliği** - hizmet kalitesi araştırması acil
4. **TotalCharges leakage riski** - modelden kesinlikle çıkarılmalı

**Bir sonraki adım:** Data Prep Expert ile preprocessing pipeline kurulumu.

---

## 📁 Ek Dosyalar

Tüm analiz çıktıları şu klasörlerde saklanmıştır:

- **Görseller:** `figures/` (50+ HTML + PNG grafik)
- **CSV Raporları:** `reports/csv/` (15+ detaylı özet raporu)
- **Scriptler:** `scripts/` (7 phase scripti)

---

**Rapor Sonu**

*Bu rapor EDA Expert tarafından 7 aşamalı agentik EDA süreci ile hazırlanmıştır.*
*Analiz Tarihi: 5 Mayıs 2026*
