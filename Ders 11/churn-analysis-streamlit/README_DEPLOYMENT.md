# 🎯 Churn Risk Değerlendirme Platformu - Deployment Kılavuzu

## 📋 Genel Bakış

Bu uygulama, telekom müşterilerinin churn (kayıp) riskini değerlendirmek için geliştirilmiş kullanıcı dostu bir Wizard arayüzüdür. Apple'ın Bento Grid tasarım diliyle modern, görkemli ve profesyonel bir kullanıcı deneyimi sunar.

### ✨ Özellikler

- 🎨 **Apple Bento Grid Tasarımı**: Modern, glassmorphism efektleri, smooth transitions
- 🧭 **Wizard Yaklaşımı**: 5 adımlı kullanıcı dostu akış
- 🎯 **Akıllı Tahmin**: Calibrated Classifier (F1: 0.7917, ROC-AUC: 0.8404)
- 📊 **Risk Analizi**: Detaylı risk faktörleri ve aksiyon önerileri
- 💰 **İş Etkisi**: ROI hesaplaması ve maliyet analizi
- 📥 **Rapor İndirme**: Tahmin sonuçlarını TXT formatında indirme
- 🔄 **Session Management**: Geri alma, temizleme, form durumu saklama

### 🏆 HCI İlkeleri

Uygulama **Shneiderman'ın 8 Altın Kuralı**'na göre tasarlanmıştır:

1. ✅ **Tutarlılık**: Tüm sayfalarda aynı kart yapısı, renk paleti, tipografi
2. ✅ **Kısayollar**: Progress bar ile hızlı navigasyon
3. ✅ **Bilgilendirici Geri Bildirim**: Her adımda net durum göstergesi
4. ✅ **Tamamlanmış Eylemler**: Başlangıç → Veri → Tahmin → Sonuç → Aksiyon akışı
5. ✅ **Hata Önleme**: Input validation, zorunlu alan kontrolü
6. ✅ **Geri Alma**: Her adımda "Geri" butonu, "Baştan Başla" seçeneği
7. ✅ **Kontrol Hissi**: Kullanıcı her adımda kontrolde hisseder
8. ✅ **Bellek Yükü Azaltma**: Progress bar, adım göstergesi, tooltip'ler

---

## 🚀 Kurulum

### Gereksinimler

- Python 3.8 veya üzeri
- pip (Python paket yöneticisi)

### Adım 1: Bağımlılıkları Yükle

```bash
pip install -r requirements.txt
```

### Adım 2: Model Dosyalarını Kontrol Et

Aşağıdaki dosyaların `models/` klasöründe olduğundan emin olun:

- `final_model.pkl` (Calibrated Classifier modeli)
- `preprocessing_pipeline.pkl` (Veri önişleme pipeline'ı)

### Adım 3: Uygulamayı Çalıştır

```bash
streamlit run app.py
```

Uygulama varsayılan olarak `http://localhost:8501` adresinde açılacaktır.

---

## 📱 Kullanım Kılavuzu

### Wizard Adımları

#### **Adım 1: Müşteri Profili** 👤
- Cinsiyet
- Yaşlı vatandaş durumu (65+)
- Partner durumu
- Bakmakla yükümlü kişi durumu
- Müşteri süresi (ay)

#### **Adım 2: Hizmet Paketi** 📱
- Telefon hizmetleri (tek/çoklu hat)
- İnternet hizmeti (DSL/Fiber/Yok)
- Ek hizmetler:
  - Online güvenlik
  - Online yedekleme
  - Cihaz koruma
  - Teknik destek
  - TV streaming
  - Film streaming

#### **Adım 3: Sözleşme & Ödeme** 📄
- Sözleşme tipi (Aylık/1 Yıl/2 Yıl)
- Ödeme yöntemi (E-çek, Posta, Otomatik transfer, Kredi kartı)
- Kağıtsız fatura tercihi
- Aylık ücret
- Toplam ödeme (otomatik hesaplama)

#### **Adım 4: Risk Değerlendirmesi** 🎯
- Risk seviyesi (Düşük/Orta/Yüksek)
- Churn olasılığı (%)
- Güven seviyesi
- Top 3 risk faktörü analizi

#### **Adım 5: Aksiyon Önerileri** 💡
- Kişiselleştirilmiş öneriler
- Her önerinin risk azaltma etkisi (%)
- İş etkisi analizi (Churn maliyeti vs Retention maliyeti)
- Rapor indirme

---

## 🎨 Tasarım Sistemi

### Renk Paleti (Apple-Inspired)

```python
PRIMARY: #007AFF     # Apple Blue
SECONDARY: #34C759   # Apple Green
DANGER: #FF3B30      # Apple Red
WARNING: #FF9500     # Apple Orange
PURPLE: #AF52DE      # Apple Purple
TEAL: #5AC8FA        # Apple Teal
```

### Tipografi

- **Font Family**: -apple-system, BlinkMacSystemFont, 'Segoe UI'
- **Başlıklar**: 
  - H1: 52px, Font-weight: 800
  - H2: 36px, Font-weight: 700
  - H3: 24px, Font-weight: 700
- **Paragraf**: 17px, Line-height: 1.6

### Card Yapısı

- **Hero Card**: Glassmorphism efekti, backdrop-filter blur(20px)
- **Bento Card**: 24px border-radius, smooth shadow transitions
- **Metric Card**: Center aligned, hover efekti

---

## 📊 Model Bilgisi

### Final Model

- **Model Tipi**: Calibrated Classifier
- **Test F1-Score**: 0.7917 (Weighted Average)
- **ROC-AUC**: 0.8404 (Excellent discrimination)
- **Recall**: 0.8020 (Churn eden müşterilerin %80'ini yakalıyoruz)
- **Precision**: 0.7908
- **CV Kararlılığı**: 0.7941 ± 0.0115
- **Overfitting Riski**: 0.0073 (Çok düşük)

### İş Etkisi

- **False Negative (187)**: $561,000 maliyet (LTV kaybı)
- **False Positive (91)**: $4,550 maliyet (gereksiz kampanya)
- **Toplam Hata Maliyeti**: $565,550

### Preprocessing Pipeline

1. **Missing Value**: TotalCharges 11 NaN impute (tenure × MonthlyCharges)
2. **Encoding**: 
   - Binary: Label Encoding
   - Multi-class: One-Hot Encoding (drop_first=True)
3. **Scaling**: StandardScaler (train fit, train+test transform)
4. **Feature Engineering**: 10 yeni feature
5. **Stratified Split**: 80-20, target dağılımı korundu

---

## 🔧 Yapılandırma

### Streamlit Config (Opsiyonel)

`.streamlit/config.toml` dosyası oluşturabilirsiniz:

```toml
[theme]
primaryColor = "#007AFF"
backgroundColor = "#F5F5F7"
secondaryBackgroundColor = "#FFFFFF"
textColor = "#1D1D1F"
font = "sans serif"

[server]
port = 8501
enableCORS = false
```

---

## 📂 Dosya Yapısı

```
churn-analysis/
├── app.py                          # Ana Streamlit uygulaması
├── requirements.txt                 # Python bağımlılıkları
├── README_DEPLOYMENT.md            # Bu dosya
├── models/
│   ├── final_model.pkl             # Trained model
│   └── preprocessing_pipeline.pkl  # Preprocessing pipeline
├── figures/                         # Model performans grafikleri
├── reports/
│   ├── csv/                        # CSV raporları
│   └── markdown/                   # Markdown raporları
└── data/
    ├── raw/                        # Ham veri
    ├── processed/                  # İşlenmiş veri
    └── model_ready/                # Model-ready veri
```

---

## 🛡️ Güvenlik ve Etik Notlar

### ⚠️ Önemli Uyarılar

1. **Model Kararı Final Değildir**: Bu sistem yalnızca karar destek aracıdır. Kritik iş kararlarında uzman değerlendirmesi gereklidir.

2. **Düşük Güvenli Tahminler**: Churn olasılığı %40-60 arasında olan tahminlerde özellikle dikkatli olun.

3. **Veri Gizliliği**: Kullanıcı verileri loglanıyorsa GDPR/KVKK uyumluluğu sağlanmalıdır.

4. **Model Drift**: Üretim ortamında düzenli model performans izleme gereklidir.

5. **Bias Kontrolü**: Model eğitiminde kullanılan veri setindeki olası bias'ları göz önünde bulundurun.

---

## 📈 Monitoring (Gelecek Versiyon)

### Loglama

Şu anda tahmin geçmişi session state'te tutulmaktadır. Üretim ortamında:

- Prediction log dosyası (`logs/prediction_log.csv`)
- Timestamp, input data, prediction, probability
- Model version tracking
- Error logging

### İzlenecek Metrikler

- Günlük/haftalık tahmin sayısı
- Ortalama churn olasılığı
- Confidence distribution
- Düşük güvenilirlik oranı (drift göstergesi)

---

## 🆘 Sorun Giderme

### Problem: Model yüklenmiyor

**Çözüm**: 
```bash
# Model dosyalarını kontrol edin
ls models/final_model.pkl
ls models/preprocessing_pipeline.pkl
```

### Problem: Paket hatası

**Çözüm**:
```bash
# Tüm paketleri yeniden yükleyin
pip install -r requirements.txt --upgrade
```

### Problem: Streamlit çalışmıyor

**Çözüm**:
```bash
# Streamlit'i yeniden yükleyin
pip uninstall streamlit
pip install streamlit>=1.28.0
```

### Problem: Glassmorphism efektleri görünmüyor

**Çözüm**: 
- Modern tarayıcı kullanın (Chrome 76+, Safari 14+, Firefox 103+)
- `backdrop-filter` desteği gereklidir

---

## 🔄 Versiyon Geçmişi

### v1.0.0 (11 Mayıs 2026)
- ✨ İlk deployment
- 🎨 Apple Bento Grid tasarımı
- 🧭 5 adımlı Wizard akışı
- 📊 Risk analizi ve aksiyon önerileri
- 📥 Rapor indirme özelliği
- 🏆 HCI ilkeleri tam uyum

---

## 📞 İletişim ve Destek

Bu proje **Model Expert** çıktılarını kullanarak **Deployment Expert** tarafından geliştirilmiştir.

### Sonraki Adımlar

1. **Monitoring Expert**: Canlı ortam performans izleme
2. **A/B Testing**: Farklı UI varyantlarını test etme
3. **API Integration**: REST API ile entegrasyon
4. **Batch Processing**: CSV ile toplu tahmin (gelecek özellik)

---

## 📝 Lisans

Bu proje eğitim amaçlıdır ve Makine Öğrenmesi dersi kapsamında geliştirilmiştir.

---

**🎯 İyi Tahminler!**
