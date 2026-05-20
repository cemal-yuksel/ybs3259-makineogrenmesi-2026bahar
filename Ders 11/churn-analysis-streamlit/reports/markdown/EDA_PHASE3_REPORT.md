# PHASE 3: BIVARIATE ANALYSIS - HEDEF DEĞİŞKEN İLİŞKİ ANALİZİ

## 📊 Yapılan Analiz

Bu aşamada hedef değişken (**Churn**) ile diğer değişkenler arasındaki ikili ilişkiler incelendi. Sayısal değişkenler için boxplot, violin plot ve t-test yapıldı. Kategorik değişkenler için çapraz tablolar, churn oranı karşılaştırmaları ve chi-square testleri gerçekleştirildi.

**Analiz Kapsamı:**
- 3 sayısal değişken vs Churn
- 16 kategorik değişken vs Churn (customerID hariç, TotalCharges dahil)
- **Toplam 38 grafik** oluşturuldu

---

## 🧠 Koddan Elde Edilen Bulgular

### 1. Sayısal Değişkenler vs Churn - İstatistiksel Karşılaştırma

| Değişken | Churn=No Ortalama | Churn=Yes Ortalama | Ortalama Farkı | T-Statistic | P-Value | Anlamlılık |
|---|---|---|---|---|---|---|
| **SeniorCitizen** | 0.13 | 0.25 | **+0.12** | -12.81 | < 0.001 | ✅ Çok güçlü |
| **tenure** | 37.57 ay | 17.98 ay | **-19.59 ay** | 31.58 | < 0.001 | ✅ Çok güçlü |
| **MonthlyCharges** | $61.27 | $74.44 | **+$13.17** | -16.54 | < 0.001 | ✅ Çok güçlü |

### 2. Kategorik Değişkenler vs Churn - En Kritik Bulgular

#### 🏆 EN GÜÇLÜ CHURN PREDİCTOR'LAR (Churn rate farkı > %30)

| Değişken | En Yüksek Churn Kategori | Churn % | En Düşük Churn Kategori | Churn % | Fark | Chi2 | P-Value |
|---|---|---|---|---|---|---|---|
| **Contract** | Month-to-month | **42.71%** | Two year | **2.83%** | **39.88%** | 1184.60 | < 0.001 |
| **InternetService** | Fiber optic | **41.89%** | No internet | **7.40%** | **34.49%** | 894.91 | < 0.001 |
| **OnlineSecurity** | No | **41.77%** | No internet service | **7.40%** | **34.37%** | 737.65 | < 0.001 |
| **TechSupport** | No | **41.64%** | No internet service | **7.40%** | **34.24%** | 714.91 | < 0.001 |
| **OnlineBackup** | No | **39.93%** | No internet service | **7.40%** | **32.53%** | 565.02 | < 0.001 |
| **DeviceProtection** | No | **39.13%** | No internet service | **7.40%** | **31.73%** | 528.64 | < 0.001 |
| **PaymentMethod** | Electronic check | **45.29%** | Credit card (auto) | **15.24%** | **30.05%** | 648.14 | < 0.001 |

#### 🔍 DİĞER ÖNEMLİ BULGULAR (Churn rate farkı %15-30)

| Değişken | En Yüksek Churn | Churn % | En Düşük Churn | Churn % | Fark |
|---|---|---|---|---|---|
| **StreamingMovies** | No | 33.68% | No internet service | 7.40% | 26.28% |
| **StreamingTV** | No | 33.52% | No internet service | 7.40% | 26.12% |
| **MultipleLines** | No | 28.33% | No phone service | 25.00% | 3.33% (düşük) |
| **PaperlessBilling** | Yes | 33.57% | No | 16.33% | 17.24% |
| **Dependents** | No | 31.28% | Yes | 15.46% | 15.82% |
| **Partner** | No | 32.96% | Yes | 19.66% | 13.30% |

---

## 💡 Analitik Yorum (YBS Uzmanı Perspektifi)

### 1. Sayısal Değişkenler - Derinlemesine Yorum

#### tenure (Müşteri Süresi) - EN GÜÇLÜ PREDİCTOR
**📊 Kritik Bulgu:**
- Churn eden müşteriler ortalama **17.98 ay** kalmış
- Churn etmeyen müşteriler ortalama **37.57 ay** kalmış
- **19.59 ay fark** (neredeyse 2 kat!)
- T-test: p < 0.001 → Çok güçlü istatistiksel fark

**💼 İş Değeri Yorumu:**
Bu bulgu **telekom sektörünün en bilinen gerçeğini** doğruluyor:
- **İlk 12-18 ay kritik risk periyodudur**
- Yeni müşteriler yüksek churn riskine sahiptir
- 3 yıl+ kalan müşteriler sadık segment oluşturur

**🎯 Operasyonel Aksiyon Önerileri:**
1. **İlk 6 ay boyunca** proaktif müşteri hizmetleri ve onboarding programı
2. **12-18 ay arası** özel retention kampanyaları
3. **24 ay sonra** loyalty rewards programı
4. Yeni müşteriler için **ilk 3 ay discount + 18 ay sonra renewal incentive** stratejisi

**🔬 Modelleme Etkisi:**
- Feature engineering: `tenure_group` (0-12, 13-24, 25-48, 49+)
- `is_new_customer` (tenure < 6 ay)
- `tenure_squared` (non-linear ilişki olabilir)
- Model en yüksek feature importance'ı tenure'den beklenir

#### MonthlyCharges (Aylık Ücret) - FİYAT DUYARLILIĞI
**📊 Kritik Bulgu:**
- Churn edenler ortalama **$74.44** ödüyor
- Churn etmeyenler ortalama **$61.27** ödüyor
- **$13.17 fark** (%21.5 daha yüksek)
- T-test: p < 0.001 → Çok güçlü istatistiksel fark

**💼 İş Değeri Yorumu:**
Yüksek fiyat segmenti churn'e daha yatkın. Bu durum:
- **Fiber optic** gibi premium hizmetlerin yüksek fiyatlı olması
- **Fiyat-değer algısı** uyumsuzluğu (müşteri beklediği değeri görmüyor)
- **Rekabetçi piyasa** (rakipler daha ucuz)
- **Ekonomik duyarlılık** (high spenders daha fazla alternatifleri değerlendiriyor)

**🎯 Operasyonel Aksiyon Önerileri:**
1. **$70+ fiyat segmentine** value-added services sunma (ücretsiz premium support, ekstra GB vb.)
2. **Dynamic pricing** stratejisi - tenure bazlı indirimler
3. **Bundle discount** kampanyaları (yüksek fiyat → daha fazla hizmet)
4. **Competitor price monitoring** ve proaktif counter-offer

**🔬 Modelleme Etkisi:**
- Feature engineering: `price_per_tenure_month` (MonthlyCharges / tenure)
- `is_high_spender` (MonthlyCharges > $80)
- `price_value_ratio` (TotalCharges / number of services)

#### SeniorCitizen (Yaşlı Müşteri) - DEMOGRAFIK RISK
**📊 Kritik Bulgu:**
- Churn eden müşterilerin **%25'i yaşlı**
- Churn etmeyen müşterilerin **%13'ü yaşlı**
- **%12 fark** (neredeyse 2 kat)
- T-test: p < 0.001 → Çok güçlü istatistiksel fark

**💼 İş Değeri Yorumu:**
Yaşlı müşteriler daha fazla churn ediyor. Olası sebepler:
- **Teknik sorunlar** ve yardım ihtiyacı (dijital okuryazarlık)
- **Sabit gelir** nedeniyle fiyat duyarlılığı
- **Basit hizmet ihtiyacı** (premium paketlere ihtiyaç yok)
- **Rekabetçi teklifler** (diğer operatörler senior discount sunuyor olabilir)

**🎯 Operasyonel Aksiyon Önerileri:**
1. **Senior support line** - özel müşteri hizmetleri ekibi
2. **Simplified pricing plans** - karmaşık paketler yerine basit, şeffaf fiyatlandırma
3. **Senior discount programs** - yaşlılara özel indirimler
4. **Proactive tech support** - ayda bir kontrol araması

---

### 2. Kategorik Değişkenler - Derinlemesine Yorum

#### Contract (Sözleşme Tipi) - MUTLAKİYETLE EN GÜÇLÜ PREDİCTOR
**📊 Kritik Bulgu:**
- **Month-to-month**: **%42.71 churn** 🔴
- **One year**: **%11.27 churn** 🟡
- **Two year**: **%2.83 churn** 🟢
- Chi-square: 1184.60, p < 0.001
- **%39.88 fark** → Modelin en güçlü değişkeni olacak

**💼 İş Değeri Yorumu:**
Bu bulgu **sözleşme bağlılığının churn üzerinde baskın etkisini** gösteriyor:
- Aylık sözleşme → Düşük bağlılık, yüksek esneklik, yüksek churn
- 1 yıllık sözleşme → Orta bağlılık, makul churn
- 2 yıllık sözleşme → Yüksek bağlılık, çok düşük churn

**🚨 Kritik İçgörü:**  
Month-to-month müşterilerin **yarıya yakını** churn ediyor. Bu segment **en riskli segment**.

**🎯 Operasyonel Aksiyon Önerileri:**
1. **Aggressive incentive** - Month-to-month'tan 1 yıllığa geçiş için discount (örn: 2 ay bedava)
2. **Auto-renewal bonus** - 2 yıllık sözleşme yenileme bonusu
3. **Early termination fee waiver** - Upgrade için erken çıkış cezası kaldırma
4. **Contract expiry tracking** - Sözleşme bitiş tarihi yaklaşan müşterilere proaktif kampanya

**🔬 Modelleme Etkisi:**
- Bu değişken **en yüksek feature importance**a sahip olacak (tenure ile birlikte)
- Feature engineering: `contract_remaining_months` (sözleşmenin kalan süresi)
- `is_at_risk_contract` (month-to-month = 1)

#### InternetService (İnternet Hizmeti Tipi) - FİBER OPTIC RİSKİ
**📊 Kritik Bulgu:**
- **Fiber optic**: **%41.89 churn** 🔴
- **DSL**: **%18.96 churn** 🟡
- **No internet**: **%7.40 churn** 🟢
- Chi-square: 894.91, p < 0.001
- **%34.49 fark**

**💼 İş Değeri Yorumu:**
Fiber optic müşterileri DSL'den **2.2 kat daha fazla churn** ediyor! Bu şaşırtıcı bulgu:
- Fiber optic **en pahalı** hizmet → Fiyat duyarlılığı
- Fiber optic **yüksek beklenti** → Hizmet kalitesi şikayetleri
- Fiber optic **rekabetçi pazar** → Rakipler de fiber sunuyor
- Fiber optic müşterileri **tech-savvy** → Alternatifleri araştırıyor

**🚨 Stratejik Risk:**  
Fiber optic premium hizmet ancak en riskli segment. **Paradoks!**

**🎯 Operasyonel Aksiyon Önerileri:**
1. **Fiber quality monitoring** - Hizmet kalitesi şikayetlerini proaktif çözme
2. **Fiber customer retention team** - Özel takip ekibi
3. **Value-added services** - Fiber müşterilerine ekstra hizmetler (cloud storage, security)
4. **Competitive pricing** - Rakip fiyatlarını izleme ve counter-offer

#### PaymentMethod (Ödeme Yöntemi) - ELECTRONIC CHECK RİSKİ
**📊 Kritik Bulgu:**
- **Electronic check**: **%45.29 churn** 🔴
- **Mailed check**: **%19.11 churn** 🟡
- **Bank transfer (auto)**: **%16.71 churn** 🟢
- **Credit card (auto)**: **%15.24 churn** 🟢
- **%30.05 fark**

**💼 İş Değeri Yorumu:**
Electronic check kullanıcıları **3 kat daha fazla churn** ediyor. Olası sebepler:
- **Manuel ödeme** → Her ay bilinçli ödeme kararı → Churn fırsatı
- **Ödeme başarısızlığı** riski → Hesap kapatma
- **Düşük engagement** → Otomatik ödeme yapmayanlar daha az bağlı
- **Finansal istikrarsızlık** göstergesi olabilir

**🔬 Davranışsal İçgörü:**  
Otomatik ödeme yapanlar (credit card, bank transfer) **daha sadık**. Çünkü:
- **Cognitive ease** - Her ay yeniden karar vermiyorlar
- **Status quo bias** - Değiştirmek ekstra effort gerektirir

**🎯 Operasyonel Aksiyon Önerileri:**
1. **Auto-pay incentive** - Otomatik ödemeye geçenlere discount
2. **Payment failure prevention** - Ödeme başarısız olunca hemen hatırlatma + alternatif sunma
3. **Electronic check risk scoring** - Bu segment için özel retention campaign

#### Hizmet Değişkenleri (OnlineSecurity, TechSupport vb.) - HİZMET EKSİKLİĞİ RİSKİ
**📊 Kritik Pattern:**
Tüm ek hizmetlerde aynı pattern görülüyor:
- **Hizmet yok (No)**: %35-42 churn 🔴
- **Hizmet var (Yes)**: %15-25 churn 🟡
- **No internet service**: %7.40 churn 🟢

**💼 İş Değeri Yorumu:**
İnternet hizmeti olan ama **ek koruma/destek hizmetleri almayan** müşteriler yüksek risk altında. Bu:
- **Value perception** sorunu - Yalnız internet yeterli görülmüyor
- **Competitor attractiveness** - Rakipler bundle offer sunuyor
- **Lack of stickiness** - Tek hizmet → kolay bırakma

**🎯 Operasyonel Aksiyon Önerileri:**
1. **Cross-sell campaign** - İnternet varsa + OnlineSecurity + TechSupport bundle
2. **First 3 months free** - Ek hizmetleri deneme fırsatı
3. **Risk segment tagging** - "Fiber optic + No security" → En riskli segment

---

## ⚠️ Risk / Dikkat Edilmesi Gereken Noktalar

### 1. tenure - Yeni Müşteri Riski
**Risk Seviyesi:** 🔴 Kritik  
**Açıklama:** Ortalama 17.98 ay kalan müşteriler churn ediyor. İlk 12-18 ay kritik periyot.  
**Öneri:** Yeni müşteri onboarding programı ve ilk 6 ay proaktif takip zorunlu.

### 2. Contract - Month-to-Month Dominosu
**Risk Seviyesi:** 🔴 Kritik  
**Açıklama:** Month-to-month müşterilerin %42.71'i churn ediyor. Bu segment kontrol altına alınmazsa revenue kaybı devam eder.  
**Öneri:** Month-to-month'tan yıllık sözleşmeye geçiş incentive'leri agresif şekilde uygulanmalı.

### 3. InternetService - Fiber Optic Paradoksu
**Risk Seviyesi:** 🔴 Yüksek  
**Açıklama:** En premium hizmet (Fiber optic) en yüksek churn'e sahip (%41.89). **Stratejik sorun işareti**.  
**Öneri:** Fiber müşteri deneyimi audit edilmeli, hizmet kalitesi ve fiyat-değer dengesi gözden geçirilmelidir.

### 4. PaymentMethod - Electronic Check Kırılganlığı
**Risk Seviyesi:** 🟡 Orta  
**Açıklama:** Electronic check kullananların %45.29'u churn ediyor.  
**Öneri:** Otomatik ödeme geçiş kampanyası + ödeme başarısızlığı proaktif yönetimi.

### 5. MonthlyCharges - Fiyat Duyarlılığı
**Risk Seviyesi:** 🟡 Orta  
**Açıklama:** Yüksek ücret ödeyen segment churn'e daha yatkın ($74.44 vs $61.27).  
**Öneri:** $70+ segment için value-added services ve dynamic pricing stratejisi.

### 6. TotalCharges - Veri Kalitesi Sorunu (Devam Ediyor)
**Risk Seviyesi:** 🔴 Yüksek  
**Açıklama:** TotalCharges kategorik değişken gibi işlendi, chi-square testi anlamlı çıkmadı (p=0.55). Ancak bu değişken sayısal olmalı.  
**Öneri:** Data Prep Expert bu değişkeni numeric'e çevirmeli ve PHASE 4'te korelasyon analizi tekrarlanmalıdır.

---

## 🔁 Agent Etkileşim Notu

### Data Prep Expert İçin Öneriler

| Öncelik | Sorun | Kanıt | Öneri |
|---|---|---|---|
| 🔴 Yüksek | Contract - Güçlü predictor | Churn rate farkı %39.88 (p<0.001) | Feature engineering: `contract_remaining_months`, `is_at_risk_contract` (month-to-month flag) |
| 🔴 Yüksek | InternetService - Güçlü predictor | Churn rate farkı %34.49 (p<0.001) | Feature engineering: `is_fiber_customer`, `internet_service_score`, InternetService × Contract interaction |
| 🔴 Yüksek | PaymentMethod - Güçlü predictor | Churn rate farkı %30.05 (p<0.001) | Feature engineering: `is_auto_pay`, `is_electronic_check_risk` |
| 🔴 Yüksek | OnlineSecurity, TechSupport - Güçlü predictor | Churn rate farkı %34+ (p<0.001) | Feature engineering: `total_services_count`, `has_protection_services`, `service_bundle_score` |
| 🔴 Yüksek | TotalCharges - Veri tipi hatası | Chi-square testi anlamlı değil (p=0.55) | Numeric dönüşüm yapılmalı, PHASE 4'te korelasyon analizi tekrarlanmalıdır |
| 🟡 Orta | tenure - Feature engineering fırsatı | Ortalama fark 19.59 ay (p<0.001) | Feature engineering: `tenure_group`, `is_new_customer`, `tenure_squared` |
| 🟡 Orta | MonthlyCharges - Feature engineering fırsatı | Ortalama fark $13.17 (p<0.001) | Feature engineering: `price_per_tenure`, `is_high_spender`, `price_value_ratio` |

### Feature Engineering Expert İçin Öneriler

| Öneri Tipi | Önerilen Feature | Açıklama |
|---|---|---|
| **Interaction Features** | `Contract × InternetService` | Month-to-month + Fiber optic = En riskli segment |
| **Interaction Features** | `tenure × MonthlyCharges` | Yeni müşteri + yüksek fiyat = Çift risk |
| **Aggregation Features** | `total_services_count` | PhoneService + InternetService + ek hizmetler sayısı |
| **Binary Risk Flags** | `is_high_risk_customer` | Month-to-month + Fiber + Electronic check + tenure<12 |
| **Ratio Features** | `price_per_service` | MonthlyCharges / total_services_count |
| **Temporal Features** | `contract_expiry_soon` | Sözleşme bitiş tarihi < 3 ay |

---

## 📁 Kaydedilen Çıktılar

- ✅ **reports/csv/phase3_numeric_vs_churn.csv** - Sayısal değişken vs Churn istatistikleri
- ✅ **reports/csv/phase3_categorical_vs_churn.csv** - Kategorik değişken vs Churn özeti
- ✅ **reports/csv/phase3_data_prep_recommendations.csv** - Data Prep önerileri
- ✅ **38 adet grafik** (figures/ klasörü):
  - 3 boxplot (sayısal vs Churn)
  - 3 violin plot (sayısal vs Churn)
  - 16 grouped bar chart (kategorik vs Churn)
  - 16 churn rate bar chart (kategorik bazlı churn oranları)

---

## 🎯 Sonraki Adım

PHASE 4'te **multivariate analysis** yapılacak:
- Sayısal değişkenler arası korelasyon matrisi
- VIF (Variance Inflation Factor) - Multicollinearity kontrolü
- TotalCharges değişkeninin numeric'e çevrilmesi ve yeniden analiz
- Interaction effects (örn: Contract × InternetService)
- Pairwise scatter matrix (feature relationships)

---

**Tarih:** 5 Mayıs 2026  
**Analiz Sorumlusu:** EDA Expert  
**Durum:** ✅ Tamamlandı
