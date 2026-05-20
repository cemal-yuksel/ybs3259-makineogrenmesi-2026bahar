# PHASE 4: MULTIVARIATE ANALYSIS - Detaylı Rapor

## 📊 Yapılan Analiz:

Bu aşamada tüm sayısal değişkenler (Outcome dahil) arasındaki **çok değişkenli ilişkiler** incelenmiştir. Pearson korelasyon matrisi hesaplanmış, **multicollinearity riski** kontrol edilmiş ve **Outcome ile korelasyonlar** (feature importance proxy) görselleştirilmiştir.

**Kod:** `phase4_multivariate_analysis.py`  
**Görsel Sayısı:** 3 adet (correlation heatmap, outcome correlations, scatter matrix)  
**Kaydedilen Raporlar:**
- `reports/csv/phase4_correlation_matrix.csv`
- `reports/csv/phase4_outcome_correlations.csv`

---

## 🧠 Koddan Elde Edilen Bulgular:

### **1. Multicollinearity Kontrolü**

**Yüksek Korelasyonlar (|r| > 0.70):**
- ✅ **HİÇBİRİ YOK!**
- Bu, veri setinde **multicollinearity riskinin düşük** olduğunu gösterir.
- Lineer modeller (LogisticRegression, LinearSVC) için mükemmel bir durum.

**Orta Korelasyonlar (0.50 < |r| < 0.70):**
- ⚠️ **Pregnancies <-> Age: 0.544**
  - Bu korelasyon **beklenen ve mantıklı** bir durumdur.
  - Yaş arttıkça hamilelik sayısı artar (biyolojik ve sosyal gerçeklik).
  - Bu seviyede korelasyon multicollinearity riski oluşturmaz.
  - İki değişken de modelde tutulabilir.

**Sonuç:**
- ✅ Veri seti multicollinearity açısından **sağlıklı**.
- ✅ Regularization (Ridge/Lasso) kullanma ihtiyacı **düşük** (ama yine de denenebilir).
- ✅ Feature selection yapma ihtiyacı **yok** (korelasyon bazlı).

---

### **2. Outcome ile Korelasyonlar (Feature Importance Proxy)**

Outcome ile her değişkenin Pearson korelasyon katsayıları:

| Sıra | Değişken | Korelasyon (r) | Yorum |
|------|----------|----------------|-------|
| 1 | **Glucose** | **0.467** | Çok güçlü, en önemli öngörücü |
| 2 | **BMI** | **0.293** | Güçlü |
| 3 | **Age** | **0.238** | Orta-güçlü |
| 4 | **Pregnancies** | **0.222** | Orta |
| 5 | **DiabetesPedigreeFunction** | **0.174** | Zayıf-orta |
| 6 | Insulin | 0.131 | Zayıf |
| 7 | SkinThickness | 0.075 | Çok zayıf |
| 8 | BloodPressure | 0.065 | Çok zayıf |

**Kritik Gözlemler:**

**Top Tier (r > 0.3):**
- **Glucose: 0.467** - Tek başına çok güçlü öngörücü
  - Bu, Phase 3'teki istatistiksel test sonuçlarıyla (p<0.001) uyumlu
  - Model eğitiminde en yüksek feature importance alacak

**Mid Tier (0.2 < r < 0.3):**
- **BMI: 0.293** - Güçlü öngörücü
- **Age: 0.238** - Güçlü öngörücü
- **Pregnancies: 0.222** - Güçlü öngörücü

**Low Tier (r < 0.2):**
- **DiabetesPedigreeFunction: 0.174** - Zayıf ama anlamlı
- **Insulin: 0.131** - Çok zayıf (muhtemelen %48.7 eksik veri nedeniyle)
- **SkinThickness: 0.075** - Çok zayıf (muhtemelen %29.6 eksik veri nedeniyle)
- **BloodPressure: 0.065** - Çok zayıf

---

### **3. Phase 3 (Bivariate) ile Karşılaştırma**

**Phase 3 (Mann-Whitney U test) ile Phase 4 (Pearson Correlation) sonuçları uyumlu:**

| Değişken | Phase 3 Sıralaması | Phase 4 Sıralaması | Uyum |
|----------|-------------------|-------------------|------|
| Glucose | 1. (p<0.0001) | 1. (r=0.467) | ✅ Uyumlu |
| Pregnancies | 2. (p<0.0001) | 4. (r=0.222) | ⚠️ Küçük fark |
| BMI | 3. (p<0.0001) | 2. (r=0.293) | ✅ Uyumlu |
| Age | 4. (p<0.0001) | 3. (r=0.238) | ✅ Uyumlu |
| DiabetesPedigreeFunction | 5. (p<0.0001) | 5. (r=0.174) | ✅ Uyumlu |
| BloodPressure | 6. (p=0.0001) | 8. (r=0.065) | ⚠️ Büyük fark |
| SkinThickness | 7. (p=0.0130) | 7. (r=0.075) | ✅ Uyumlu |
| Insulin | 8. (p=0.0657) | 6. (r=0.131) | ⚠️ Fark var |

**Uyumsuzluk Açıklamaları:**

- **BloodPressure:** Phase 3'te p=0.0001 (çok anlamlı) ama korelasyon çok düşük (r=0.065)
  - **Neden:** Mann-Whitney U non-lineer ilişkileri de yakalayabilir, Pearson sadece lineer ilişkiyi ölçer.
  - **Yorum:** BloodPressure, Outcome ile **non-lineer** bir ilişkiye sahip olabilir.

- **Insulin:** Phase 3'te p=0.0657 (anlamsız) ama korelasyon r=0.131
  - **Neden:** %48.7 eksik veri, test gücünü düşürüyor.
  - **Yorum:** Her iki testte de zayıf ilişki var, değişken şüpheli.

---

### **4. Değişkenler Arası İlişkiler (Korelasyon Matrisi)**

**Önemli Korelasyonlar:**

**Pregnancies ile:**
- Age: 0.544 (beklenen, mantıklı)
- Glucose: 0.129 (zayıf)

**Glucose ile:**
- Insulin: 0.331 (orta, beklenen - glikoz arttıkça insülin artar)
- BMI: 0.221 (zayıf-orta)
- Age: 0.264 (zayıf-orta)

**BMI ile:**
- Glucose: 0.221 (zayıf-orta)
- SkinThickness: 0.392 (orta, beklenen - BMI arttıkça cilt kalınlığı artar)

**Age ile:**
- Pregnancies: 0.544 (orta, beklenen)
- Glucose: 0.264 (zayıf-orta)
- BloodPressure: 0.240 (zayıf-orta)

**Sonuç:**
- Değişkenler arası korelasyonlar genellikle düşük-orta seviyede.
- Beklenen biyolojik ilişkiler (Glucose-Insulin, BMI-SkinThickness, Age-Pregnancies) doğrulanmış.
- Multicollinearity riski yok.

---

## 💡 Analitik Yorum:

### **1. Multicollinearity Riski: YOK ✅**

- Veri seti multicollinearity açısından **sağlıklı**.
- |r| > 0.70 olan korelasyon yok.
- Lineer modeller (LogisticRegression) için **ideal**.
- **Regularization (Ridge/Lasso) gerekliliği düşük**, ama yine de denenebilir (overfitting kontrolü için).
- **Feature selection ihtiyacı yok** (korelasyon bazlı).

### **2. Feature Importance Hiyerarşisi**

**Tier 1: Kritik Değişkenler (r > 0.3)**
- ✅ **Glucose** (r=0.467)

**Tier 2: Güçlü Değişkenler (0.2 < r < 0.3)**
- ✅ **BMI** (r=0.293)
- ✅ **Age** (r=0.238)
- ✅ **Pregnancies** (r=0.222)

**Tier 3: Zayıf Değişkenler (r < 0.2)**
- ⚠️ DiabetesPedigreeFunction (r=0.174)
- ❌ Insulin (r=0.131)
- ❌ SkinThickness (r=0.075)
- ❌ BloodPressure (r=0.065)

**Modelleme Stratejisi:**
- **Baseline Model:** Tier 1 + Tier 2 (Glucose, BMI, Age, Pregnancies)
- **Advanced Model:** Tier 1 + Tier 2 + Tier 3 seçmeli (DiabetesPedigreeFunction dahil, Insulin-SkinThickness hariç)

### **3. Lineer vs Non-Lineer İlişkiler**

**BloodPressure'ın Durumu:**
- Phase 3: Mann-Whitney U p<0.001 (çok anlamlı)
- Phase 4: Pearson r=0.065 (çok zayıf)
- **Yorum:** BloodPressure, Outcome ile **non-lineer** bir ilişkiye sahip olabilir.
- **Strateji:** Tree-based modeller (RandomForest, XGBoost) BloodPressure'ı daha iyi kullanabilir.

### **4. Model Seçimi İçin İpuçları**

**Lineer Modeller (LogisticRegression, LinearSVC):**
- ✅ Multicollinearity yok, uygun
- ⚠️ Çarpıklık problemi var (Insulin, DiabetesPedigreeFunction, Age) - dönüşüm gerekli
- ⚠️ Non-lineer ilişkiler (BloodPressure) kaybolabilir

**Tree-based Modeller (RandomForest, XGBoost):**
- ✅ Çarpıklık dönüşümü gerekmez
- ✅ Non-lineer ilişkileri yakalayabilir (BloodPressure)
- ✅ Multicollinearity'ye duyarsız
- ⚠️ Yorumlanabilirlik düşük

**Ensemble Modeller:**
- ✅ En iyi performans için önerilir
- Hem lineer hem tree-based modelleri birleştir

---

## ⚠️ Risk / Dikkat Edilmesi Gereken Nokta:

### **1. Insulin ve SkinThickness (Yüksek Risk)**

- Bu iki değişken hem Phase 3'te hem Phase 4'te **zayıf ilişki** gösterdi.
- **Neden:** %29-49 oranında gizli eksik veri.
- **Öneri:** Bu değişkenler **baseline modelden çıkarılmalı**, advanced modelde denenmeli.

### **2. BloodPressure Non-Lineer İlişki (Orta Risk)**

- Pearson korelasyonu çok düşük (r=0.065) ama Mann-Whitney U testi anlamlı (p<0.001).
- **Yorum:** Non-lineer ilişki olabilir.
- **Öneri:** Tree-based modeller BloodPressure'ı daha iyi kullanabilir.

### **3. Feature Engineering Fırsatları**

**Interaction Features (önerilir):**
```python
df['BMI_Age'] = df['BMI'] * df['Age']
df['Glucose_BMI'] = df['Glucose'] * df['BMI']
df['Glucose_Age'] = df['Glucose'] * df['Age']
```

**Neden:**
- BMI ve Age ayrı ayrı güçlü, birlikte daha güçlü olabilir.
- Glucose en güçlü değişken, diğerleriyle interaction oluşturulabilir.

---

## 🔁 Agent Etkileşim Notu:

### **Data Prep Expert İçin Öneriler:**

#### **1. Multicollinearity Yok - Tüm Değişkenler Tutulabilir (Yüksek Öncelik)**

- ✅ |r| > 0.70 olan korelasyon yok.
- ✅ Regularization gerekliliği düşük.
- ⚠️ Yine de Ridge/Lasso denenebilir (overfitting kontrolü için).

#### **2. Feature Selection Stratejisi (Yüksek Öncelik)**

**Baseline Model (Önerilen):**
```python
selected_features = ['Glucose', 'BMI', 'Age', 'Pregnancies', 'DiabetesPedigreeFunction']
```
- Sadece r > 0.17 olan değişkenler
- Veri kalitesi yüksek
- Güvenilir tahmin

**Advanced Model (Riskli):**
```python
all_features = ['Glucose', 'BMI', 'Age', 'Pregnancies', 
                'DiabetesPedigreeFunction', 'BloodPressure']
# Insulin ve SkinThickness hariç
```
- BloodPressure dahil (non-lineer ilişki potansiyeli)
- Insulin ve SkinThickness hariç (çok zayıf korelasyon + yüksek eksik veri)

#### **3. Feature Engineering (Orta Öncelik)**

**Interaction Features:**
```python
# En güçlü değişkenler arası interactionlar
df['BMI_Age'] = df['BMI'] * df['Age']
df['Glucose_BMI'] = df['Glucose'] * df['BMI']
df['Glucose_Age'] = df['Glucose'] * df['Age']
df['Pregnancies_Age'] = df['Pregnancies'] * df['Age']
```

**Polynomial Features (opsiyonel):**
```python
from sklearn.preprocessing import PolynomialFeatures

poly = PolynomialFeatures(degree=2, include_bias=False, interaction_only=True)
# Sadece interaction terimler, quadratic terimler değil
```

#### **4. Model Seçimi Önerisi (Yüksek Öncelik)**

**Lineer Modeller:**
- LogisticRegression (baseline)
- LogisticRegression + Ridge/Lasso (regularized)
- LinearSVC

**Tree-based Modeller:**
- RandomForestClassifier (non-lineer ilişkiler için)
- XGBoostClassifier (en iyi performans için)
- LightGBMClassifier

**Ensemble:**
- VotingClassifier (Logistic + RandomForest + XGBoost)
- StackingClassifier

---

## 📁 Kaydedilen Görseller:

- `figures/phase4_correlation_heatmap.html/png` - Tüm değişkenler arası korelasyon matrisi
- `figures/phase4_outcome_correlations.html/png` - Outcome ile korelasyonlar (feature importance)
- `figures/phase4_scatter_matrix.html/png` - Top 5 değişken + Outcome scatter matrix

**CSV Raporlar:**
- `reports/csv/phase4_correlation_matrix.csv` - Tam korelasyon matrisi
- `reports/csv/phase4_outcome_correlations.csv` - Outcome korelasyonları (sıralı)

---

## ✅ Phase 4 Tamamlandı - Sırada: Phase 5 (Data Quality & Anomaly Detection)
