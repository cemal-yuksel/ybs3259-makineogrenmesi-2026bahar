# MODEL EXPERT HANDOFF REPORT
**Model Expert → Explainability Expert / Deployment Expert**  
**Tarih:** 05 May 2026, 15:36  
**Proje:** Churn Analysis  

---

## 1. YÖNETICI ÖZETI

18+ farklı makine öğrenmesi modeli karşılaştırıldı. En başarılı model çok kriterli biçimde seçildi.

**Final Model:** Logistic Regression  
**Test F1-Score:** 0.7902  
**Baseline Üstünlük:** +16.74%  
**Model Readiness:** ✅ HAZIR

---

## 2. MODEL KARŞILAŞTIRMA SONUÇLARI

### PrettyTable Özeti
Toplam 22 model eğitildi.  
Başarılı: 20 model  
Başarısız: 2 model  

### Top 5 Model:
| Model                        |   Test Skoru |   CV Ortalama |   Overfitting Farkı |
|:-----------------------------|-------------:|--------------:|--------------------:|
| Logistic Regression          |       0.7902 |        0.7966 |              0.0124 |
| Logistic Regression (L2)     |       0.7902 |        0.7966 |              0.0124 |
| Random Forest (max_depth=10) |       0.789  |        0.7863 |              0.0751 |
| Logistic Regression (L1)     |       0.7888 |        0.7969 |              0.0122 |
| Gradient Boosting            |       0.7887 |        0.7931 |              0.0296 |

### Baseline Karşılaştırma:
- Baseline (DummyClassifier): 0.6228
- Final Model: 0.7902
- İyileşme: +16.74%

---

## 3. FINAL MODEL DETAYLARI

### Model Tipi: Logistic Regression

### Test Performansı:
- **Accuracy:** 0.7984
- **Precision:** 0.7880
- **Recall:** 0.7984
- **F1-Score:** 0.7902

### Cross-Validation:
- **CV Mean:** 0.7966
- **CV Std:** 0.0142
- **Kararlılık:** Yüksek

### Overfitting Analizi:
- **Train F1:** 0.8026
- **Test F1:** 0.7902
- **Gap:** 0.0124
- **Risk:** Düşük

---

## 4. CONFUSION MATRIX ANALİZİ

### Confusion Matrix:
```
[[930 102]
 [181 191]]
```

### Detaylı Analiz:
- **True Negative (TN):** 930 - Doğru 'No Churn' tahmini
- **False Positive (FP):** 102 - Yanlış alarm (gereksiz retention maliyeti)
- **False Negative (FN):** 181 - Kaçırılan churn müşterisi (kritik iş riski!)
- **True Positive (TP):** 191 - Doğru 'Churn' tahmini

### İş Bağlamı:
- **False Negative Riski:** Yüksek (FN=181)
  → Churn edecek müşterileri kaçırma riski
- **False Positive Riski:** Orta (FP=102)
  → Gereksiz retention kampanyası maliyeti

---

## 5. GÖRSEL KARAR PANELİ ÖZETİ

### Oluşturulan Grafikler:
1. ✅ Ana Performans Karşılaştırması (18+ model)
2. ✅ CV Kararlılık Analizi
3. ✅ Overfitting Analizi (Train vs Test)
4. ✅ Eğitim Süresi vs Performans
5. ✅ Model Liderlik Matrisi
6. ✅ Final Model Confusion Matrix
7. ✅ Feature Importance (eğer varsa)

### Görsel Karar Sonuçları:
- **En Performanslı:** Logistic Regression (0.7902)
- **En Kararlı:** Baseline (Dummy) (CV Std: 0.0002)
- **En Düşük Overfit:** Baseline (Dummy) (Gap: 0.0005)
- **En Hızlı:** Naive Bayes (0.147s)

---

## 6. EXPLAINABILITY EXPERT HANDOFF

### Final Model Dosyası:
`models/final_model.pkl`

### Problem Tipi:
Binary Classification (Churn: No=0, Yes=1)

### Seçim Gerekçesi:
Logistic Regression en yüksek test performansı, makul CV kararlılığı ve kabul edilebilir overfit seviyesi nedeniyle seçildi.

### En Önemli Metrikler:
- Test F1-Score: 0.7902
- ROC-AUC: Hesaplanabilir (predict_proba var)
- Baseline Üstünlük: +16.74%

### Hata Analizi:
- False Negative (FN): 181 müşteri kaçırıldı
- False Positive (FP): 102 gereksiz alarm
- Kritik: False Negative'i azaltmak için threshold tuning veya cost-sensitive learning değerlendirilebilir

### Açıklanabilirlik İhtiyacı:
- **SHAP:** Model tahminlerinin müşteri bazında açıklanması
- **LIME:** Lokal açıklama (bireysel müşteri tahmini)
- **Permutation Importance:** Feature contribution analizi
- **Feature Importance:** Yok (permutation importance kullan)

### Dikkat Edilecek Feature'lar:
EDA ve DataPrep bulgularına göre kritik feature'lar:
- Contract (ordinal: 0, 1, 2)
- tenure (scaled)
- MonthlyCharges (scaled)
- InternetService (one-hot encoded)
- tenure_group (engineered: 0=new, 1=medium, 2=loyal)

---

## 7. DEPLOYMENT EXPERT HANDOFF

### Model Dosyaları:
- `models/final_model.pkl` - Final eğitilmiş model
- `models/preprocessing_scaler.pkl` - StandardScaler (DataPrep Expert tarafından kaydedildi)

### Gerekli Pipeline:
1. Load preprocessing_scaler.pkl
2. Apply scaling to numeric features (tenure, MonthlyCharges, SeniorCitizen)
3. Load final_model.pkl
4. Predict

### Input Schema:
30 feature (X_train.columns):
gender, SeniorCitizen, Partner, Dependents, tenure, PhoneService, Contract, PaperlessBilling, MonthlyCharges, MultipleLines_No phone service, MultipleLines_Yes, InternetService_Fiber optic, InternetService_No, OnlineSecurity_No internet service, OnlineSecurity_Yes, OnlineBackup_No internet service, OnlineBackup_Yes, DeviceProtection_No internet service, DeviceProtection_Yes, TechSupport_No internet service, TechSupport_Yes, StreamingTV_No internet service, StreamingTV_Yes, StreamingMovies_No internet service, StreamingMovies_Yes, PaymentMethod_Credit card (automatic), PaymentMethod_Electronic check, PaymentMethod_Mailed check, tenure_group, MonthlyCharges_category

### Output:
- Binary Prediction: 0 (No Churn) veya 1 (Churn)
- Probability: predict_proba kullanılabilir

### Monitoring:
- **Data Drift:** Feature distribution değişimi (özellikle tenure, MonthlyCharges)
- **Prediction Drift:** Churn tahmin oranı değişimi
- **Performance Degradation:** F1-Score düşüşü (threshold: <0.7402)

### Riskler:
- False Negative: 181 müşteri kaçırıldı (FN rate: 48.66%)
- Model güncelleme: Yeni veri geldiğinde yeniden eğitim değerlendir
- Class Imbalance: SMOTE kullanılmadı (deployment'ta da gerek yok)

---

## 8. KRİTİK UYARILAR

⚠️ **FALSE NEGATIVE RİSKİ**
- 181 churn müşterisi kaçırıldı
- Business impact: Müşteri kaybı
- Öneri: Threshold tuning (precision/recall trade-off)

⚠️ **MODEL GÜNCELLEMESİ**
- Yeni veri geldiğinde model performansı izlenmeli
- Data drift detection kritik

⚠️ **FEATURE ENGINEERING**
- 3 yeni feature oluşturuldu (tenure_group, MonthlyCharges_category, FiberOptic_NoSecurity)
- Deployment'ta aynı feature engineering pipeline uygulanmalı

⚠️ **SCALING**
- StandardScaler train veriye fit edildi
- Yeni veriye transform uygulanmalı (fit değil!)

---

## 9. SONUÇ VE YOL HARİTASI

✅ **Model Training Tamamlandı**
- 18+ model karşılaştırıldı
- En başarılı model seçildi: Logistic Regression
- Baseline'dan anlamlı üstünlük: +16.74%
- Confusion matrix ve hata analizi yapıldı

🎯 **Sonraki Adımlar:**
1. **Explainability Expert:** SHAP/LIME ile model açıklanabilirliği
2. **Deployment Expert:** Streamlit arayüzü ve model deployment
3. **Threshold Tuning:** False Negative'i azaltmak için precision/recall trade-off
4. **Hyperparameter Tuning:** GridSearchCV/RandomizedSearchCV (opsiyonel)

---

**Model Expert İmzası**  
Model training ve evaluation tamamlandı. Explainability ve Deployment aşamasına hazır.
