# 🎯 MAKİNE ÖĞRENMESİ - DERS 02

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║   ██████╗ ███████╗██████╗ ███████╗     ██████╗ ██████╗                      ║
║   ██╔══██╗██╔════╝██╔══██╗██╔════╝    ██╔═████╗╚════██╗                     ║
║   ██║  ██║█████╗  ██████╔╝███████╗    ██║██╔██║ █████╔╝                     ║
║   ██║  ██║██╔══╝  ██╔══██╗╚════██║    ████╔╝██║██╔═══╝                      ║
║   ██████╔╝███████╗██║  ██║███████║    ╚██████╔╝███████╗                     ║
║   ╚═════╝ ╚══════╝╚═╝  ╚═╝╚══════╝     ╚═════╝ ╚══════╝                     ║
║                                                                              ║
║        VERİ ANALİTİĞİ HAZIRLIGI: PYTHON RECAP HAFTASI                       ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

<div align="center">

### 🐍 **Makine Öğrenmesi'ne Geçmeden Önce Veri Analitiği Temelleri**

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Pandas](https://img.shields.io/badge/Pandas-Latest-green.svg?style=for-the-badge&logo=pandas&logoColor=white)](https://pandas.pydata.org/)
[![NumPy](https://img.shields.io/badge/NumPy-013243.svg?style=for-the-badge&logo=numpy&logoColor=white)](https://numpy.org/)
[![Matplotlib](https://img.shields.io/badge/Matplotlib-11557c.svg?style=for-the-badge&logo=plotly&logoColor=white)](https://matplotlib.org/)
[![Seaborn](https://img.shields.io/badge/Seaborn-3776AB.svg?style=for-the-badge&logo=python&logoColor=white)](https://seaborn.pydata.org/)
[![Plotly](https://img.shields.io/badge/Plotly-3F4F75.svg?style=for-the-badge&logo=plotly&logoColor=white)](https://plotly.com/)

[![Status](https://img.shields.io/badge/Status-Python%20Fundamentals-success.svg?style=for-the-badge)]()
[![Level](https://img.shields.io/badge/Level-Preparation%20Week-yellow.svg?style=for-the-badge)]()
[![Type](https://img.shields.io/badge/Type-Data%20Analytics-purple.svg?style=for-the-badge)]()
[![Duration](https://img.shields.io/badge/Duration-Week%202-orange.svg?style=for-the-badge)]()

---

### 🌟 **Strateji: Teknik Değil, Analitik Düşünce**

*"Makine Öğrenmesi modelleri kurmadan önce, verinin dilini konuşmalısınız!"*

</div>

---

## 🎬 GİRİŞ: NEDEN BU HAFTA?

### 💡 **Anlayış Değişimi**

Bu hafta **kod yazmak** için değil, **veri ile konuşmak** için hazırlanıyoruz.

<div align="center">

```mermaid
graph LR
    A[❌ Yanlış Anlayış] --> B[🔄 Paradigma]
    B --> C[✅ Doğru Anlayış]
    
    A1[Python öğrenmek] --> A
    A2[Kütüphane ezberlemek] --> A
    A3[Fonksiyon bilmek] --> A
    
    C --> C1[Veriyi anlamak]
    C --> C2[İçgörü çıkarmak]
    C --> C3[Karar vermek]
    
    style A fill:#ffcccc
    style B fill:#fff3cd
    style C fill:#d4f1d4
```

</div>

### 🎯 **Bu Haftanın Misyonu**

**Makine Öğrenmesi'ne** geçmeden önce, **Veri Analitiği** için Python ekosistemini hatırlayacağız.

### 📊 **Gerçek Dünya Bağlamı**

<div align="center">

```
┌────────────────────────────────────────────────────────────────┐
│                                                                │
│   "Bir YBS uzmanı olarak,                                      │
│    Python ile veri analizi bana NE KAZANDIRIR?"               │
│                                                                │
│   Cevap:                                                       │
│   ✓ Excel'in 1 milyon satır sınırını aşma                    │
│   ✓ Tekrar edilebilir analiz süreçleri                       │
│   ✓ Otomatik raporlama sistemleri                            │
│   ✓ Büyük veri ile çalışma yetkinliği                        │
│   ✓ Görselleştirme ile hikaye anlatma                        │
│                                                                │
└────────────────────────────────────────────────────────────────┘
```

</div>

---

## 📊 KULLANILAN VERİ SETLERİ

### 🎬 **Netflix İçerik Katalogu**

Bu hafta **ana veri setimiz** olarak Netflix içerik kataloğunu kullandık. Sentetik ama gerçekçi bir veri seti ile içerik analizi yaptık.

<div align="center">

```mermaid
graph TD
    A[🎬 Netflix Dataset] --> B[📋 34,854 İçerik]
    
    B --> C[🎥 Filmler]
    B --> D[📺 Diziler]
    
    C --> E[🌍 Ülke Bilgisi]
    C --> F[📅 Yayın Tarihi]
    C --> G[⭐ Kullanıcı Puanı]
    
    D --> E
    D --> F
    D --> G
    
    E --> H[📊 Analiz Çıktıları]
    F --> H
    G --> H
    
    H --> I[💡 İş Kararları]
    
    style A fill:#E50914,color:#fff
    style H fill:#d4f1d4
    style I fill:#fff3cd
```

</div>

**Veri Yapısı:**

| Sütun | Açıklama | Örnek Değer | YBS Kullanımı |
|-------|----------|-------------|---------------|
| `title` | İçerik adı | "The Adventures" | Katalog yönetimi |
| `type` | Film veya Dizi | Movie / TV Show | İçerik stratejisi |
| `genre` | Tür kategorisi | Action, Drama, Comedy | Hedef kitle analizi |
| `release_year` | Çıkış yılı | 2008 | Trend analizi |
| `duration` | Süre bilgisi | 182 min / 5 Seasons | İçerik planlaması |
| `rating` | Kullanıcı puanı | 4.3 | Kalite metrikleri |
| `country` | Üretim ülkesi | USA, Turkey, Japan | Coğrafi segmentasyon |
| `date_added` | Eklenme tarihi | 2017-06-04 | Yayın takvimlendirme |

### 🛒 **Trendyol Sipariş Verileri**

Case Study için kullandığımız **e-ticaret veri seti**. Gerçek bir operasyon masası perspektifinden müşteri davranışı analizi.

<div align="center">

```mermaid
graph LR
    A[🛒 Trendyol Dataset] --> B[📦 59,866 Sipariş]
    
    B --> C[💳 Ödeme Bilgisi]
    B --> D[🚚 Teslimat Durumu]
    B --> E[⭐ Değerlendirme]
    
    C --> F[💼 İş Zekası]
    D --> F
    E --> F
    
    F --> G[🎯 Aksiyon Planı]
    
    style A fill:#FF6000,color:#fff
    style F fill:#d4f1d4
    style G fill:#fff3cd
```

</div>

**Operasyonel Değişkenler:**

| Sütun | Açıklama | Analiz Amacı |
|-------|----------|--------------|
| `order_id` | Sipariş numarası | Takip sistemi |
| `user_id` | Müşteri kimliği | Davranış analizi |
| `product_category` | Ürün kategorisi | Envanter yönetimi |
| `product_price` | Ürün fiyatı | Gelir analizi |
| `discount_rate` | İndirim oranı | Karlılık hesabı |
| `payment_type` | Ödeme yöntemi | Risk değerlendirme |
| `delivery_time_days` | Teslimat süresi | Lojistik optimizasyon |
| `seller_rating` | Satıcı puanı | Tedarikçi yönetimi |
| `product_rating` | Ürün puanı | Müşteri memnuniyeti |
| `return_status` | İade durumu | Kayıp önleme |
| `city` | Şehir bilgisi | Bölgesel planlama |

### 💡 **Veri Setleri Neden Bu İkisi?**

<div align="center">

| Özellik | Netflix | Trendyol | YBS Öğrenim Hedefi |
|---------|---------|----------|-------------------|
| **Sektör** | 🎬 Medya/Eğlence | 🛒 E-Ticaret | Farklı iş modellerini anlama |
| **Veri Boyutu** | 34K+ satır | 59K+ satır | Büyük veriyle çalışma |
| **Karmaşıklık** | Orta | Yüksek | Eksik veri yönetimi |
| **Görselleştirme** | Kategorik analiz | Sayısal/Kategorik mix | Çoklu grafik teknikleri |
| **İş Sorusu** | "Hangi içerikler popüler?" | "Hangi müşteriler riskli?" | Karar verme süreçleri |

</div>

---

## 🔧 PYTHON VERİ ANALİZİ EKOSİSTEMİ

### 🌳 **Araç Kutusu Haritası**

Bu hafta **5 temel kütüphane** ile veri analizinin her aşamasını deneyimledik:

<div align="center">

```mermaid
mindmap
  root((🐍 Python<br/>Veri Analitiği))
    🔢 NumPy
      Sayısal Hesaplama
      N-Boyutlu Array
      Matematiksel İşlemler
      Performans Odaklı
    🐼 Pandas
      DataFrame Yapısı
      Veri Okuma/Yazma
      Filtreleme & Gruplama
      Veri Temizleme
    📊 Matplotlib
      Temel Grafikler
      Çizgi & Çubuk
      Scatter Plot
      Tam Kontrol
    🎨 Seaborn
      İstatistiksel Görsel
      Güzel Temalar
      Korelasyon Haritası
      Hızlı Analiz
    ✨ Plotly
      İnteraktif Grafikler
      Dashboard
      Dinamik Filtreler
      Yönetici Sunumları
```

</div>

### 📈 **Veri Analizi Akış Sürecimiz**

<div align="center">

```mermaid
flowchart TD
    A[📥 Veri Toplama] --> B{🔍 Veri Kalitesi OK?}
    B -->|❌ Hayır| C[🧹 Veri Temizleme]
    B -->|✅ Evet| D[📊 Keşifsel Analiz]
    C --> D
    
    D --> E[📈 Tanımlayıcı İstatistikler]
    E --> F[🎯 Segmentasyon]
    F --> G[📊 Görselleştirme]
    
    G --> H{💡 İçgörü Var mı?}
    H -->|❌ Hayır| D
    H -->|✅ Evet| I[📋 Raporlama]
    
    I --> J[💼 İş Kararı]
    J --> K[🚀 Aksiyon]
    
    style A fill:#E5F4FF
    style C fill:#FFE5E5
    style D fill:#FFF3CD
    style G fill:#E8D6FF
    style I fill:#D6FFE8
    style J fill:#FFD6E8
    
    L[🔢 NumPy] -.-> E
    M[🐼 Pandas] -.-> C
    M -.-> D
    M -.-> F
    N[📊 Matplotlib] -.-> G
    O[🎨 Seaborn] -.-> G
    P[✨ Plotly] -.-> G
```

</div>

---

## 🐼 ANA KÜTÜPHANELER

### 📚 **Kütüphane Karşılaştırması**

<div align="center">

| Kütüphane | 🎯 Ana Amaç | 💪 Süper Gücü | 🏢 YBS Kullanım Senaryosu | 📝 Notebookt'ta Ne Yaptık? |
|-----------|------------|---------------|---------------------------|----------------------------|
| **🔢 NumPy** | Sayısal hesaplama | Hızlı matematiksel işlemler | Finansal hesaplamalar, istatistiksel analizler | Array operasyonları, matematiksel fonksiyonlar |
| **🐼 Pandas** | Veri manipülasyonu | DataFrame ile Excel benzeri işlemler | Satış raporları, müşteri segmentasyonu | CSV okuma, filtreleme, gruplama, pivot tablo |
| **📊 Matplotlib** | Temel görselleştirme | Her detaya tam kontrol | Yıllık performans grafikleri | Bar chart, line plot, scatter plot |
| **🎨 Seaborn** | İstatistiksel görsel | Güzel ve hızlı grafikler | Trend analizi, dağılım grafikleri | Heatmap, box plot, distribution plot |
| **✨ Plotly** | İnteraktif görsel | Zoom, filter, hover özellikleri | Yönetim dashboardları, sunumlar | İnteraktif bar, scatter, sunburst charts |

</div>

### 🔄 **Kütüphaneler Arası İlişki**

<div align="center">

```mermaid
graph TB
    subgraph "📊 GÖRSELLEŞTİRME KATMANI"
        E[📊 Matplotlib<br/>Statik Grafikler]
        F[🎨 Seaborn<br/>İstatistiksel Görsel]
        G[✨ Plotly<br/>İnteraktif Dashboard]
    end
    
    subgraph "🔧 VERİ İŞLEME KATMANI"
        C[🐼 Pandas<br/>DataFrame Manipülasyonu]
        D[🔢 NumPy<br/>Array İşlemleri]
    end
    
    subgraph "💾 VERİ KATMANI"
        A[📁 CSV Dosyaları]
        B[📊 Excel/Database]
    end
    
    A --> C
    B --> C
    C --> D
    D --> C
    
    C --> E
    C --> F
    C --> G
    
    D --> E
    
    F -.->|Kullanır| E
    G -.->|Bağımsız| C
    
    style C fill:#52C41A,color:#fff
    style D fill:#1890FF,color:#fff
    style E fill:#FA8C16,color:#fff
    style F fill:#EB2F96,color:#fff
    style G fill:#722ED1,color:#fff
```

</div>

### 🎯 **Hangi Kütüphaneyi Ne Zaman Kullanırız?**

<div align="center">

```mermaid
flowchart LR
    A{🤔 İhtiyacım Ne?} --> B[📊 Veri Okuma/Temizleme]
    A --> C[🔢 Matematiksel Hesaplama]
    A --> D[📈 Basit Statik Grafik]
    A --> E[🎨 Güzel Görsel Hızlıca]
    A --> F[✨ Dashboard/Sunum]
    
    B --> B1[🐼 Pandas<br/>read_csv, groupby, merge]
    C --> C1[🔢 NumPy<br/>mean, std, array ops]
    D --> D1[📊 Matplotlib<br/>plot, bar, scatter]
    E --> E1[🎨 Seaborn<br/>heatmap, boxplot]
    F --> F1[✨ Plotly<br/>interactive charts]
    
    style B1 fill:#52C41A,color:#fff
    style C1 fill:#1890FF,color:#fff
    style D1 fill:#FA8C16,color:#fff
    style E1 fill:#EB2F96,color:#fff
    style F1 fill:#722ED1,color:#fff
```

</div>

### 💼 **YBS Perspektifi: İş Değeri Yaratma**

| Süreç Aşaması | Kullanılan Araç | İş Çıktısı | Karar Etkisi |
|---------------|-----------------|------------|--------------|
| 📥 **Veri Toplama** | Pandas | Farklı kaynaklardan birleşik veri | Veri siloları yıkılır |
| 🧹 **Veri Temizleme** | Pandas + NumPy | Tutarlı, güvenilir veri | Hatalı kararlar önlenir |
| 🔍 **Keşifsel Analiz** | Pandas | İlk içgörüler ve hipotezler | Strateji yönü belirlenir |
| 📊 **İstatistiksel Analiz** | NumPy + Pandas | Sayısal kanıtlar | Veriye dayalı argümanlar |
| 📈 **Görselleştirme** | Matplotlib/Seaborn/Plotly | Hikaye anlatımı | Paydaş ikna edilir |
| 📋 **Raporlama** | Tümü | Aksiyon önerileri | İş değeri gerçekleşir |

---

## 🎯 CASE STUDY: OPERASYON MASASI ANALİZİ

### 📋 **Gerçek Dünya Senaryosu**

Bu hafta **Telekomünikasyon Şirketi Müşteri Tutundurma ve Risk Analitiği** perspektifinden bir case study üzerinde çalıştık. Amaç: **Teknik modelleme yapmadan, yöneticiye karar aldırabilecek içgörüler üretmek**.

<div align="center">

```mermaid
timeline
    title 🚀 Case Study Analiz Yolculuğu
    section Hazırlık
        Veri Toplama : Kaggle Dataset
        Kalite Kontrolü : Doğrulama Pipeline
    section Keşif
        EDA : İstatistikler
        Görselleştirme : İlk İçgörüler
    section Analiz
        Segmentasyon : Risk Grupları
        Filtreleme : Kritik Müşteriler
    section Sunum
        Raporlama : Yönetici Özeti
        Aksiyonlar : Strateji Önerileri
```

</div>

### 🔍 **12 Adımlık Analitik Protokol**

Case Study boyunca **operasyon masası protokolü** ile ilerledik:

<div align="center">

| Adım | Başlık | Araç | Çıktı |
|------|--------|------|-------|
| 1️⃣ | Veri Kaynağı Doğrulama | Pandas | Kapı kontrolü ✓ |
| 2️⃣ | İlk Refleks Protokolü | Pandas | Veriyle tanışma |
| 3️⃣ | Karara Hizmet Eden Sütunlar | Pandas | Yönetici slaytı için seçim |
| 4️⃣ | Hedef Değişken Analizi | Pandas | Churn fotoğrafı |
| 5️⃣ | Riskli Segment Filtreleme | Pandas | Kritik müşteriler |
| 6️⃣ | GroupBy Analizi | Pandas | Tek satırlık cevaplar |
| 7️⃣ | Matplotlib Görsel 1 | Matplotlib | Tek bakışta içgörü |
| 8️⃣ | Matplotlib Görsel 2 | Matplotlib | Davranış eğrisi |
| 9️⃣ | Seaborn Görsel | Seaborn | İlişki haritası |
| 🔟 | Plotly İnteraktif 1 | Plotly | Etkileşimli keşif |
| 1️⃣1️⃣ | Plotly İnteraktif 2 | Plotly | Risk haritası |
| 1️⃣2️⃣ | Yönetici Özeti | Tümü | Operasyon masası çıktısı |

</div>

### 💼 **İş Soruları ve Cevaplar**

<div align="center">

```mermaid
graph TD
    A[❓ İş Sorusu] --> B{🎯 Hangi Analiz?}
    
    B --> C[📊 Tanımlayıcı<br/>Ne oldu?]
    B --> D[🔍 Tanısal<br/>Neden oldu?]
    B --> E[🔮 Öngörücü<br/>Ne olacak?]
    
    C --> F[Pandas GroupBy<br/>Segmentasyon]
    D --> G[Seaborn Heatmap<br/>Korelasyon]
    E --> H[İstatistiksel Analiz<br/>Trend Çıkarımı]
    
    F --> I[💡 İçgörü]
    G --> I
    H --> I
    
    I --> J[📋 Yönetici Raporu]
    J --> K[🚀 Aksiyon Planı]
    
    style A fill:#FFE5E5
    style I fill:#D6FFE8
    style K fill:#FFD6E8
```

</div>

### 🎓 **Öğrenim Çıktısı**

Bu case study ile öğrendiklerimiz:

- ✅ **Veri okuma ve kalite kontrolü** (Pandas)
- ✅ **Eksik veri yönetimi** stratejileri
- ✅ **Filtreleme ve segmentasyon** teknikleri
- ✅ **GroupBy ile özet istatistikler** üretme
- ✅ **Statik grafikler** (Matplotlib) ile raporlama
- ✅ **İstatistiksel görseller** (Seaborn) ile ilişki keşfi
- ✅ **İnteraktif dashboard** (Plotly) ile sunum
- ✅ **Yönetici özeti** hazırlama becerisi

## 🎓 KAPANIŞ

### 💭 **Yansıma: Nereden Nereye?**

<div align="center">

```
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║   "Excel'de 1000 satır veriyle uğraşırken,                  ║
║    Python ile 100.000 satırı saniyeler içinde analiz ettik" ║
║                                                              ║
║   "Manuel grafikler çizerken,                                ║
║    5 satır kod ile interaktif görseller yarattık"           ║
║                                                              ║
║   "Tahmin ve sezgiyle karar verirken,                        ║
║    Veriye dayalı stratejiler geliştirdik"                   ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

</div>

### 🌟 **Son Söz**

Bu hafta **Python veri analizi araçlarını** öğrenmedik sadece; **veriyle konuşmayı**, **sayılardan hikaye çıkarmayı**, **grafiklerde anlam bulmayı** öğrendik.

**Unutmayın:**  
> 💡 *"En iyi veri analisti, en çok Python bilen değil; verinin dilini en iyi anlayan ve iş değerine dönüştürendir."*

### 🚀 **Motivasyon: Yolculuk Yeni Başlıyor**

<div align="center" style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 30px; border-radius: 15px; color: white;">

### **✨ Siz Artık Veri Analisti Adayısınız! ✨**

Bu hafta attığınız adımlar, **Makine Öğrenmesi** yolculuğunuzun en sağlam temelleri.  

🎯 **NumPy** ile matematik işlemleri yaptınız  
📊 **Pandas** ile veri dansı yaptınız  
🎨 **Matplotlib, Seaborn, Plotly** ile hikaye anlattınız  

Şimdi sırada, bu araçlarla **bir verisetini derinlemesine keşfedip modelleme öncesi en iyi anlayacağımız nokta olan Keşifsel Veri Analizi (EDA)** var!

**Unutmayın:** Her büyük veri bilimci, bir gün sizin olduğunuz noktadan başladı.  
Fark yaratan, **devam etmek** ve **öğrenmeye aç kalmaktır**.

---

### 🔥 **"Veri, yeni petrol değil; veriden anlam çıkarmak yeni petrol!"**

**Gelecek hafta keşifsel veri analizi sürecini birlikte deneyimleyelim!** 🚀

</div>

---

<div align="center">

**📚 YBS 3259 - Makine Öğrenmesi | Ders 02**  
**🎓 2025-2026 Bahar Dönemi**  
**👨‍🏫 Hazırlayan: Dr. Öğr. Ü. Zeynep ÖZER & Arş. Gör. Cemal YÜKSEL**

**⭐ Başarılar Dileriz! ⭐**
