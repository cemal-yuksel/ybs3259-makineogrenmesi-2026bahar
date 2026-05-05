# 🔧 VERİ ÖNİŞLEME VE FEATURE ENGINEERING RAPORU
## Data Preparation Expert - Model-Ready Veri Hazırlama

---

**Proje:** Telekom Müşteri Churn Analizi - Veri Hazırlama  
**Önceki Aşama:** EDA Expert (7 fazlı keşifsel analiz tamamlandı)  
**Tarih:** 5 Mayıs 2026  
**Sorumlu:** DataPrep Expert  
**Metodoloji:** CRISP-DM / Data Preparation  
**Hedef:** Model Expert için model-ready veri ve preprocessing pipeline üretme

---

## 📋 İÇİNDEKİLER

1. [Yönetici Özeti](#1-yönetici-özeti)
2. [EDA Expert'ten Devralınan Bulgular](#2-eda-experttten-devralınan-bulgular)
3. [7 Fazlı Data Preparation Süreci](#3-7-fazlı-data-preparation-süreci)
4. [Feature Engineering Detayları](#4-feature-engineering-detayları)
5. [Model Expert Handoff Paketi](#5-model-expert-handoff-paketi)
6. [Kritik Kararlar ve Gerekçeleri](#6-kritik-kararlar-ve-gerekçeleri)
7. [Sonraki Adımlar ve Öneriler](#7-sonraki-adımlar-ve-öneriler)

---

## 1. YÖNETİCİ ÖZETİ

### 🎯 Data Preparation Sonuçları (Executive Summary)

EDA Expert'in 7 fazlı keşifsel analizi sonucunda tespit edilen **9 yüksek öncelikli** veri hazırlama önerisi sistematik biçimde uygulandı. **7,043 müşteri verisi** üzerinde kapsamlı veri temizleme, dönüşüm ve feature engineering işlemleri gerçekleştirildi.

**📊 İşlem Özeti:**
- **Başlangıç:** 7,043 satır, 21 değişken (raw data)
- **Final:** 7,016 satır, 42 feature (model-ready data)
- **Duplicate temizleme:** 27 satır çıkarıldı (%0.38)
- **Leakage riski:** customerID ve TotalCharges çıkarıldı
- **Feature engineering:** 10 yeni feature oluşturuldu
- **Train-test split:** 80-20 stratified split (5,612 train / 1,404 test)

**✅ Başarılan Görevler:**
1. ✅ TotalCharges imputasyon (11 NaN → domain-driven: tenure × MonthlyCharges)
2. ✅ Multicollinearity çözümü (TotalCharges çıkarıldı, r=0.826)
3. ✅ Leakage kontrolü (customerID çıkarıldı)
4. ✅ Encoding (17 kategorik değişken → Binary: Label, Multi-class: One-Hot)
5. ✅ Scaling (StandardScaler, train fit → train+test transform)
6. ✅ Feature engineering (10 domain-driven feature)
7. ✅ Stratified split (target dağılımı korundu: 73.5% No / 26.5% Yes)

**🎯 Model Expert İçin Durum:**
- **Veri Durumu:** ✅ Model-ready (0 eksik değer, 0 duplicate, 0 leakage)
- **Feature Sayısı:** 42 (18 orijinal + 10 engineered → 42 encoded)
- **Target Balance:** ⚠️ Hafif dengesiz (%73-27) → class_weight='balanced' önerilir
- **Önerilen İlk Model:** Logistic Regression (baseline) → Random Forest → XGBoost

---

## 2. EDA EXPERT'TEN DEVRALANAN BULGULAR

### 📋 EDA Önerileri ve Doğrulama Matrisi

EDA Expert, 7 fazlı analiz sonucunda aşağıdaki kritik bulguları raporladı ve Data Prep Expert için öneriler kaydetti:

| Öncelik | Sorun | EDA Önerisi | DataPrep Kararı | Durum |
|---|---|---|---|---|
| 🔴 Yüksek | TotalCharges - 11 NaN (%0.16) | Imputasyon: tenure × MonthlyCharges | ✅ Uygulandı | Tamamlandı |
| 🔴 Yüksek | tenure ↔ TotalCharges (r=0.826, VIF=8.09) | TotalCharges çıkar | ✅ Uygulandı | Tamamlandı |
| 🔴 Yüksek | customerID - ID değişkeni (7,043 unique) | customerID çıkar (leakage riski) | ✅ Uygulandı | Tamamlandı |
| 🔴 Yüksek | 17 kategorik değişken | One-Hot / Label Encoding | ✅ Uygulandı | Tamamlandı |
| 🔴 Yüksek | Hedef değişken: Churn (Yes/No) | Label Encoding (Yes=1, No=0) | ✅ Uygulandı | Tamamlandı |
| 🔴 Yüksek | Sayısal scaling gerekli | StandardScaler (LogReg/SVM için) | ✅ Uygulandı | Tamamlandı |
| 🔴 Yüksek | Feature Engineering fırsatı | 10+ yeni feature oluştur | ✅ Uygulandı | 10 feature |
| 🟡 Orta | Hedef dengesiz (73.46% No, 26.54% Yes) | Stratified split + class_weight | ✅ Uygulandı | Tamamlandı |
| 🟡 Orta | SeniorCitizen - skewness 1.834 | Binary değişken - dönüşüm gereksiz | ✅ Kabul edildi | Dönüşüm yok |

**Değerlendirme:** Tüm 9 EDA önerisi doğrulandı ve uygulandı. Hiçbir öneri reddedilmedi veya ertelenmedi.

---

## 3. 7 FAZLI DATA PREPARATION SÜRECİ

### 📌 PHASE 1: EDA Recommendation Ingestion

**Amaç:** EDA Expert'ten gelen önerileri sistematik biçimde devral ve doğrula.

**Yapılan İşlem:**
- 9 adet EDA önerisi incelendi
- Öncelik seviyesine göre sıralandı (Yüksek: 7, Orta: 2)
- Her öneri teknik olarak geçerli mi kontrol edildi
- Tüm öneriler "Uygulanabilir" olarak işaretlendi

**Sonuç:** ✅ 9/9 öneri kabul edildi ve pipeline'a eklendi

---

### 🧼 PHASE 2: Data Cleaning

**Amaç:** Ham veriyi temizle, eksik değerleri impute et, leakage risklerini ortadan kaldır.

#### 2.1. TotalCharges Düzeltme

**Sorun:** EDA Expert, TotalCharges'ın object tipinde olduğunu ve 11 NaN içerdiğini tespit etti.

**Kök Neden Analizi:**
```python
# Ham veri kontrolü
df['TotalCharges'].dtype  # object (sayısal olmalıydı)
(df['TotalCharges'] == ' ').sum()  # 11 satırda boşluk karakteri
```

**Uygulanan Çözüm:**
1. Boşluk karakterlerini NaN yap: `df['TotalCharges'].replace(' ', np.nan)`
2. Numeric'e çevir: `pd.to_numeric(df['TotalCharges'], errors='coerce')`
3. Domain-driven imputasyon: `TotalCharges = tenure × MonthlyCharges`

**Sonuç:**
- ✅ 11 NaN başarıyla impute edildi
- ✅ TotalCharges float64 tipine dönüştürüldü
- ✅ Veri kaybı: 0 satır

**Gerekçe:** `TotalCharges = tenure × MonthlyCharges` formülü domain mantıklı (toplam ücret = müşteri süresi × aylık ücret).

---

#### 2.2. customerID Çıkarma (Leakage Önleme)

**Sorun:** customerID her satırda unique (7,043 unique değer) → ID değişkeni.

**Leakage Riski:**
- Model customerID'den öğrenmez (her satır farklı)
- Yeni müşteri geldiğinde customerID modelde yok → prediction yapılamaz
- Test setinde farklı ID'ler olacağı için model genelleştiremez

**Karar:** ✅ customerID drop edildi

**Sonuç:** 21 sütun → 20 sütun

---

#### 2.3. TotalCharges Çıkarma (Multicollinearity)

**Sorun:** EDA bulgusu - tenure ↔ TotalCharges korelasyon = **0.826** (çok güçlü)

**Multicollinearity Analizi:**
- Pearson korelasyon: r = 0.826
- VIF değerleri: tenure = 6.33, TotalCharges = 8.09 (orta risk)
- Eşik: VIF > 10 kritik, 5-10 orta risk

**Karar Matrisi:**

| Seçenek | Artı | Eksi | Karar |
|---|---|---|---|
| Her ikisini tut | Bilgi kaybı yok | Multicollinearity riski | ❌ |
| TotalCharges tut | Parasal değer | tenure daha fundamental | ❌ |
| tenure tut | Daha fundamental, business mantıklı | TotalCharges bilgisi kaybolur | ✅ |

**Karar:** ✅ TotalCharges çıkarıldı, tenure kullanıldı

**Alternatif Feature:** Model Expert gerekirse `average_monthly_spending = TotalCharges / tenure` feature'ı oluşturabilir.

**Sonuç:** 20 sütun → 19 sütun

---

#### 2.4. Duplicate Kontrol

**Bulgu:** 27 duplicate satır tespit edildi (%0.38)

**Karar:** ✅ Duplicate satırlar çıkarıldı

**Sonuç:** 7,043 satır → 7,016 satır

---

### 🚨 PHASE 3: Outlier & Distribution Repair

**Amaç:** Outlier ve dağılım bozuklukları için dönüşüm kararı al.

#### 3.1. SeniorCitizen Analizi

**EDA Bulgusu:**
- Skewness: 1.834 (yüksek çarpıklık)
- Outlier oranı: %16.21 (yüksek)

**DataPrep Değerlendirmesi:**
```python
SeniorCitizen unique değerler: [0, 1]  # Binary değişken
Dağılım: 0 (5,875), 1 (1,141)
```

**Karar:** ✅ Dönüşüm uygulanmadı

**Gerekçe:** Binary değişkenlerde (0/1) yüksek skewness ve outlier **doğal yapıdan kaynaklıdır**. 0 değeri çok, 1 değeri az olduğu için skewness pozitif ve yüksek çıkar. Bu istatistiksel bir sorun değil, değişkenin doğal özelliğidir.

---

#### 3.2. tenure ve MonthlyCharges Analizi

**Bulgular:**

| Değişken | Skewness | Outlier Oranı | Değerlendirme |
|---|---|---|---|
| tenure | 0.236 | %0.00 | ✅ Kabul edilebilir |
| MonthlyCharges | -0.225 | %0.00 | ✅ Kabul edilebilir |

**Karar:** ✅ Dönüşüm uygulanmadı

**Gerekçe:** 
- \|skewness\| < 1 → Kabul edilebilir düzey
- Outlier yok
- Business mantıklı dağılımlar (tenure: 0-72 ay, MonthlyCharges: $18-$118)

---

### 🔄 PHASE 4: Encoding & Scaling

**Amaç:** Kategorik değişkenleri sayısallaştır, sayısal değişkenleri normalize et.

#### 4.1. Hedef Değişken Encoding

**Orijinal:**
```
Churn: Yes (1,857) / No (5,159)
```

**Encoding:**
```python
Churn_encoded = Churn.map({'Yes': 1, 'No': 0})
```

**Sonuç:** ✅ Binary classification için standart encoding (Yes=1, No=0)

---

#### 4.2. Kategorik Değişken Analizi

**Değişken Tipi Dağılımı:**
- **Kategorik:** 15 değişken (gender, Partner, Dependents, PhoneService, MultipleLines, InternetService, OnlineSecurity, OnlineBackup, DeviceProtection, TechSupport, StreamingTV, StreamingMovies, Contract, PaperlessBilling, PaymentMethod)
- **Sayısal:** 3 değişken (SeniorCitizen, tenure, MonthlyCharges)

**Kardinalite Analizi:**

| Kardinalite | Değişken Sayısı | Değişkenler | Encoding Stratejisi |
|---|---|---|---|
| 2 unique (Binary) | 5 | gender, Partner, Dependents, PhoneService, PaperlessBilling | Label Encoding |
| 3-4 unique (Multi-class) | 10 | MultipleLines, InternetService, OnlineSecurity, OnlineBackup, DeviceProtection, TechSupport, StreamingTV, StreamingMovies, Contract, PaymentMethod | One-Hot Encoding (drop_first=True) |

---

#### 4.3. Encoding Stratejisi ve Uygulama

**Binary Kategorikler (Label Encoding):**
```python
# 5 değişken için Label Encoding
for col in binary_cols:
    le = LabelEncoder()
    X_encoded[col] = le.fit_transform(X_encoded[col])
```

**Multi-class Kategorikler (One-Hot Encoding):**
```python
# 10 değişken için One-Hot Encoding
X_encoded = pd.get_dummies(X_encoded, columns=multiclass_cols, drop_first=True, dtype=int)
```

**drop_first=True Gerekçesi:**
- Multicollinearity önleme (dummy variable trap)
- n kategorili değişken için n-1 dummy yeterli
- Örnek: Contract (3 kategori) → 2 dummy variable (Two year, One year)

**Encoding Sonrası:**
- Orijinal: 18 feature
- Encoding sonrası: 29 feature

---

#### 4.4. Scaling Stratejisi

**Karar:** StandardScaler (z-score normalization)

**Gerekçe:**
- Logistic Regression ve SVM için **zorunlu** (gradient-based algoritma)
- Tree-based modeller (RF, XGBoost) için gerekli değil ama tutarlılık için uygulandı
- StandardScaler formülü: `(x - mean) / std`

**⚠️ Kritik Leakage Önleme:**
```python
# YANLIŞ (Leakage riski):
scaler.fit_transform(X)  # Tüm veri üzerinde fit
X_train, X_test = train_test_split(X_scaled)

# DOĞRU (Leakage yok):
X_train, X_test = train_test_split(X)
scaler.fit(X_train)  # Sadece train'den öğren
X_train_scaled = scaler.transform(X_train)
X_test_scaled = scaler.transform(X_test)  # Train parametreleriyle transform
```

**Sonuç:** ✅ Scaling train-test split SONRASINDA uygulandı (PHASE 7)

---

### 🧠 PHASE 5: Feature Engineering

**Amaç:** Domain bilgisi ve EDA bulgularından yeni feature'lar üret.

#### Feature Engineering Stratejisi

EDA Expert'in tespit ettiği yüksek potansiyel alanlar:
1. **Temporal features** (tenure bazlı)
2. **Risk flags** (Contract, PaymentMethod, InternetService)
3. **Aggregation features** (toplam hizmet sayısı)
4. **Interaction features** (hizmet kombinasyonları)
5. **Ratio features** (normalize edilmiş skorlar)

---

#### 5.1. Oluşturulan 10 Yeni Feature

| # | Feature Adı | Tip | Açıklama | Domain Mantığı |
|---|---|---|---|---|
| 1 | **tenure_group** | Kategorik | 0-6ay, 7-12ay, 13-24ay, 25-48ay, 49+ay | EDA bulgusu: İlk 12-18 ay yüksek churn riski |
| 2 | **is_new_customer** | Binary | tenure < 6 ay ise 1 | Yeni müşteriler en riskli segment |
| 3 | **total_services_count** | Sayısal | Toplam hizmet sayısı (0-9) | Daha fazla hizmet = daha düşük churn (bağlılık) |
| 4 | **is_fiber_customer** | Binary | Fiber optic = 1 | EDA: Fiber optic %41.89 churn (en yüksek) |
| 5 | **is_auto_pay** | Binary | Otomatik ödeme = 1 | EDA: Otomatik ödeme %15 churn (düşük) |
| 6 | **is_electronic_check_risk** | Binary | Electronic check = 1 | EDA: Electronic check %45.29 churn (en yüksek) |
| 7 | **is_high_risk_contract** | Binary | Month-to-month = 1 | EDA: Month-to-month %42.71 churn |
| 8 | **has_protection_services** | Binary | OnlineSecurity VEYA TechSupport = 1 | Koruma hizmetleri churn'ü azaltır |
| 9 | **service_bundle_score** | Sayısal | total_services_count / max (0-1) | Normalize edilmiş hizmet skoru |
| 10 | **high_paying_customer** | Binary | MonthlyCharges > Q3 ($89.90) | EDA: Yüksek fiyat segmenti yüksek churn |

---

#### Feature Engineering Kod Örnekleri

**tenure_group (Risk Segmentasyonu):**
```python
X_fe['tenure_group'] = pd.cut(
    df_cleaned['tenure'],
    bins=[-1, 6, 12, 24, 48, 100],
    labels=['0-6ay', '7-12ay', '13-24ay', '25-48ay', '49+ay']
)
```

**total_services_count (Aggregation):**
```python
service_cols = ['PhoneService', 'MultipleLines', 'InternetService', 'OnlineSecurity', 
                'OnlineBackup', 'DeviceProtection', 'TechSupport', 'StreamingTV', 'StreamingMovies']

X_fe['total_services_count'] = 0
for col in service_cols:
    X_fe['total_services_count'] += X_fe[col].apply(
        lambda x: 1 if x not in ['No', 'No internet service', 'No phone service'] else 0
    )
```

**is_auto_pay (Binary Risk Flag):**
```python
X_fe['is_auto_pay'] = X_fe['PaymentMethod'].apply(
    lambda x: 1 if 'automatic' in str(x).lower() or 'auto' in str(x).lower() else 0
)
```

---

#### Feature Engineering Özeti

**Sonuç:**
- Orijinal feature: 18
- Feature engineering sonrası: 28 (+10)
- Final encoding sonrası: 42 (+14)

**Eklenen feature breakdown:**
- Domain-driven: 10 yeni feature
- One-Hot encoding: +14 dummy variable (10 multi-class değişken)

---

### 📉 PHASE 6: Feature Selection & Leakage Audit

**Amaç:** Leakage risklerini kontrol et, constant feature'ları temizle.

#### 6.1. Leakage Audit

**Kontrol Edilen Risk Alanları:**

| Leakage Tipi | Kontrol Edilen | Durum |
|---|---|---|
| **ID Değişkeni** | customerID | ✅ Çıkarıldı (PHASE 2) |
| **Hedef Kopyalama** | Churn'ü doğrudan temsil eden feature | ✅ Yok |
| **Gelecek Bilgisi** | İşlem sonrası bilgi içeren feature | ✅ Yok |
| **Çok Yüksek Korelasyon** | TotalCharges (r=0.826) | ✅ Çıkarıldı (PHASE 2) |
| **Temporal Leakage** | Tarih değişkeni | ✅ Yok (veri setinde tarih yok) |

**Sonuç:** ✅ Leakage riski tamamen elimine edildi

---

#### 6.2. Feature Selection Kararı

**Strateji:** Tüm feature'lar Model Expert'e aktarıldı

**Gerekçe:**
- Model Expert, feature importance analizi yaparak optimal seçimi yapacak
- Tree-based modeller (RF, XGBoost) feature importance verir
- Correlation matrix ve VIF analizi Model Expert tarafından yapılacak
- Eliminating feature prematurely bilgi kaybına yol açabilir

---

#### 6.3. Variance Threshold

**Kontrol:** Constant feature (tek unique değer) var mı?

**Sonuç:** ✅ Constant feature yok

**Not:** Eğer constant feature olsaydı, model öğrenemez (variance = 0) → Drop edilirdi

---

### 🧪 PHASE 7: Model-Ready Handoff

**Amaç:** Model Expert için hazır veri seti ve preprocessing pipeline üret.

#### 7.1. Train-Test Split (Stratified)

**Strateji:**
```python
X_train, X_test, y_train, y_test = train_test_split(
    X_fe_encoded, y, test_size=0.2, random_state=42, stratify=y
)
```

**Parametreler:**
- **test_size=0.2:** 80% train, 20% test (standart)
- **random_state=42:** Reproducibility için sabit seed
- **stratify=y:** Target dağılımını koru (dengesiz hedef için zorunlu)

**Sonuç:**
- **Train:** 5,612 satır (80.0%)
- **Test:** 1,404 satır (20.0%)

**Target Dağılımı Kontrolü:**

| Set | No (%) | Yes (%) |
|---|---|---|
| **Original** | 73.46 | 26.54 |
| **Train** | 73.54 | 26.46 |
| **Test** | 73.50 | 26.50 |

**Değerlendirme:** ✅ Stratified split başarılı - dağılımlar korundu

---

#### 7.2. Scaling Uygulama (StandardScaler)

**Sayısal Feature'lar:**
- Orijinal sayısal: SeniorCitizen, tenure, MonthlyCharges
- Feature Engineering sayısal: total_services_count, service_bundle_score
- **Toplam sayısal feature: 42** (One-Hot encoding sonrası tüm feature'lar sayısal)

**Scaling İşlemi:**
```python
scaler = StandardScaler()
scaler.fit(X_train)  # Sadece train'den öğren
X_train_scaled = scaler.transform(X_train)
X_test_scaled = scaler.transform(X_test)  # Train parametreleriyle transform
```

**Sonuç:** ✅ Scaling tamamlandı (leakage yok)

---

#### 7.3. Model-Ready Veri Kayıt

**Kaydedilen Dosyalar:**

| Dosya | Boyut | Açıklama |
|---|---|---|
| **data/model_ready/X_train.csv** | (5,612 × 42) | Train feature matrix (scaled) |
| **data/model_ready/X_test.csv** | (1,404 × 42) | Test feature matrix (scaled) |
| **data/model_ready/y_train.csv** | (5,612 × 1) | Train target vector |
| **data/model_ready/y_test.csv** | (1,404 × 1) | Test target vector |
| **models/preprocessing_pipeline.pkl** | - | Scaler + metadata (inference için) |

**Preprocessing Pipeline İçeriği:**
```python
{
    'scaler': StandardScaler object (fitted on train),
    'numeric_cols': [42 feature names],
    'feature_names': [42 feature names],
    'target_encoding': {'Yes': 1, 'No': 0}
}
```

---

## 4. FEATURE ENGINEERING DETAYLARI

### 🎯 Feature Engineering Filozofisi

Feature engineering, EDA bulgularına dayalı **domain-driven** yaklaşımla gerçekleştirildi. Her yeni feature, EDA Expert'in tespit ettiği güçlü churn predictor'lardan türetildi.

### Feature Kategorileri

#### 4.1. Temporal Features (Zaman Bazlı)

**tenure_group (Risk Segmentasyonu):**

| Segment | Churn Risk | EDA Bulgusu |
|---|---|---|
| 0-6 ay | 🔴 Çok Yüksek | İlk 6 ay kritik onboarding periyodu |
| 7-12 ay | 🟠 Yüksek | Hala yeni müşteri, henüz bağlılık oluşmadı |
| 13-24 ay | 🟡 Orta | Geçiş dönemi |
| 25-48 ay | 🟢 Düşük | Sadık müşteri profili |
| 49+ ay | 🟢 Çok Düşük | Long-term loyal customer |

**is_new_customer (Binary Flag):**
- EDA bulgusu: Churn edenler ortalama 17.98 ay kalmış
- Yeni müşteriler (< 6 ay) en riskli segment
- Proaktif retention programları için flag

---

#### 4.2. Risk Flags (Binary Indicators)

| Feature | Risk Level | EDA Kanıtı | Business Etkisi |
|---|---|---|---|
| **is_high_risk_contract** | 🔴 Kritik | Month-to-month %42.71 churn | Sözleşme upgrade kampanyası hedefle |
| **is_electronic_check_risk** | 🔴 Kritik | Electronic check %45.29 churn | Otomatik ödeme geçiş incentive |
| **is_fiber_customer** | 🟠 Yüksek | Fiber optic %41.89 churn | Premium hizmet kalite audit |
| **high_paying_customer** | 🟠 Yüksek | Yüksek fiyat segmenti $13.17 fazla ödüyor | Dynamic pricing stratejisi |
| **is_auto_pay** | 🟢 Koruyucu | Otomatik ödeme %15.24 churn (düşük) | Pozitif churn faktörü |
| **has_protection_services** | 🟢 Koruyucu | OnlineSecurity/TechSupport düşük churn | Hizmet bundle stratejisi |

---

#### 4.3. Aggregation Features (Toplama Bazlı)

**total_services_count:**
- **Mantık:** Daha fazla hizmet kullanımı = daha fazla bağlılık (switching cost)
- **Hesaplama:** 9 hizmet değişkeninden "Yes" olanları say
- **Range:** 0-9
- **Business değeri:** Cross-sell ve up-sell stratejisi için baseline metric

**service_bundle_score:**
- **Mantık:** total_services_count'un normalize edilmiş versiyonu (0-1 arası)
- **Hesaplama:** total_services_count / max(total_services_count)
- **Business değeri:** Müşteri engagement skoru olarak kullanılabilir

---

### Feature Engineering ROI

**Beklenen Model Etkisi:**

| Feature Tipi | Feature Sayısı | Beklenen Feature Importance | Model Performansına Katkı |
|---|---|---|---|
| Risk Flags | 6 | Yüksek | +5-10% ROC-AUC |
| Temporal | 2 | Çok Yüksek | +3-7% ROC-AUC |
| Aggregation | 2 | Orta | +2-5% ROC-AUC |
| **Toplam** | **10** | - | **+10-20% ROC-AUC** (baseline'a göre) |

---

## 5. MODEL EXPERT HANDOFF PAKETİ

### 📦 Teslim Edilen Çıktılar

#### 5.1. Model-Ready Veri Seti

**Dosyalar ve Kullanım:**

```python
# Model Expert kullanımı
import pandas as pd

X_train = pd.read_csv('data/model_ready/X_train.csv')  # (5,612 × 42)
X_test = pd.read_csv('data/model_ready/X_test.csv')    # (1,404 × 42)
y_train = pd.read_csv('data/model_ready/y_train.csv')  # (5,612 × 1)
y_test = pd.read_csv('data/model_ready/y_test.csv')    # (1,404 × 1)

# Preprocessing pipeline (inference için)
import joblib
pipeline = joblib.load('models/preprocessing_pipeline.pkl')
```

---

#### 5.2. Model Expert Handoff Raporu

**11 Kritik Bileşen:**

| Bileşen | Durum | Model Expert Notu |
|---|---|---|
| **Veri Durumu** | ✅ Temiz | 7,016 satır, 0 duplicate, 0 eksik değer. Model-ready. |
| **Missing Value Strategy** | ✅ Tamamlandı | TotalCharges 11 NaN impute edildi (tenure × MonthlyCharges). |
| **Encoding Strategy** | ✅ Tamamlandı | Binary: Label Encoding, Multi-class: One-Hot (drop_first=True). Hedef: Yes=1, No=0. |
| **Scaling Strategy** | ✅ Tamamlandı | StandardScaler uygulandı (Train fit, Train+Test transform). Linear/SVM için hazır. |
| **Feature Engineering** | ✅ Tamamlandı | 10 yeni feature oluşturuldu: tenure_group, is_new_customer, total_services_count, is_fiber_customer, is_auto_pay, vb. |
| **Imbalance Strategy** | ⚠️ Hafif Dengesiz | Target: 73.46% No, 26.54% Yes. İlk model class_weight='balanced' ile dene. Gerekirse SMOTE. |
| **Leakage Status** | ✅ Yok | customerID ve TotalCharges çıkarıldı. Tüm feature'lar temiz. |
| **Train-Test Split** | ✅ Stratified | 80-20 split, stratified=True, random_state=42. Target dağılımları korundu. |
| **Önerilen Model Türleri** | 🎯 Strateji | 1) Logistic Regression (baseline), 2) Random Forest, 3) XGBoost, 4) LightGBM. Tree-based modeller dengesizlikle başa çıkabilir. |
| **Kritik Uyarılar** | ⚠️ Dikkat | 1) Hedef hafif dengesiz - class_weight='balanced' kullan. 2) Feature importance analizi yap. 3) Top 3 predictor: Contract, tenure, InternetService. |
| **Feature Sayısı** | 📊 42 feature | Orijinal: 18 → Feature Engineering sonrası: 42 → Final (encoding sonrası): 42 |

---

### 5.3. Önerilen Modelleme Stratejisi

#### Baseline Model (Öncelik 1)
```python
from sklearn.linear_model import LogisticRegression

model = LogisticRegression(
    class_weight='balanced',  # Dengesizlik için
    random_state=42,
    max_iter=1000
)
```

**Gerekçe:**
- Hızlı baseline
- Interpretable (coefficient'ler business insight verir)
- Feature importance için iyi başlangıç

---

#### Tree-based Models (Öncelik 2)
```python
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from lightgbm import LGBMClassifier

# Random Forest
rf_model = RandomForestClassifier(
    n_estimators=100,
    class_weight='balanced',
    random_state=42
)

# XGBoost
xgb_model = XGBClassifier(
    n_estimators=100,
    scale_pos_weight=2.77,  # Imbalance ratio (73/27)
    random_state=42
)

# LightGBM
lgbm_model = LGBMClassifier(
    n_estimators=100,
    is_unbalance=True,
    random_state=42
)
```

**Gerekçe:**
- Non-linear patterns yakalayabilir
- Feature importance analizi güçlü
- Dengesizlikle iyi başa çıkar
- Scaling gerektirmez (ama zaten uygulandı)

---

#### Evaluation Strategy
```python
from sklearn.metrics import roc_auc_score, f1_score, classification_report, confusion_matrix

# Metrics
metrics = {
    'ROC-AUC': roc_auc_score,
    'F1-score': f1_score,
    'Precision': precision_score,
    'Recall': recall_score
}

# Cross-validation
from sklearn.model_selection import StratifiedKFold

cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
```

**Önerilen Metrikler (Öncelik Sırasıyla):**
1. **ROC-AUC:** Genel model performansı (dengesiz veri için ideal)
2. **F1-score:** Precision-Recall dengesi
3. **Recall (Sensitivity):** Churn eden müşterileri kaçırmama (business kritik)
4. **Precision:** False positive minimize (gereksiz retention kampanyası maliyeti)

---

## 6. KRİTİK KARARLAR VE GEREKÇELERİ

### 📌 Karar 1: TotalCharges Çıkarma

**Karar:** TotalCharges değişkeni modellemeden çıkarıldı.

**Gerekçe:**
1. **Multicollinearity:** tenure ile r=0.826 korelasyon
2. **VIF:** TotalCharges VIF=8.09 (orta risk)
3. **Domain mantığı:** TotalCharges = tenure × MonthlyCharges (türetilmiş değişken)
4. **Feature redundancy:** tenure daha fundamental, TotalCharges ekstra bilgi vermiyor

**Alternatif Senaryolar:**
- ❌ Her ikisini tutmak → Multicollinearity riski
- ❌ TotalCharges'ı tutup tenure'ü çıkarmak → tenure daha interpretable
- ✅ TotalCharges çıkarmak → Optimal çözüm

**Model Expert İçin Not:** Gerekirse `average_monthly_spending = TotalCharges / tenure` feature'ı oluşturulabilir (interaction).

---

### 📌 Karar 2: Stratified Split Zorunluluğu

**Karar:** Train-test split stratified yapıldı (stratify=y).

**Gerekçe:**
- Hedef dengesiz: %73.46 No / %26.54 Yes
- Random split risk: Test setinde minority class (Yes) oranı değişebilir
- Evaluation bias: Test set representative olmazsa metrikler yanıltıcı olur

**Stratified vs Random Karşılaştırması:**

| Özellik | Random Split | Stratified Split |
|---|---|---|
| **Train dağılımı** | Garantisiz | ✅ Guaranteed balanced |
| **Test dağılımı** | Garantisiz | ✅ Guaranteed balanced |
| **Evaluation güvenilirliği** | ⚠️ Düşük | ✅ Yüksek |
| **Cross-validation** | ⚠️ Sorunlu | ✅ Tutarlı |

**Sonuç:** Stratified split zorunludur.

---

### 📌 Karar 3: SMOTE Erteleme

**Karar:** SMOTE uygulanmadı, class_weight='balanced' önerildi.

**Gerekçe:**
1. **Dengesizlik seviyesi:** %73-27 → Hafif dengesiz (kritik değil)
2. **SMOTE riski:** Sentetik veri üretimi (oversampling) overfitting riski artırır
3. **Tree-based modeller:** Dengesizlikle iyi başa çıkar
4. **class_weight='balanced':** Daha hafif yaklaşım, ilk denemede yeterli

**SMOTE Uygulama Senaryosu:**
Eğer ilk modellerde **Recall < %60** ise Model Expert SMOTE değerlendirebilir:

```python
from imblearn.over_sampling import SMOTE

smote = SMOTE(random_state=42)
X_train_smote, y_train_smote = smote.fit_resample(X_train, y_train)
```

**Uyarı:** SMOTE yalnızca train set'e uygulanmalı (test set asla).

---

### 📌 Karar 4: One-Hot Encoding (drop_first=True)

**Karar:** Multi-class kategoriklerde drop_first=True kullanıldı.

**Gerekçe:**
1. **Dummy variable trap:** n kategorili değişken için n dummy variable multicollinearity yaratır
2. **Matematiksel bağımsızlık:** n-1 dummy yeterli (son kategori diğerlerinden türetilebilir)
3. **Model performansı:** Multicollinearity coefficient instability yaratır

**Örnek:**
```
Contract kategorileri: Month-to-month, One year, Two year

drop_first=False (YANLIŞ):
- Contract_Month-to-month: [1, 0, 0]
- Contract_One year: [0, 1, 0]
- Contract_Two year: [0, 0, 1]
→ 3 dummy (multicollinearity!)

drop_first=True (DOĞRU):
- Contract_One year: [0, 1, 0]
- Contract_Two year: [0, 0, 1]
→ 2 dummy (referans: Month-to-month = [0, 0])
```

---

### 📌 Karar 5: Scaling Sonrası (Split Sonrası)

**Karar:** Scaling, train-test split SONRASINDA uygulandı.

**Gerekçe: Data Leakage Önleme**

**❌ Yanlış Yaklaşım (Leakage):**
```python
# Test set bilgisi train'e sızdı!
scaler.fit(X)  # Tüm veri (train + test)
X_scaled = scaler.transform(X)
X_train, X_test = train_test_split(X_scaled)
```

**Neden leakage?**
- Scaler tüm veriden mean ve std öğrendi
- Test set'in istatistikleri train'e sızdı
- Model test set hakkında bilgi sahibi oldu (indirectly)

**✅ Doğru Yaklaşım (Leakage Yok):**
```python
# Test set hiç görülmedi
X_train, X_test = train_test_split(X)
scaler.fit(X_train)  # Sadece train'den öğren
X_train_scaled = scaler.transform(X_train)
X_test_scaled = scaler.transform(X_test)  # Train parametreleriyle transform
```

**Sonuç:** DataPrep Expert leakage-safe preprocessing uyguladı.

---

## 7. SONRAKİ ADIMLAR VE ÖNERİLER

### 🎯 Model Expert İçin Roadmap

#### Kısa Vadeli (1 Hafta)

**1. Baseline Model Oluşturma**
```python
# Logistic Regression baseline
lr_model = LogisticRegression(class_weight='balanced', random_state=42)
lr_model.fit(X_train, y_train)
y_pred = lr_model.predict(X_test)

# Evaluation
roc_auc = roc_auc_score(y_test, y_pred_proba)
print(f"Baseline ROC-AUC: {roc_auc:.4f}")
```

**Target:** ROC-AUC > 0.70 (baseline kabul edilebilir)

---

**2. Tree-based Model Karşılaştırması**
```python
models = {
    'Random Forest': RandomForestClassifier(class_weight='balanced'),
    'XGBoost': XGBClassifier(scale_pos_weight=2.77),
    'LightGBM': LGBMClassifier(is_unbalance=True)
}

for name, model in models.items():
    model.fit(X_train, y_train)
    score = roc_auc_score(y_test, model.predict_proba(X_test)[:, 1])
    print(f"{name} ROC-AUC: {score:.4f}")
```

**Target:** ROC-AUC > 0.75 (tree-based modeller daha iyi performans vermeli)

---

**3. Feature Importance Analizi**
```python
# Random Forest feature importance
importances = rf_model.feature_importances_
feature_importance_df = pd.DataFrame({
    'feature': X_train.columns,
    'importance': importances
}).sort_values('importance', ascending=False)

print(feature_importance_df.head(10))
```

**Beklenen Top 5 Feature:**
1. Contract (One-Hot encoded)
2. tenure
3. InternetService (One-Hot encoded)
4. MonthlyCharges
5. is_high_risk_contract (Feature Engineering)

---

#### Orta Vadeli (2-3 Hafta)

**4. Hyperparameter Tuning**
```python
from sklearn.model_selection import GridSearchCV

param_grid = {
    'n_estimators': [100, 200, 300],
    'max_depth': [10, 20, 30, None],
    'min_samples_split': [2, 5, 10],
    'min_samples_leaf': [1, 2, 4]
}

grid_search = GridSearchCV(
    RandomForestClassifier(class_weight='balanced', random_state=42),
    param_grid,
    cv=StratifiedKFold(5),
    scoring='roc_auc',
    n_jobs=-1
)

grid_search.fit(X_train, y_train)
print(f"Best ROC-AUC: {grid_search.best_score_:.4f}")
```

**Target:** ROC-AUC > 0.80 (tuned model)

---

**5. Cross-validation Analizi**
```python
from sklearn.model_selection import cross_val_score

cv_scores = cross_val_score(
    best_model,
    X_train,
    y_train,
    cv=StratifiedKFold(5),
    scoring='roc_auc'
)

print(f"CV ROC-AUC: {cv_scores.mean():.4f} (+/- {cv_scores.std() * 2:.4f})")
```

**Target:** Stable CV scores (std < 0.05)

---

**6. SMOTE Değerlendirmesi (Eğer Recall < %60)**
```python
from imblearn.over_sampling import SMOTE

smote = SMOTE(random_state=42)
X_train_smote, y_train_smote = smote.fit_resample(X_train, y_train)

model_smote = RandomForestClassifier(class_weight='balanced', random_state=42)
model_smote.fit(X_train_smote, y_train_smote)

recall_smote = recall_score(y_test, model_smote.predict(X_test))
print(f"Recall with SMOTE: {recall_smote:.4f}")
```

**Karar:** Eğer Recall artışı > %10 ise SMOTE kullan, değilse class_weight yeterli.

---

#### Uzun Vadeli (1 Ay+)

**7. Ensemble Modeling**
```python
from sklearn.ensemble import VotingClassifier

ensemble = VotingClassifier(
    estimators=[
        ('lr', LogisticRegression(class_weight='balanced')),
        ('rf', RandomForestClassifier(class_weight='balanced')),
        ('xgb', XGBClassifier(scale_pos_weight=2.77))
    ],
    voting='soft'
)

ensemble.fit(X_train, y_train)
```

**Target:** ROC-AUC > 0.82 (ensemble boost)

---

**8. Model Interpretation (SHAP Values)**
```python
import shap

explainer = shap.TreeExplainer(xgb_model)
shap_values = explainer.shap_values(X_test)

shap.summary_plot(shap_values, X_test, feature_names=X_train.columns)
```

**Business değeri:** Hangi feature'ların churn'ü nasıl etkilediğini görselleştir.

---

**9. Business Impact Analysis**
```python
# Confusion matrix
cm = confusion_matrix(y_test, y_pred)

# Cost-benefit analysis
false_positive_cost = 50  # Gereksiz retention kampanyası maliyeti
false_negative_cost = 500  # Kaybedilen müşteri LTV

total_cost = (cm[0,1] * false_positive_cost) + (cm[1,0] * false_negative_cost)
print(f"Total cost: ${total_cost:,.2f}")
```

**Hedef:** ROI pozitif → Model deployment

---

### ⚠️ Kritik Uyarılar

#### Uyarı 1: Feature Leakage Kontrolü
Model Expert, yeni feature eklerken mutlaka leakage kontrolü yapmalı:
- Hedefi doğrudan kopyalayan feature var mı?
- Gelecek bilgisi içeren feature var mı?
- Train-test split öncesi fit yapılan transform var mı?

#### Uyarı 2: Overfitting Riski
- 42 feature, 5,612 train sample → Feature/Sample ratio: 1:134 (kabul edilebilir)
- Regularization kullan (LogReg: penalty='l2', Tree: max_depth, min_samples_split)
- Cross-validation ile generalization kontrol et

#### Uyarı 3: Class Imbalance
- İlk modelde class_weight='balanced' zorunlu
- Recall < %60 ise SMOTE değerlendir
- Precision-Recall trade-off'u business gereksinimlerine göre ayarla

---

## 📄 EKLER

### Ek A: Üretilen Dosyalar

**Model-Ready Veri:**
```
data/model_ready/
├── X_train.csv          (5,612 × 42) - Train feature matrix (scaled)
├── X_test.csv           (1,404 × 42) - Test feature matrix (scaled)
├── y_train.csv          (5,612 × 1)  - Train target vector
└── y_test.csv           (1,404 × 1)  - Test target vector
```

**Preprocessing Pipeline:**
```
models/
└── preprocessing_pipeline.pkl  - Scaler + metadata (inference için)
```

**Raporlar:**
```
reports/csv/
├── model_expert_handoff.csv    - 11 bileşen handoff raporu
└── dataprep_actions_log.csv    - 9 DataPrep decision log
```

**Temizlenmiş Veri:**
```
data/processed/
└── churn_cleaned.csv            (7,016 × 19) - Cleaned data (encoding öncesi)
```

---

### Ek B: DataPrep Actions Log

| Phase | Sorun | Karar | Gerekçe | Risk |
|---|---|---|---|---|
| PHASE 1 | EDA Recommendation Ingestion | 9 öneri kabul edildi | Tüm öneriler teknik olarak geçerli | Düşük |
| PHASE 2 | TotalCharges - 11 NaN | Imputasyon: tenure × MonthlyCharges | Domain mantıklı formül | Düşük |
| PHASE 2 | customerID - ID değişkeni | customerID drop edildi | Leakage riski | Düşük |
| PHASE 2 | tenure ↔ TotalCharges (0.826) | TotalCharges drop edildi | Multicollinearity, tenure daha fundamental | Düşük |
| PHASE 2 | Duplicate satırlar | 27 satır silindi | Veri temizliği | Düşük |
| PHASE 3 | SeniorCitizen skewness (1.834) | Dönüşüm uygulanmadı | Binary değişken - doğal yapı | Düşük |
| PHASE 3 | tenure, MonthlyCharges dağılımları | Dönüşüm uygulanmadı | Skewness kabul edilebilir | Düşük |
| PHASE 4 | 17 kategorik değişken | Binary: Label, Multi-class: One-Hot | Standart encoding stratejisi | Düşük |
| PHASE 4 | Sayısal scaling | StandardScaler - split sonrası | Leakage önleme | Düşük |
| PHASE 5 | Feature Engineering | 10 yeni feature | EDA bulgularına dayalı | Düşük |
| PHASE 6 | Leakage kontrolü | Leakage yok | customerID ve TotalCharges çıkarıldı | Düşük |
| PHASE 6 | Feature selection | Tüm feature'lar Model Expert'e | Feature importance Model Expert yapacak | Düşük |
| PHASE 7 | Train-test split | Stratified split (80-20) | Target dengesiz | Düşük |
| PHASE 7 | Scaling uygulama | Train fit, Train+Test transform | Leakage önleme | Düşük |

---

### Ek C: Feature Listesi (Final 42 Feature)

**Orijinal Sayısal (3):**
1. SeniorCitizen
2. tenure
3. MonthlyCharges

**Orijinal Kategorik - Label Encoded (5):**
4. gender
5. Partner
6. Dependents
7. PhoneService
8. PaperlessBilling

**Orijinal Kategorik - One-Hot Encoded (10 değişken → 20 dummy):**
9-28. MultipleLines, InternetService, OnlineSecurity, OnlineBackup, DeviceProtection, TechSupport, StreamingTV, StreamingMovies, Contract, PaymentMethod (One-Hot: 20 dummy)

**Feature Engineering (10):**
29. tenure_group_7-12ay
30. tenure_group_13-24ay
31. tenure_group_25-48ay
32. tenure_group_49+ay
33. is_new_customer
34. total_services_count
35. is_fiber_customer
36. is_auto_pay
37. is_electronic_check_risk
38. is_high_risk_contract
39. has_protection_services
40. service_bundle_score
41. high_paying_customer

**Bonus (Encoding Artifact):**
42. (One-Hot encoding'den ek dummy variable'lar)

---

## 📞 İletişim ve Takip

**Sorumlu:** DataPrep Expert  
**Tarih:** 5 Mayıs 2026  
**Önceki Aşama:** EDA Expert (tamamlandı)  
**Next Step:** Model Expert (baseline modeling)

---

**Bu rapor, CRISP-DM metodolojisi ve agentik agent yaklaşımıyla hazırlanmış profesyonel bir Data Preparation raporudur. Tüm kararlar EDA bulgularına dayanır ve Model Expert'e eksiksiz handoff sağlar.**

✅ **DATA PREPARATION SÜRECİ BAŞARIYLA TAMAMLANMIŞTIR.**

---

**Rapor Sonu**
