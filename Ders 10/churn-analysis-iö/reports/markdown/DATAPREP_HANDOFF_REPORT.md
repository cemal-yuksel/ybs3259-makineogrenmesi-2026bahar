# DATA PREPARATION HANDOFF REPORT
**DataPrep Expert → Model Expert**  
**Tarih:** 05 May 2026, 15:25  
**Proje:** Churn Analysis  

---

## 1. YÖNETICI ÖZETI

EDA Expert'ten gelen kritik bulgular doğrultusunda 7 aşamalı agentik veri hazırlama süreci tamamlanmıştır.

**Model Readiness Durumu:** ✅ HAZIR

**Kritik Aksiyonlar:**
- TotalCharges çıkarıldı (Leakage + Multicollinearity riski)
- 15 kategorik değişkene encoding uygulandı
- 3 yeni feature oluşturuldu (tenure_group, MonthlyCharges_category, FiberOptic_NoSecurity)
- 80-20 Stratified Split uygulandı
- StandardScaler ile scaling yapıldı (leakage-safe)

---

## 2. VERİ HAZIRLAMA AŞAMALARI

### PHASE 1: EDA Recommendation Ingestion
| Öncelik   | Sorun                                     | EDA Önerisi                                         | DataPrep Kararı                                               | Gerekçe                                                                                                          |
|:----------|:------------------------------------------|:----------------------------------------------------|:--------------------------------------------------------------|:-----------------------------------------------------------------------------------------------------------------|
| Kritik    | TotalCharges Multicollinearity ve Leakage | TotalCharges değişkenini modelden çıkar             | UYGULA - TotalCharges çıkarılacak                             | Leakage riski + multicollinearity. TotalCharges = tenure × MonthlyCharges mantıksal ilişkisi model bias yaratır. |
| Kritik    | Encoding Gereksinimi                      | Contract ordinal, diğerleri one-hot                 | UYGULA - Ordinal + One-Hot + Label Encoding                   | Contract mantıksal sıralı (month-to-month < one year < two year). Binary değişkenler label encoding alacak.      |
| Yüksek    | Scaling Gereksinimi                       | StandardScaler veya MinMaxScaler                    | UYGULA - StandardScaler (linear modeller için)                | Farklı ölçekler gradient-based ve distance-based modelleri etkiler.                                              |
| Yüksek    | Missing Values                            | tenure × MonthlyCharges ile doldur veya çıkar       | REDDET - TotalCharges zaten çıkarılacak                       | TotalCharges multicollinearity nedeniyle silinecek, eksik veri sorunu otomatik çözülüyor.                        |
| Orta      | Feature Engineering                       | tenure_group (0-12: new, 13-24: medium, 25+: loyal) | UYGULA - tenure_group + MonthlyCharges_category oluşturulacak | Threshold-based segmentation non-linear pattern yakalama için faydalı.                                           |
| Orta      | Interaction Features                      | InternetService × OnlineSecurity interaction        | UYGULA - Interaction feature oluşturulacak                    | EDA'da fiber optic kullanıcılarının churn oranı %41.89 - interaction yakalanmalı.                                |
| Düşük     | Zayıf Değişkenler                         | Bu değişkenler çıkarılabilir                        | ERTELE - Model Expert feature selection yapacak               | Bu kararı model performans karşılaştırması sonrası vermek daha mantıklı.                                         |

### PHASE 2: Data Cleaning
- ✅ **TotalCharges çıkarıldı:** VIF 8.08, tenure korelasyonu 0.8259, leakage riski
- ✅ **customerID çıkarıldı:** Identifier değişken
- ✅ **Eksik veri:** TotalCharges çıkarılınca otomatik çözüldü
- ✅ **Duplicate:** Yok

### PHASE 3: Outlier & Distribution Repair
- ✅ **Karar:** Müdahale gerekmedi
- **Gerekçe:** EDA'da kritik outlier veya distribution sorunu tespit edilmedi

### PHASE 4: Encoding & Transformation
- ✅ **Binary değişkenler:** Label Encoding (gender, Partner, Dependents, PhoneService, PaperlessBilling)
- ✅ **Contract:** Ordinal Encoding (0: Month-to-month, 1: One year, 2: Two year)
- ✅ **Diğer kategorik:** One-Hot Encoding (drop_first=True)
- ✅ **Scaling:** StandardScaler (tenure, MonthlyCharges, SeniorCitizen)

### PHASE 5: Feature Engineering
- ✅ **tenure_group:** 0=new (0-12 ay), 1=medium (13-24 ay), 2=loyal (25+ ay)
- ✅ **MonthlyCharges_category:** 0=low, 1=medium, 2=high
- ✅ **FiberOptic_NoSecurity:** Interaction feature (Fiber optic × No Security)

### PHASE 6: Feature Selection & Leakage Audit
| Kontrol                           | Durum                      | Risk   |
|:----------------------------------|:---------------------------|:-------|
| TotalCharges çıkarıldı mı?        | ✅ Evet                    | Yok    |
| customerID çıkarıldı mı?          | ✅ Evet                    | Yok    |
| Target encoding split sonrası mı? | ✅ Uygulanmadı (gerek yok) | Yok    |
| SMOTE split sonrası mı?           | ✅ Uygulanmadı (gerek yok) | Yok    |

### PHASE 7: Train-Test Split
- ✅ **Split Stratejisi:** 80-20 Stratified (random_state=42)
- ✅ **Train:** 5612 satır × 30 feature
- ✅ **Test:** 1404 satır × 30 feature
- ✅ **Churn Balance (Train):** No=73.54%, Yes=26.46%
- ✅ **Churn Balance (Test):** No=73.50%, Yes=26.50%

---

## 3. MODEL EXPERT HANDOFF

| Bileşen                | Durum                         | Model Expert Notu                                                                                                              |
|:-----------------------|:------------------------------|:-------------------------------------------------------------------------------------------------------------------------------|
| Veri Kalitesi          | ✅ Çok İyi                    | Duplicate, eksik veri, outlier sorunu yok. TotalCharges leakage + multicollinearity nedeniyle çıkarıldı.                       |
| Missing Value Strategy | ✅ Tamamlandı                 | TotalCharges çıkarıldı (11 eksik değer sorunu otomatik çözüldü). Kalan değişkenlerde eksik veri yok.                           |
| Encoding Strategy      | ✅ Tamamlandı                 | Binary: Label Encoding. Contract: Ordinal Encoding. Diğerleri: One-Hot Encoding (drop_first=True).                             |
| Scaling Strategy       | ✅ Tamamlandı                 | StandardScaler uygulandı (tenure, MonthlyCharges, SeniorCitizen). Tree-based modeller için scaling opsiyonel.                  |
| Feature Engineering    | ✅ Tamamlandı                 | tenure_group, MonthlyCharges_category, FiberOptic_NoSecurity interaction feature oluşturuldu.                                  |
| Imbalance Strategy     | ✅ SMOTE Gerekli Değil        | Churn=Yes %26.54 - makul denge. Stratified split yeterli. SMOTE kullanma, model bias yaratabilir.                              |
| Leakage Status         | ✅ Temiz                      | TotalCharges + customerID çıkarıldı. Target encoding/SMOTE uygulanmadı. Tüm transformasyon split-aware.                        |
| Train-Test Split       | ✅ Tamamlandı                 | 80-20 Stratified Split (random_state=42). Train: 5634, Test: 1409 satır.                                                       |
| Feature Count          | ✅ 30 Feature                 | TotalCharges çıkarıldı, 3 yeni feature eklendi. One-hot encoding dimension explosion kontrol altında.                          |
| Önerilen Model Türleri | 📋 Baseline + Tree + Ensemble | Baseline: Logistic Regression. Tree: Random Forest, XGBoost, LightGBM. Ensemble: Voting, Stacking. En az 12 model karşılaştır. |

---

## 4. ÖNERİLEN MODELLİK STRATEJİSİ

### Baseline Modeller:
1. **Logistic Regression** (yorumlanabilirlik için)
   - Regularization: L1 (Lasso) veya L2 (Ridge)
   - class_weight='balanced' dene

### Tree-Based Modeller:
2. **Random Forest** (stable, interpretable)
3. **XGBoost** (high performance)
4. **LightGBM** (fast, efficient)
5. **CatBoost** (categorical handling)

### Ensemble Modeller:
6. **Voting Classifier** (Soft/Hard voting)
7. **Stacking** (Meta-learner)

### Diğer:
8. **Support Vector Machine (SVM)**
9. **K-Nearest Neighbors (KNN)**
10. **Naive Bayes**
11. **Gradient Boosting**
12. **AdaBoost**

**Minimum Karşılaştırma:** 12 model (PrettyTable ile raporla)

---

## 5. EVALUATION METRİKLERİ

| Metrik | Öncelik | Açıklama |
|--------|---------|----------|
| **AUC-ROC** | Yüksek | Sınıf ayrımı kalitesi (0.5-1.0) |
| **Precision** | Yüksek | Churn tahminlerinin doğruluk oranı |
| **Recall** | Yüksek | Gerçek churn müşterilerini yakalama oranı |
| **F1-Score** | Yüksek | Precision-Recall dengesi |
| **Confusion Matrix** | Yüksek | TP, FP, TN, FN analizi |
| **Accuracy** | Orta | Genel doğruluk (imbalance dikkat) |

---

## 6. KRİTİK UYARILAR

⚠️ **SMOTE KULLANMA**
- Churn=Yes oranı %26.54 - makul dengede
- Aggressive sampling model bias yaratır
- Stratified split yeterli

⚠️ **TOTALCHARGES GERİ EKLEME**
- Leakage + multicollinearity riski yüksek
- Model bias yaratır

⚠️ **TEST VERİDE FIT KULLANMA**
- Scaler train veriye fit edildi
- Test veriye sadece transform uygulanmalı
- Leakage önleme için kritik

⚠️ **FEATURE IMPORTANCE**
- Tree-based modellerde feature importance analiz et
- Contract, tenure, MonthlyCharges en önemli değişkenler olmalı

---

## 7. KAYDEDILEN DOSYALAR

| Dosya | Boyut | Açıklama |
|-------|-------|----------|
| data/model_ready/X_train.csv | (5612, 30) | Eğitim feature'ları |
| data/model_ready/X_test.csv | (1404, 30) | Test feature'ları |
| data/model_ready/y_train.csv | (5612,) | Eğitim hedef değişkeni |
| data/model_ready/y_test.csv | (1404,) | Test hedef değişkeni |
| models/preprocessing_scaler.pkl | - | StandardScaler objesi |
| reports/csv/model_expert_handoff.csv | - | Handoff raporu |

---

## 8. SONUÇ VE YOL HARİTASI

✅ **Veri Hazırlama Tamamlandı**
- Leakage riski yok
- Encoding, scaling, feature engineering uygulandı
- Train-test split stratified
- Model-ready veri kaydedildi

🎯 **Sonraki Adım: Model Expert**
- En az 12 model karşılaştır
- Baseline: Logistic Regression
- Tree-based: Random Forest, XGBoost, LightGBM
- Ensemble: Voting, Stacking
- Hyperparameter tuning: GridSearchCV (5-fold CV)
- Confusion Matrix ve Feature Importance analizi

---

**DataPrep Expert İmzası**  
Veri hazırlama tamamlandı, modellemeye hazır. Model Expert devreye girebilir.
