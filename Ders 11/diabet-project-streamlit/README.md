# 🏥 Diabetes Prediction System

**HCI Odaklı Profesyonel ML Deployment Uygulaması**

[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io/)
[![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Scikit-Learn](https://img.shields.io/badge/scikit--learn-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white)](https://scikit-learn.org/)

---

## 📊 Proje Özeti

Bu proje, **Deployment Expert** agent'ı tarafından geliştirilmiş, HCI (Human-Computer Interaction) ilkeleri ve **Shneiderman'ın 8 Altın Kuralı**'na uygun olarak tasarlanmış profesyonel bir makine öğrenmesi deployment uygulamasıdır.

### 🎯 Amaç
Kişilerin sağlık verilerine göre diyabet riskini tahmin etmek ve bu tahmini kullanıcı dostu, güvenilir ve şeffaf bir arayüzde sunmak.

### 🤖 Model
- **Algoritma:** Random Forest Classifier
- **Performans:** F1-Score 0.77, Accuracy %77.3, ROC-AUC 0.83
- **Eğitim:** 18 farklı model karşılaştırması sonucu seçildi
- **Veri:** Pima Indians Diabetes Database (768 kayıt)

---

## 🚀 Kurulum ve Çalıştırma

### 1. Gereksinimleri Yükleyin

```bash
pip install -r requirements.txt
```

### 2. Uygulamayı Başlatın

```bash
streamlit run app.py
```

### 3. Tarayıcıda Açın

Uygulama otomatik olarak tarayıcınızda açılacaktır:
```
http://localhost:8501
```

---

## 📁 Proje Yapısı

```
diabet-project/
│
├── app.py                          # Ana Streamlit uygulaması
├── requirements.txt                # Python bağımlılıkları
├── README.md                       # Bu dosya
│
├── pages/                          # Streamlit sayfaları (multi-page app)
│   ├── __init__.py
│   ├── home.py                     # Ana sayfa / Yönetici özeti
│   ├── single_prediction.py       # Tekil tahmin sayfası
│   ├── batch_prediction.py        # Toplu tahmin (CSV upload)
│   ├── model_performance.py       # Model performans grafikleri
│   ├── model_info.py              # Model bilgisi ve sınırlamalar
│   ├── monitoring.py              # Sistem izleme ve loglar
│   └── help_page.py               # Yardım ve SSS
│
├── models/                         # Eğitilmiş modeller
│   ├── final_model.pkl             # Random Forest model
│   └── preprocessing_pipeline.pkl  # Veri işleme pipeline'ı
│
├── data/                           # Veri dosyaları
│   ├── raw/                        # Ham veri
│   ├── processed/                  # İşlenmiş veri
│   └── model_ready/                # Model-ready veri (train/test split)
│
├── figures/                        # Performans grafikleri (HTML/PNG)
│   ├── model_phase7_*.html
│   ├── model_phase10_*.html
│   └── ...
│
├── reports/                        # Raporlar ve dokümantasyon
│   ├── markdown/
│   │   ├── EDA_FINAL_REPORT.md
│   │   ├── DATAPREP_SUMMARY.md
│   │   ├── MODEL_EXPERT_FINAL_REPORT.md
│   │   └── MODEL_EXPERT_HANDOFF_REPORT.md
│   └── csv/
│
├── logs/                           # Tahmin logları (otomatik oluşturulur)
│   └── prediction_log.csv
│
└── scripts/                        # Veri hazırlama ve model eğitim scriptleri
    ├── data_preparation.py
    ├── model_training.py
    └── ...
```

---

## 📑 Uygulama Sayfaları

### 🏠 Ana Sayfa
- Yönetici özeti ve genel bilgilendirme
- Model performans göstergeleri
- Hızlı erişim butonları
- Sistem mimarisi açıklaması

### 🔮 Tekil Tahmin
- Bireysel hasta bilgileriyle tahmin
- Form validasyonu ve hata önleme
- Güven skoru ve risk değerlendirmesi
- Örnek veri denemesi

### 📊 Toplu Tahmin
- CSV dosyası yükleme
- Batch prediction (çoklu kayıt)
- Otomatik kolon kontrolü
- Sonuçları CSV olarak indirme

### 📈 Model Performansı
- 18 modelin karşılaştırmalı analizi
- İnteraktif grafikler (Plotly)
- Confusion matrix yorumu
- ROC curve

### ℹ️ Model Bilgisi
- Model kimlik kartı
- Seçim gerekçesi
- Feature açıklamaları
- Sınırlamalar ve riskler

### 📡 Monitoring
- Tahmin istatistikleri
- Zaman serisi analizi
- Log dosyası görüntüleme/indirme
- Sistem durumu

### ❓ Yardım
- Kullanım kılavuzu
- Input alanları açıklamaları
- Sık sorulan sorular (SSS)
- İletişim bilgileri

---

## 🎨 HCI Tasarım Prensipleri

Bu uygulama aşağıdaki HCI ilkeleri doğrultusunda tasarlanmıştır:

### Shneiderman'ın 8 Altın Kuralı

1. **Tutarlılık Sağla:** Tüm sayfalarda aynı renk paleti, buton stilleri ve terminoloji
2. **Kısayollar Sun:** Hızlı erişim butonları, örnek veri yükleme, toplu işlem
3. **Bilgilendirici Geri Bildirim:** Success/warning/error mesajları, progress bar, spinner
4. **Tamamlanmış Eylemler:** Net başlangıç-ortadönüş akışı
5. **Hataları Önle:** Input validasyonu, min/max değerler, kolon kontrolü
6. **Geri Almayı Kolaylaştır:** Temizle butonu, form reset, yeni tahmin
7. **Kullanıcıya Kontrol Hissi Ver:** Tab menüleri, genişletilebilir bölümler, indirme opsiyonları
8. **Düşük Bellek Yükü:** Sidebar özeti, tooltip açıklamalar, adım adım kılavuz

### Nielsen Kullanılabilirlik İlkeleri

- Sistem durumunun görünürlüğü (sidebar model bilgisi)
- Gerçek dünya ile uyum (tıbbi terminoloji)
- Kullanıcı kontrolü (sayfa navigasyonu)
- Tutarlılık ve standartlar (profesyonel renk paleti)
- Hata önleme (form validasyonu)
- Hatırlama yerine tanıma (ikon kullanımı)
- Estetik ve minimalist tasarım (temiz, geniş boşluklar)
- Yardım ve dokümantasyon (yardım sayfası)

---

## 🔒 Güvenlik ve Etik

### ⚠️ Kritik Uyarılar

1. **Bu sistem tıbbi teşhis koymaz**
   - Yalnızca karar destek aracıdır
   - Uzman değerlendirmesiyle birlikte kullanılmalıdır

2. **False Negative Riski (%20)**
   - Diyabetli kişilerin bir kısmı kaçırılabilir
   - Düşük güvenli tahminler özellikle dikkatle yorumlanmalıdır

3. **Veri Gizliliği**
   - Kullanıcı verileri logs/ klasöründe saklanır
   - Üretim ortamında GDPR/KVKK uyumu gereklidir

4. **Model Sınırlamaları**
   - Yalnızca 768 kayıt ile eğitildi
   - Farklı demografik gruplarda performans değişebilir
   - Düzenli retraining gerektirir

---

## 📊 Model Performans Metrikleri

| Metrik | Değer |
|--------|-------|
| **Test F1-Score** | 0.7700 |
| **Test Accuracy** | 77.3% |
| **ROC-AUC** | 0.8306 |
| **Precision** | 0.69 |
| **Recall** | 0.63 |
| **CV Mean** | 0.7547 |
| **CV Std** | 0.0202 |
| **Baseline İyileşme** | +50.6% |

### Confusion Matrix

```
              Predicted 0  Predicted 1
Actual 0 (TN)      85           15
Actual 1 (FN)      20           34
```

- **True Negatives:** 85
- **True Positives:** 34
- **False Positives:** 15
- **False Negatives:** 20 ⚠️

---

## 🔄 Agent Zinciri

Bu proje agentik bir pipeline'ın sonucudur:

```
EDA Expert → DataPrep Expert → Model Expert → Deployment Expert
```

### Deployment Expert Sorumlulukları

1. ✅ Model Expert'ten final model ve pipeline'ı devraldı
2. ✅ Streamlit ile profesyonel multi-page app oluşturdu
3. ✅ HCI ilkeleri ve Shneiderman'ın 8 Altın Kuralı'nı uyguladı
4. ✅ Input validasyonu ve hata önleme mekanizmaları kurdu
5. ✅ Güven skoru ve risk değerlendirmesi ekledi
6. ✅ Batch prediction (CSV upload) özelliği geliştirdi
7. ✅ Monitoring ve loglama altyapısını hazırladı
8. ✅ Kapsamlı dokümantasyon ve yardım sayfası oluşturdu

---

## 📝 Kullanım Örnekleri

### Tekil Tahmin

```python
# Form doldurun:
Pregnancies: 6
Glucose: 148 mg/dL
BloodPressure: 72 mm Hg
BMI: 33.6
DiabetesPedigreeFunction: 0.627
Age: 50

# Tahmin Yap butonuna tıklayın
# Sonuç: Diyabet Riski Tespit Edildi (%85.2 güven)
```

### Toplu Tahmin (CSV)

```csv
Pregnancies,Glucose,BloodPressure,BMI,DiabetesPedigreeFunction,Age
6,148,72,33.6,0.627,50
1,85,66,26.6,0.351,31
8,183,64,23.3,0.672,32
```

CSV'yi yükleyin → Tahmin Yap → Sonuçları indirin

---

## 🛠️ Teknik Detaylar

### Kullanılan Teknolojiler

- **Frontend:** Streamlit (multi-page app)
- **Backend:** Python 3.9+
- **ML Framework:** scikit-learn
- **Visualization:** Plotly
- **Model:** Random Forest Classifier
- **Preprocessing:** StandardScaler, Yeo-Johnson, Feature Engineering
- **Validation:** 5-Fold Stratified Cross-Validation

### Veri İşleme Pipeline

1. Gizli eksik veri temizleme (0 → NaN → Median imputation)
2. Değişken çıkarma (Insulin, SkinThickness)
3. Outlier yönetimi (Winsorization)
4. Çarpıklık dönüşümü (Yeo-Johnson)
5. Feature engineering (8 yeni feature)
6. Scaling (StandardScaler)
7. Stratified train-test split (80-20)

---

## 🚀 Gelecekteki İyileştirmeler

- [ ] Threshold optimizasyonu (FN oranını azaltma)
- [ ] SHAP/LIME ile model yorumlanabilirliği
- [ ] Feature importance gösterimi
- [ ] Gerçek zamanlı drift detection
- [ ] Otomatik retraining pipeline'ı
- [ ] Kullanıcı authentication sistemi
- [ ] Database entegrasyonu (log verisi için)
- [ ] REST API endpoint'leri
- [ ] Docker containerization
- [ ] CI/CD pipeline'ı

---

## 📞 İletişim ve Destek

**Proje Sahibi:** Deployment Expert (Agentik AI)  
**Model Versiyonu:** 1.0  
**Son Güncelleme:** 5 Mayıs 2026

**Not:** Bu proje eğitim ve araştırma amaçlıdır. Klinik kullanım için uygun regulatory onaylar alınmalıdır.

---

## 📄 Lisans

Bu proje eğitim amaçlı geliştirilmiştir.

---

## 🙏 Teşekkürler

- **EDA Expert:** Kapsamlı veri analizi ve öneriler
- **DataPrep Expert:** Profesyonel veri hazırlama pipeline'ı
- **Model Expert:** 18 model karşılaştırması ve final model seçimi
- **HCI İlkeleri:** Shneiderman, Nielsen, Don Norman

---

**🏥 Sağlığınız Önemlidir - Düzenli Sağlık Kontrolleri İhmal Etmeyin! 🏥**
