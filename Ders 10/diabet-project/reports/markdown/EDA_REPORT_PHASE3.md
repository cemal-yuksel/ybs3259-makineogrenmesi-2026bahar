# PHASE 3: BIVARIATE ANALYSIS - Detaylı Rapor

## 📊 Yapılan Analiz:

Bu aşamada **Outcome (hedef değişken)** ile 8 sayısal değişken arasındaki ikili ilişkiler incelenmiştir. Her değişken için:
- Grup bazlı istatistikler (ortalama, medyan, std, min, max)
- Ortalama farkları ve yüzde değişimler
- **Mann-Whitney U testi** (non-parametrik test) ile istatistiksel anlamlılık kontrolü
- **Boxplot** ve **Violin Plot** görselleştirmeleri

**Kod:** `phase3_bivariate_analysis.py`  
**Görsel Sayısı:** 17 adet (1 hedef dağılımı + 16 değişken analizi)  
**Kaydedilen Rapor:** `reports/csv/phase3_bivariate_summary.csv`

---

## 🧠 Koddan Elde Edilen Bulgular:

### **FEATURE IMPORTANCE RANKING (İstatistiksel Anlamlılığa Göre)**

Mann-Whitney U testine göre değişkenlerin hedef değişkenle ilişki gücü:

| Sıra | Değişken | Ort. Fark (%) | p-value | Anlamlılık | Güç |
|------|----------|---------------|---------|------------|-----|
| 1 | **Glucose** | %28.4 | <0.0001 | ⭐⭐⭐ Çok Güçlü | En güçlü öngörücü |
| 2 | **Pregnancies** | %47.5 | <0.0001 | ⭐⭐⭐ Çok Güçlü | İkinci en güçlü |
| 3 | **BMI** | %16.0 | <0.0001 | ⭐⭐⭐ Çok Güçlü | Üçüncü en güçlü |
| 4 | **Age** | %18.8 | <0.0001 | ⭐⭐⭐ Çok Güçlü | Dördüncü en güçlü |
| 5 | **DiabetesPedigreeFunction** | %28.1 | <0.0001 | ⭐⭐⭐ Çok Güçlü | Beşinci en güçlü |
| 6 | **BloodPressure** | %3.9 | 0.0001 | ⭐⭐⭐ Çok Güçlü | Altıncı en güçlü |
| 7 | **SkinThickness** | %12.7 | 0.0130 | ⭐⭐ Anlamlı | Zayıf ama anlamlı |
| 8 | **Insulin** | %45.9 | 0.0657 | ❌ İlişki Yok | İstatistiksel olarak anlamsız |

---

### **1. Glucose (Glikoz Seviyesi)** ⭐⭐⭐ EN GÜÇLÜ ÖNGÖRÜCÜ

**Grup Bazlı Ortalamalar:**
- Diyabet Yok (0): **109.98**
- Diyabet Var (1): **141.26**
- Fark: **31.28** (%28.4 artış)

**İstatistiksel Test:**
- Mann-Whitney U p-value: **<0.0001** (çok güçlü ilişki)

**Yorum:**
- Glikoz seviyesi, diyabet varlığını ayırt etmede **en güçlü değişkendir**.
- Diyabet olan hastalarda glikoz seviyesi ortalama %28.4 daha yüksektir.
- Model eğitiminde bu değişken **en yüksek feature importance** alacaktır.
- ⚠️ Ancak %0.65 oranında gizli eksik veri (0 değerleri) var - imputasyon gerekli.

**Modelleme Etkisi:**
- Kritik önem taşır, kesinlikle modelde olmalı.
- Tek başına bile güçlü tahmin yapabilir.

---

### **2. Pregnancies (Hamilelik Sayısı)** ⭐⭐⭐ İKİNCİ EN GÜÇLÜ

**Grup Bazlı Ortalamalar:**
- Diyabet Yok (0): **3.30**
- Diyabet Var (1): **4.87**
- Fark: **1.57** (%47.5 artış)

**İstatistiksel Test:**
- Mann-Whitney U p-value: **<0.0001** (çok güçlü ilişki)

**Yorum:**
- Diyabet olan hastalarda ortalama hamilelik sayısı %47.5 daha fazladır.
- Hamilelik sayısı arttıkça diyabet riski artıyor.
- Bu bulgu, gebelik diyabeti (gestational diabetes) ve Tip 2 diyabet ilişkisini yansıtıyor olabilir.

**Modelleme Etkisi:**
- Güçlü öngörücü, kesinlikle modelde olmalı.
- Feature engineering fırsatı: `Pregnancies > 5` gibi binary feature oluşturulabilir.

---

### **3. BMI (Vücut Kitle İndeksi)** ⭐⭐⭐ ÜÇÜNCÜ EN GÜÇLÜ

**Grup Bazlı Ortalamalar:**
- Diyabet Yok (0): **30.30**
- Diyabet Var (1): **35.14**
- Fark: **4.84** (%16.0 artış)

**İstatistiksel Test:**
- Mann-Whitney U p-value: **<0.0001** (çok güçlü ilişki)

**Yorum:**
- Diyabet olan hastalarda BMI ortalama %16 daha yüksek.
- Her iki grupta da BMI >30 (obezite eşiği) - bu, veri setinin yüksek riskli bir popülasyon olduğunu gösteriyor.
- ⚠️ %1.43 oranında gizli eksik veri (0 değerleri) var.

**Modelleme Etkisi:**
- Güçlü öngörücü, kesinlikle modelde olmalı.
- Feature engineering: `BMI_category` (normal, overweight, obese) oluşturulabilir.

---

### **4. Age (Yaş)** ⭐⭐⭐ DÖRDÜNCÜ EN GÜÇLÜ

**Grup Bazlı Ortalamalar:**
- Diyabet Yok (0): **31.19**
- Diyabet Var (1): **37.07**
- Fark: **5.88** (%18.8 artış)

**İstatistiksel Test:**
- Mann-Whitney U p-value: **<0.0001** (çok güçlü ilişki)

**Yorum:**
- Diyabet olan hastalarda ortalama yaş %18.8 daha yüksek.
- Yaş arttıkça diyabet riski artıyor.
- Veri setinde genç hasta ağırlıklı (medyan 29 yaş).

**Modelleme Etkisi:**
- Güçlü öngörücü, kesinlikle modelde olmalı.
- Feature engineering: `Age_group` (young, middle, old) veya `Age > 40` gibi binary feature.

---

### **5. DiabetesPedigreeFunction (Diyabet Soy Ağacı Fonksiyonu)** ⭐⭐⭐ BEŞİNCİ EN GÜÇLÜ

**Grup Bazlı Ortalamalar:**
- Diyabet Yok (0): **0.43**
- Diyabet Var (1): **0.55**
- Fark: **0.12** (%28.1 artış)

**İstatistiksel Test:**
- Mann-Whitney U p-value: **<0.0001** (çok güçlü ilişki)

**Yorum:**
- Genetik/ailevi diyabet riski, diyabet varlığıyla çok güçlü ilişkili.
- Diyabet olan hastalarda soy ağacı fonksiyonu %28.1 daha yüksek.
- Bu değişken, domain knowledge açısından kritik.

**Modelleme Etkisi:**
- Güçlü öngörücü, kesinlikle modelde olmalı.
- Yüksek çarpıklık (skewness: 1.920) nedeniyle log dönüşümü faydalı olabilir.

---

### **6. BloodPressure (Kan Basıncı)** ⭐⭐⭐ ALTINCI EN GÜÇLÜ

**Grup Bazlı Ortalamalar:**
- Diyabet Yok (0): **68.18**
- Diyabet Var (1): **70.82**
- Fark: **2.64** (%3.9 artış)

**İstatistiksel Test:**
- Mann-Whitney U p-value: **0.0001** (çok güçlü ilişki)

**Yorum:**
- İstatistiksel olarak anlamlı ama grup farkı düşük (%3.9).
- ⚠️ %4.56 oranında gizli eksik veri (0 değerleri) var.
- ⚠️ %5.86 outlier oranı (kritik eşiğin üzerinde).
- ⚠️ Yüksek negatif çarpıklık (-1.844).

**Modelleme Etkisi:**
- Anlamlı ama zayıf öngörücü.
- Veri kalitesi sorunlu - imputasyon ve outlier yönetimi kritik.

---

### **7. SkinThickness (Cilt Kalınlığı)** ⭐⭐ ZAYIF AMA ANLAMLI

**Grup Bazlı Ortalamalar:**
- Diyabet Yok (0): **19.66**
- Diyabet Var (1): **22.16**
- Fark: **2.50** (%12.7 artış)

**İstatistiksel Test:**
- Mann-Whitney U p-value: **0.0130** (anlamlı ilişki, ama zayıf)

**Yorum:**
- İstatistiksel olarak anlamlı ama çok zayıf ilişki.
- 🚨 **%29.56 oranında gizli eksik veri** - veri kalitesi çok düşük!
- Model performansına katkısı şüpheli.

**Modelleme Etkisi:**
- **Kritik Karar:** Bu değişken modelden **çıkarılabilir**.
- Alternatif: İleri imputasyon (IterativeImputer) denenebilir, ancak %30 eksik veri çok riskli.

---

### **8. Insulin (İnsülin Seviyesi)** ❌ İSTATİSTİKSEL OLARAK ANLAMLI DEĞİL

**Grup Bazlı Ortalamalar:**
- Diyabet Yok (0): **68.79**
- Diyabet Var (1): **100.34**
- Fark: **31.54** (%45.9 artış)

**İstatistiksel Test:**
- Mann-Whitney U p-value: **0.0657** (p>0.05, anlamsız!)

**Yorum:**
- Ortalama fark %45.9 gibi yüksek görünüyor ama istatistiksel olarak **anlamlı değil**.
- Neden? 🚨 **%48.70 oranında gizli eksik veri** (374/768)!
- Verilerin neredeyse yarısı 0 olarak kodlanmış, bu da test gücünü düşürüyor.
- Medyan bile 0 (diyabet var grubu için)!

**Modelleme Etkisi:**
- **Kritik Karar:** Bu değişken modelden **çıkarılmalı** veya çok ileri imputasyon stratejisi uygulanmalı.
- %50 eksik veri ile imputasyon yapılsa bile model bias riski çok yüksek.
- **Öneri:** İki pipeline oluştur:
  - Pipeline 1: Insulin dahil (ileri imputasyon)
  - Pipeline 2: Insulin hariç
  - Performansları karşılaştır.

---

## 💡 Analitik Yorum:

### **1. Feature Selection Stratejisi**

**Tier 1: Kesinlikle Modelde Olmalı (p<0.001, yüksek fark)**
- ✅ Glucose
- ✅ Pregnancies
- ✅ BMI
- ✅ Age
- ✅ DiabetesPedigreeFunction

**Tier 2: Kullanılabilir (p<0.001, düşük fark)**
- ⚠️ BloodPressure (veri kalitesi sorunlu, ama anlamlı)

**Tier 3: Şüpheli (p<0.05, zayıf ilişki, yüksek eksik veri)**
- ❌ SkinThickness (model performansını düşürebilir)

**Tier 4: Çıkarılmalı (p>0.05, çok yüksek eksik veri)**
- ❌ Insulin (istatistiksel olarak anlamsız, %48.7 eksik veri)

---

### **2. Model Stratejisi Önerisi**

**Baseline Model (6 Değişken):**
- Glucose, Pregnancies, BMI, Age, DiabetesPedigreeFunction, BloodPressure
- Basit imputasyon (median) düşük oranlı eksik veriler için
- Bu model sağlam ve güvenilir olacaktır.

**Advanced Model (8 Değişken):**
- Tüm değişkenler dahil
- İleri imputasyon (IterativeImputer/KNN)
- Riskli ama daha zengin feature space
- Performans karşılaştırması gerekli.

**Recommendation:**
- İki pipeline yan yana eğitilmeli.
- Baseline model daha güvenli.
- Advanced model ancak cross-validation ile validation edilebilirse kullanılmalı.

---

### **3. Feature Engineering Fırsatları**

**Binary Features:**
```python
df['High_Glucose'] = (df['Glucose'] > 140).astype(int)
df['High_BMI'] = (df['BMI'] > 30).astype(int)
df['Many_Pregnancies'] = (df['Pregnancies'] > 5).astype(int)
df['Old_Age'] = (df['Age'] > 40).astype(int)
```

**Interaction Features:**
```python
df['BMI_Age'] = df['BMI'] * df['Age']
df['Glucose_BMI'] = df['Glucose'] * df['BMI']
df['Pregnancies_Age'] = df['Pregnancies'] * df['Age']
```

**Rationale:**
- BMI ve Age birlikte yüksekse, risk daha da artıyor olabilir.
- Glucose ve BMI birlikte yüksekse, metabolik sendrom riski.

---

## ⚠️ Risk / Dikkat Edilmesi Gereken Nokta:

### **1. Insulin ve SkinThickness Değişkenleri (Yüksek Risk)**

- Bu iki değişken çok yüksek oranda gizli eksik veri içeriyor (%29-49).
- Insulin istatistiksel olarak bile anlamlı değil (p=0.0657).
- **Strateji:** Bu değişkenler olmadan baseline model eğit, sonra advanced model ile karşılaştır.

### **2. Class Imbalance (Orta Risk)**

- Baskın sınıf oranı: %65.1 (Diyabet yok)
- Bu oran %70'in altında olduğu için kritik değil, ama stratified split şart.
- Öneri: **Stratified K-Fold CV** kullan, class weighting uygula.

### **3. Feature Importance ve Model Seçimi**

- Glucose, Pregnancies, BMI, Age - bu 4 değişken çok güçlü.
- Lineer modeller (LogisticRegression) için çarpıklık dönüşümü gerekli.
- Tree-based modeller (RandomForest, XGBoost) çarpıklığa duyarsız, dönüşüm gerekmez.

---

## 🔁 Agent Etkileşim Notu:

### **Data Prep Expert İçin Öneriler:**

#### **1. Değişken Seçimi (Yüksek Öncelik)**

**Baseline Pipeline (Önerilen):**
```python
selected_features = ['Glucose', 'Pregnancies', 'BMI', 'Age', 
                     'DiabetesPedigreeFunction', 'BloodPressure']
```

**Advanced Pipeline (Riskli):**
```python
all_features = ['Glucose', 'Pregnancies', 'BMI', 'Age', 
                'DiabetesPedigreeFunction', 'BloodPressure',
                'SkinThickness', 'Insulin']
```

#### **2. İmputasyon Stratejisi (Yüksek Öncelik)**

**Düşük eksik veri (%0-5):**
- Glucose (%0.65), BMI (%1.43) → Median imputation

**Orta eksik veri (%4-5):**
- BloodPressure (%4.56) → KNN Imputer (k=5)

**Yüksek eksik veri (%29-49):**
- SkinThickness (%29.56), Insulin (%48.70) → **İki alternatif:**
  - Alternatif 1: Bu değişkenleri modelden çıkar (önerilen)
  - Alternatif 2: IterativeImputer (MICE) kullan, ancak overfitting riski yüksek

#### **3. Feature Engineering (Orta Öncelik)**

```python
# Binary features
df['High_Glucose'] = (df['Glucose'] > 140).astype(int)
df['High_BMI'] = (df['BMI'] > 30).astype(int)
df['Many_Pregnancies'] = (df['Pregnancies'] > 5).astype(int)

# Interaction features
df['BMI_Age_Interaction'] = df['BMI'] * df['Age']
df['Glucose_BMI_Interaction'] = df['Glucose'] * df['BMI']
```

#### **4. Cross-Validation Stratejisi (Yüksek Öncelik)**

```python
from sklearn.model_selection import StratifiedKFold

cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
```

---

## 📁 Kaydedilen Görseller:

**Hedef Değişken:**
- `figures/phase3_target_distribution.html/png`

**Boxplotlar (8 adet):**
- `figures/phase3_boxplot_pregnancies_vs_outcome.html/png`
- `figures/phase3_boxplot_glucose_vs_outcome.html/png`
- `figures/phase3_boxplot_bloodpressure_vs_outcome.html/png`
- `figures/phase3_boxplot_skinthickness_vs_outcome.html/png`
- `figures/phase3_boxplot_insulin_vs_outcome.html/png`
- `figures/phase3_boxplot_bmi_vs_outcome.html/png`
- `figures/phase3_boxplot_diabetespedigreefunction_vs_outcome.html/png`
- `figures/phase3_boxplot_age_vs_outcome.html/png`

**Violin Plots (8 adet):**
- `figures/phase3_violin_pregnancies_vs_outcome.html/png`
- `figures/phase3_violin_glucose_vs_outcome.html/png`
- `figures/phase3_violin_bloodpressure_vs_outcome.html/png`
- `figures/phase3_violin_skinthickness_vs_outcome.html/png`
- `figures/phase3_violin_insulin_vs_outcome.html/png`
- `figures/phase3_violin_bmi_vs_outcome.html/png`
- `figures/phase3_violin_diabetespedigreefunction_vs_outcome.html/png`
- `figures/phase3_violin_age_vs_outcome.html/png`

**CSV Raporlar:**
- `reports/csv/phase3_bivariate_summary.csv` (p-value'ya göre sıralı)
- `reports/csv/phase3_data_prep_recommendations.csv` (7 öneri)

---

## ✅ Phase 3 Tamamlandı - Sırada: Phase 4 (Multivariate Analysis)
