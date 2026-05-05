# PHASE 4: MULTIVARIATE ANALYSIS - ÇOKLU DEĞİŞKEN İLİŞKİLERİ

## 📊 Yapılan Analiz

Bu aşamada çok değişkenli yapı incelendi. TotalCharges veri kalitesi sorunu çözüldü (object → numeric), korelasyon matrisi oluşturuldu, VIF (Variance Inflation Factor) analizi ile multicollinearity kontrol edildi ve scatter plotlar çizildi.

**Analiz Kapsamı:**
- TotalCharges veri tipi düzeltmesi
- 4 sayısal değişken korelasyon analizi
- VIF analizi (multicollinearity)
- 3 scatter plot (ikili ilişkiler)

---

## 🧠 Koddan Elde Edilen Bulgular

### 1. TotalCharges Veri Kalitesi Düzeltmesi

**📊 Tespit Edilen Sorun:**
- Önceki veri tipi: **object (string)**
- **11 satırda boşluk karakteri** tespit edildi (%0.16)

**✅ Uygulanan Çözüm:**
- Boşluklar NaN'a çevrildi
- TotalCharges numeric (float64) tipine dönüştürüldü
- Dönüşüm sonrası: **11 NaN** (%0.16) - düşük oran

**📈 TotalCharges İstatistikleri (NaN hariç, n=7,032):**
- Ortalama: $2,283.30
- Medyan: $1,397.48
- Std. Sapma: $2,266.77
- Min: $18.80 | Max: $8,684.80

### 2. Korelasyon Matrisi

| | SeniorCitizen | tenure | MonthlyCharges | TotalCharges |
|---|---|---|---|---|
| **SeniorCitizen** | 1.000 | 0.017 | 0.220 | 0.102 |
| **tenure** | 0.017 | 1.000 | 0.248 | **0.826** |
| **MonthlyCharges** | 0.220 | 0.248 | 1.000 | 0.651 |
| **TotalCharges** | 0.102 | **0.826** | 0.651 | 1.000 |

**🔴 Yüksek Korelasyon (|r| > 0.80):**
- **tenure ↔ TotalCharges**: r = **0.826** (çok güçlü pozitif ilişki)

**🟡 Orta-Yüksek Korelasyon (0.50 < |r| < 0.80):**
- **MonthlyCharges ↔ TotalCharges**: r = **0.651** (güçlü pozitif ilişki)

### 3. VIF (Multicollinearity) Analizi

| Değişken | VIF | Yorumlama |
|---|---|---|
| **SeniorCitizen** | 1.26 | ✅ Düşük multicollinearity |
| **tenure** | 6.33 | ⚠️ Orta multicollinearity |
| **MonthlyCharges** | 3.70 | ✅ Düşük multicollinearity |
| **TotalCharges** | 8.09 | ⚠️ Orta multicollinearity |

**📖 VIF Yorumlama:**
- VIF < 5: Düşük multicollinearity (kabul edilebilir)
- 5 ≤ VIF < 10: Orta multicollinearity (izlenmeli)
- VIF ≥ 10: Yüksek multicollinearity (müdahale gerekli)

**✅ Sonuç:** Hiçbir değişkende VIF ≥ 10 yok, kritik multicollinearity sorunu yok.

---

## 💡 Analitik Yorum (YBS Uzmanı Perspektifi)

### 1. TotalCharges Veri Kalitesi - Başarıyla Çözüldü

**📊 Kritik Bulgu:**
11 satırda (%0.16) TotalCharges boşluk karakteri içeriyordu. Bu PHASE 1 ve PHASE 2'de tespit edilen veri kalitesi sorunuydu.

**💼 İş Değeri Yorumu:**
- **%0.16 NaN oranı çok düşüktür** ve veri setine ciddi zarar vermez
- NaN olan satırlar muhtemelen **yeni müşteriler** (tenure=0 veya çok düşük) olabilir
- Bu satırlar:
  - **Silme stratejisi** kullanılabilir (sadece 11 satır → %0.16 kayıp)
  - **Imputasyon stratejisi** kullanılabilir: `TotalCharges = tenure × MonthlyCharges`
  - **Forward/backward fill** mantıklı olmaz (müşteriler bağımsız)

**🎯 Data Prep Expert Önerisi:**
TotalCharges NaN olan satırlar için **imputasyon formülü**:  
```python
TotalCharges = tenure × MonthlyCharges
```
Bu formül iş mantığına uygun çünkü toplam ücret = müşteri süresi × aylık ücrettir (yaklaşık olarak).

---

### 2. tenure ↔ TotalCharges Yüksek Korelasyon (r = 0.826)

**📊 Kritik Bulgu:**
tenure ve TotalCharges arasında **0.826 korelasyon** var. Bu çok güçlü bir pozitif ilişkidir.

**💼 İş Değeri Yorumu:**
Bu korelasyon **beklenen ve mantıklıdır** çünkü:
- **TotalCharges = tenure × MonthlyCharges** (yaklaşık)
- Müşteri ne kadar uzun süredir kalırsa, toplam ödediği ücret o kadar yüksek olur
- Bu ilişki **causality** (nedensellik) değil, **mathematical relationship** (matematiksel ilişki)

**🚨 Modelleme Riski - Multicollinearity:**
0.826 korelasyon **multicollinearity riski** yaratır:
- Model tenure'nin katsayısını doğru tahmin edemeyebilir
- tenure ve TotalCharges birbirinin etkisini "maskeleyebilir"
- Feature importance yanıltıcı olabilir

**🎯 Çözüm Önerileri:**

#### Seçenek 1: Değişken Seçimi (Recommended)
- **tenure'i kullan, TotalCharges'ı çıkar**
  - tenure daha fundamental (müşteri süresi doğrudan churn'ü etkiler)
  - TotalCharges derived variable (tenure'den türetilmiş)
  - VIF: tenure (6.33) < TotalCharges (8.09)

#### Seçenek 2: Feature Engineering
- **Yeni değişken:** `average_monthly_spending = TotalCharges / tenure`
- Bu değişken müşterinin ortalama aylık harcamasını gösterir
- Orijinal tenure ve TotalCharges çıkarılır

#### Seçenek 3: Regularization
- **Ridge Regression** veya **Lasso Regression** kullan
- Multicollinearity'yi cezalandırır
- Her iki değişken de modelde kalabilir

**🔬 Model Expert İçin Öneri:**
İlk modelde **tenure'i kullan, TotalCharges'ı çıkar**. Sonra alternatif modellerde `average_monthly_spending` feature'ını dene.

---

### 3. MonthlyCharges ↔ TotalCharges Orta-Yüksek Korelasyon (r = 0.651)

**📊 Kritik Bulgu:**
MonthlyCharges ve TotalCharges arasında **0.651 korelasyon** var.

**💼 İş Değeri Yorumu:**
Bu ilişki de **beklenen ve mantıklıdır**:
- Aylık ücreti yüksek olanların toplam ücreti de yüksek olur (eğer tenure benzer ise)
- Ancak tenure'nin etkisi daha dominant (r=0.826)

**🎯 Modelleme Stratejisi:**
0.651 korelasyon **orta seviyede** multicollinearity riski yaratır ama **kritik değil**. MonthlyCharges modelde kalabilir çünkü tenure ve TotalCharges'tan farklı bilgi taşır (fiyat segmenti).

---

### 4. VIF Analizi - Orta Seviye Multicollinearity

**📊 Kritik Bulgu:**
- **tenure**: VIF = 6.33 (orta)
- **TotalCharges**: VIF = 8.09 (orta)

**💼 İş Değeri Yorumu:**
VIF değerleri **5-10 aralığında** → Orta seviye multicollinearity. Kritik seviye (≥10) değil ama **izlenmeli**.

**📖 VIF Yorumlama Detayı:**
- **VIF = 6.33** → tenure'nin varyansının **%84'ü** (1 - 1/6.33) diğer değişkenlerle açıklanabiliyor
- **VIF = 8.09** → TotalCharges'ın varyansının **%88'i** diğer değişkenlerle açıklanabiliyor

**🎯 Öneriler:**
1. **tenure kullan, TotalCharges çıkar** → VIF problemi çözülür
2. Eğer her ikisi de kullanılacaksa:
   - **Regularization** (Ridge/Lasso) kullan
   - **Feature importance** dikkatle yorumla
   - **Coefficient stability** kontrol et (cross-validation ile)

---

### 5. Scatter Plot İçgörüleri

#### tenure vs TotalCharges
- **Güçlü lineer ilişki** görülüyor (r=0.826 doğrulanıyor)
- **Churn=Yes** müşterileri sol alt köşede yoğunlaşmış (düşük tenure, düşük TotalCharges)
- **Churn=No** müşterileri sağ üst köşede (yüksek tenure, yüksek TotalCharges)

**💡 İçgörü:** Uzun süredir kalan ve yüksek harcama yapan müşteriler sadık. Yeni ve düşük harcama yapanlar risk altında.

#### tenure vs MonthlyCharges
- **Zayıf pozitif ilişki** (r=0.248)
- Churn segmentleri arasında belirgin fark yok
- **Insight:** tenure uzun olsa bile MonthlyCharges yüksekse churn riski var (PHASE 3 bulgusuyla uyumlu)

#### MonthlyCharges vs TotalCharges
- **Orta güçlü pozitif ilişki** (r=0.651)
- Yüksek MonthlyCharges + düşük TotalCharges → Yeni müşteri + pahalı paket → Yüksek churn riski

---

## ⚠️ Risk / Dikkat Edilmesi Gereken Noktalar

### 1. tenure ↔ TotalCharges Yüksek Korelasyon
**Risk Seviyesi:** 🔴 Yüksek  
**Açıklama:** r = 0.826 → Multicollinearity riski. Model katsayıları yanıltıcı olabilir.  
**Öneri:** TotalCharges değişkenini modellemeden çıkar, alternatif olarak `average_monthly_spending` feature'ını kullan.

### 2. TotalCharges - 11 NaN Değer
**Risk Seviyesi:** 🟢 Düşük  
**Açıklama:** %0.16 NaN oranı çok düşük ama yine de imputasyon gerekli.  
**Öneri:** `TotalCharges = tenure × MonthlyCharges` formülü ile imputasyon yap.

### 3. VIF: tenure (6.33) ve TotalCharges (8.09)
**Risk Seviyesi:** 🟡 Orta  
**Açıklama:** Orta seviye multicollinearity. Kritik değil ama izlenmeli.  
**Öneri:** Değişken seçimi veya regularization stratejisi kullan.

---

## 🔁 Agent Etkileşim Notu

### Data Prep Expert İçin Öneriler

| Öncelik | Sorun | Kanıt | Öneri |
|---|---|---|---|
| 🔴 Yüksek | tenure ↔ TotalCharges yüksek korelasyon | r = 0.826 | TotalCharges değişkenini çıkar ve alternatif olarak `average_monthly_spending = TotalCharges / tenure` feature'ını oluştur. |
| 🔴 Yüksek | TotalCharges - 11 NaN değer | %0.16 NaN oranı | Imputasyon: `TotalCharges = tenure × MonthlyCharges` formülü ile doldur. |
| 🟡 Orta | VIF: tenure (6.33) ve TotalCharges (8.09) | Orta multicollinearity | Değişken seçimi stratejisi uygula (tenure kullan, TotalCharges çıkar) veya regularization (Ridge/Lasso) kullan. |

### Model Expert İçin Öneriler

| Öneri Tipi | Açıklama |
|---|---|
| **Feature Selection** | **Baseline model:** tenure, MonthlyCharges, SeniorCitizen kullan. TotalCharges çıkar. |
| **Alternative Model** | `average_monthly_spending` feature'ı oluştur ve modele ekle. |
| **Regularization** | Eğer TotalCharges modelde kalacaksa Ridge veya Lasso Regression kullan. |
| **VIF Monitoring** | Model train ettikten sonra coefficient stability kontrol et. |

---

## 📁 Kaydedilen Çıktılar

- ✅ **reports/csv/phase4_correlation_matrix.csv** - Korelasyon matrisi
- ✅ **reports/csv/phase4_vif_analysis.csv** - VIF analizi
- ✅ **reports/csv/phase4_data_prep_recommendations.csv** - Data Prep önerileri
- ✅ **4 adet grafik** (figures/ klasörü):
  - 1 correlation heatmap
  - 3 scatter plot (ikili ilişkiler)

---

## 🎯 Sonraki Adım

PHASE 5'te **data quality & anomaly detection** yapılacak:
- Eksik veri analizi (detaylı)
- Duplicate kontrolü
- Outlier tespiti (IQR, Z-score)
- Tutarsız kategori kontrolü
- Veri tipi kontrolleri
- Final data quality raporu

---

**Tarih:** 5 Mayıs 2026  
**Analiz Sorumlusu:** EDA Expert  
**Durum:** ✅ Tamamlandı
