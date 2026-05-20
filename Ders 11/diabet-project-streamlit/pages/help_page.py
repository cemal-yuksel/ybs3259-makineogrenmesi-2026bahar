"""
Yardım Sayfası - Kullanım Kılavuzu ve SSS
Shneiderman Kural 8: Yardım ve dokümantasyon
"""

import streamlit as st

def show():
    """Yardım sayfası içeriği"""
    
    st.markdown("""
    <div class="hero-card">
        <h1 style="margin: 0; color: #1F2937;">❓ Yardım ve Kullanım Kılavuzu</h1>
        <p style="margin-top: 8px; color: #6B7280;">
            Uygulamayı nasıl kullanacağınız ve sık sorulan sorular
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Hızlı Başlangıç
    st.markdown("### 🚀 Hızlı Başlangıç")
    
    st.info("""
    **3 Adımda Tahmin Yapın:**
    
    1. **Sol menüden "Tekil Tahmin"** sekmesine gidin
    2. **Hasta bilgilerini** form alanlarına girin (tüm alanlar zorunlu)
    3. **"Tahmin Yap"** butonuna tıklayın ve sonucu görün
    
    Toplu tahmin için CSV dosyası yüklemek isterseniz **"Toplu Tahmin"** sekmesini kullanın.
    """)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Sayfa Açıklamaları
    st.markdown("### 📑 Sayfalar ve Kullanımları")
    
    tabs = st.tabs([
        "🏠 Ana Sayfa",
        "🔮 Tekil Tahmin",
        "📊 Toplu Tahmin",
        "📈 Model Performansı",
        "ℹ️ Model Bilgisi",
        "📡 Monitoring"
    ])
    
    with tabs[0]:
        st.markdown("""
        **🏠 Ana Sayfa - Yönetici Özeti**
        
        - Sistemin genel görünümü ve model performans metrikleri
        - Hızlı erişim butonları ile doğrudan tahmin sayfalarına geçiş
        - Kullanım amaçları ve kritik sınırlamalar
        - Model mimarisi ve veri işleme pipeline bilgisi
        
        **Ne Zaman Kullanılır:**
        - İlk girişte genel bilgi almak için
        - Model performansına hızlı bakış için
        - Diğer sayfalara hızlı erişim için
        """)
    
    with tabs[1]:
        st.markdown("""
        **🔮 Tekil Tahmin - Bireysel Risk Tahmini**
        
        **Nasıl Kullanılır:**
        1. Formdaki 6 alanı doldurun:
           - Pregnancies (Hamilelik sayısı)
           - Glucose (Glikoz seviyesi, mg/dL)
           - BloodPressure (Kan basıncı, mm Hg)
           - BMI (Vücut kitle indeksi)
           - DiabetesPedigreeFunction (Diyabet soy ağacı skoru)
           - Age (Yaş)
        2. "Tahmin Yap" butonuna tıklayın
        3. Sonucu ve güven skorunu görüntüleyin
        
        **Ek Özellikler:**
        - **"Örnek Veriyle Dene":** Hazır örnek veri ile test edin
        - **"Temizle":** Formu sıfırlayın
        - Otomatik veri doğrulama (geçersiz girişlerde uyarı)
        - Son tahmin özeti (tekrar görmek için)
        
        **Önemli Notlar:**
        - Tüm alanlar zorunludur
        - Değerler mantıksal sınırlar içinde olmalıdır
        - Düşük güvenli tahminler dikkatle yorumlanmalıdır
        """)
    
    with tabs[2]:
        st.markdown("""
        **📊 Toplu Tahmin - CSV ile Batch Prediction**
        
        **Nasıl Kullanılır:**
        1. "Örnek CSV İndir" butonuyla format örneği indirin
        2. Kendi verilerinizi CSV formatında hazırlayın
        3. CSV dosyasını yükleyin
        4. Kolon kontrolü otomatik yapılır
        5. "Toplu Tahmin Yap" butonuna tıklayın
        6. Sonuçları görüntüleyin ve CSV olarak indirin
        
        **Gerekli CSV Formatı:**
        ```
        Pregnancies,Glucose,BloodPressure,BMI,DiabetesPedigreeFunction,Age
        6,148,72,33.6,0.627,50
        1,85,66,26.6,0.351,31
        ```
        
        **Önemli Notlar:**
        - Kolon isimleri tam eşleşmeli (büyük/küçük harf duyarlı)
        - Tüm değerler sayısal olmalıdır
        - Eksik kolon varsa hata verilir
        - Fazla kolonlar göz ardı edilir
        - Maksimum dosya boyutu: 200MB
        """)
    
    with tabs[3]:
        st.markdown("""
        **📈 Model Performansı - Detaylı Analiz**
        
        **İçerik:**
        - 18 modelin performans karşılaştırma tablosu
        - İnteraktif grafikler (tab menüsü ile gezin):
          - Model Performans Karşılaştırması
          - Cross-Validation Kararlılık Analizi
          - Overfitting Analizi
          - Eğitim Süresi Karşılaştırması
          - Leadership Matrix
          - Confusion Matrix
          - ROC Curve
        
        **Nasıl Yorumlanır:**
        - **Test F1-Score:** Yüksek = iyi performans
        - **CV Mean:** Cross-validation ortalaması
        - **CV Std:** Düşük = kararlı model
        - **Overfitting:** Düşük = genelleme iyi
        - **Confusion Matrix:** TP, TN, FP, FN dağılımı
        
        **Ne Zaman Kullanılır:**
        - Model seçim gerekçesini anlamak için
        - Alternatif modelleri karşılaştırmak için
        - Akademik/teknik raporlama için
        """)
    
    with tabs[4]:
        st.markdown("""
        **ℹ️ Model Bilgisi - Teknik Detaylar**
        
        **İçerik:**
        - Model kimlik kartı (temel bilgiler)
        - Model seçim gerekçesi
        - Kullanılan feature'lar (orijinal + engineered)
        - Veri işleme pipeline açıklaması
        - Confusion matrix detaylı yorumu
        - Model sınırlamaları ve riskler
        - Kullanım önerileri
        - İyileştirme önerileri
        
        **Ne Zaman Kullanılır:**
        - Model hakkında detaylı bilgi almak için
        - Akademik/teknik dokümantasyon için
        - Model sınırlamalarını anlamak için
        - Güvenlik ve etik notları için
        """)
    
    with tabs[5]:
        st.markdown("""
        **📡 Monitoring - Sistem İzleme**
        
        **İçerik:**
        - Toplam tahmin istatistikleri
        - Günlük tahmin zaman serisi
        - Tahmin sınıf dağılımı (pie chart)
        - Güven skoru dağılımı (histogram)
        - Son 20 tahmin listesi
        - Sistem durumu özeti
        - Log dosyası indirme
        
        **Ne Zaman Kullanılır:**
        - Sistem kullanım istatistiklerini görmek için
        - Tahmin geçmişini incelemek için
        - Anomali tespiti için
        - Raporlama amaçlı log indirmek için
        
        **Önemli Notlar:**
        - İlk tahminden sonra veriler görünür olur
        - Tüm tahminler otomatik loglanır
        - Log dosyası düzenli yedeklenmelidir
        """)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Input Alanları Açıklamaları
    st.markdown("### 📝 Input Alanları Açıklamaları")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **1. Pregnancies (Hamilelik Sayısı)**
        - **Açıklama:** Kişinin toplam hamilelik sayısı
        - **Birim:** Sayı (tam sayı)
        - **Normal Aralık:** 0-17 (veri setinde)
        - **Örnek:** 6
        - **Not:** Erkekler için 0 giriniz
        
        **2. Glucose (Glikoz Seviyesi)**
        - **Açıklama:** 2 saatlik oral glikoz tolerans testinde plazma glikoz
        - **Birim:** mg/dL
        - **Normal Aralık:** 70-180 (normal), >200 (diyabetik)
        - **Örnek:** 148
        - **Kritik:** En önemli feature
        
        **3. BloodPressure (Kan Basıncı)**
        - **Açıklama:** Diyastolik kan basıncı (alt değer)
        - **Birim:** mm Hg
        - **Normal Aralık:** 60-90 (normal), >90 (yüksek)
        - **Örnek:** 72
        - **Not:** Sistolik (üst) değer değil
        """)
    
    with col2:
        st.markdown("""
        **4. BMI (Vücut Kitle İndeksi)**
        - **Açıklama:** Vücut ağırlığı / Boy uzunluğu²
        - **Birim:** kg/m²
        - **Normal Aralık:** 18.5-24.9 (normal), 25-29.9 (fazla kilolu), ≥30 (obez)
        - **Örnek:** 33.6
        - **Hesaplama:** Ağırlık(kg) / Boy(m)²
        
        **5. DiabetesPedigreeFunction**
        - **Açıklama:** Aile geçmişine dayalı diyabet risk skoru
        - **Birim:** Skala (0-2.5 tipik)
        - **Normal Aralık:** 0.1-0.5 (düşük risk), >1.0 (yüksek risk)
        - **Örnek:** 0.627
        - **Not:** Genetik risk faktörü
        
        **6. Age (Yaş)**
        - **Açıklama:** Kişinin yaşı
        - **Birim:** Yıl
        - **Normal Aralık:** 21-81 (veri setinde)
        - **Örnek:** 50
        - **Not:** Yaş arttıkça diyabet riski artar
        """)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # SSS
    st.markdown("### ❓ Sık Sorulan Sorular (SSS)")
    
    with st.expander("❓ Model ne kadar güvenilir?"):
        st.markdown("""
        Model %77 Test Accuracy ve 0.77 F1-Score ile **iyi seviyede** performans gösteriyor.
        Ancak **%20 False Negative** riski var (diyabetli kişiyi yanlış sağlıklı tahmin etme).
        
        **Sonuç:** Güvenilir bir ön tarama aracıdır, ancak kesin teşhis için yetersizdir.
        Mutlaka uzman doktor değerlendirmesiyle birlikte kullanılmalıdır.
        """)
    
    with st.expander("❓ Düşük güven skorlu tahmin ne anlama gelir?"):
        st.markdown("""
        Güven skoru modelin tahmin için ne kadar emin olduğunu gösterir:
        
        - **%80+ (Yüksek):** Model çok emin, tahmin güvenilir
        - **%60-80 (Orta):** Model orta derecede emin, dikkatli yorumlayın
        - **%60> (Düşük):** Model emin değil, şüpheli tahmin, mutlaka uzman danışın
        
        **Önemli:** Düşük güvenli tahminlerde **ikinci görüş** almak kritiktir.
        """)
    
    with st.expander("❓ Neden bazı özellikler (Insulin, SkinThickness) kullanılmıyor?"):
        st.markdown("""
        **Insulin:** %48.7 eksik veri, istatistiksel anlamlılık yok
        **SkinThickness:** %29.6 eksik veri, zayıf öngörü gücü
        
        DataPrep Expert bu iki feature'ı **overfitting riskini azaltmak** ve 
        **model genelleme gücünü artırmak** için çıkardı. Model performansı bu 
        karardan sonra iyileşti.
        """)
    
    with st.expander("❓ Modeli hangi veriler için kullanabilirim?"):
        st.markdown("""
        **Uygun:**
        - 18-81 yaş arası bireyler
        - Temel sağlık göstergeleri mevcut olan kişiler
        - Erken risk taraması amacıyla
        
        **Uygun Değil:**
        - 18 yaş altı çocuklar (model bununla eğitilmedi)
        - Hamile kadınlar (gebelikte glikoz metabolizması farklıdır)
        - Tip 1 diyabet (model Tip 2 için tasarlandı)
        - Acil durum değerlendirmesi
        """)
    
    with st.expander("❓ Tahminler nereye kaydediliyor?"):
        st.markdown("""
        Tüm tahminler otomatik olarak **logs/prediction_log.csv** dosyasına kaydedilir.
        
        **Kaydedilen Bilgiler:**
        - Timestamp (zaman damgası)
        - Tahmin sonucu (Diyabet Var/Yok)
        - Güven skoru
        - Input feature değerleri
        
        **Gizlilik:** Log dosyası yerel sunucuda tutulur. Üretim ortamında 
        veri gizliliği politikası uygulanmalıdır.
        """)
    
    with st.expander("❓ Model ne sıklıkla güncellenmelidir?"):
        st.markdown("""
        **Önerilen Güncelleme Sıklığı:**
        
        - **Performans düşüşünde:** Hemen (drift tespit edilirse)
        - **Yeni veri geldiğinde:** 3-6 ayda bir
        - **Feature değişikliği:** Gerektiğinde
        - **Hyperparameter tuning:** Yılda 1 kez
        
        **Monitoring:** Tahmin istatistiklerini haftalık kontrol edin.
        Feature drift tespit edilirse retraining yapın.
        """)
    
    with st.expander("❓ False Negative (FN) riskini nasıl azaltabilirim?"):
        st.markdown("""
        **Threshold Optimizasyonu:**
        - Default threshold 0.5 yerine 0.3-0.4 kullanın
        - Daha fazla pozitif tahmin yapılır (FN azalır, FP artar)
        
        **Class Weight Artırımı:**
        - Pozitif sınıfın ağırlığını artırın: `class_weight={0: 1, 1: 2}`
        
        **Ensemble Yöntemi:**
        - Birden fazla modelin konsensüsünü alın
        
        **Manuel İnceleme:**
        - Düşük güvenli negatif tahminleri manuel inceleyin
        - Sınırda (0.4-0.6 olasılık) olan vakaları şüpheli kabul edin
        """)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # İletişim ve Destek
    st.markdown("### 📞 İletişim ve Destek")
    
    st.info("""
    **🏥 Teknik Destek:**
    - **E-posta:** support@diabetes-prediction.com (örnek)
    - **Dokümantasyon:** Bu sayfa
    - **Model Versiyonu:** 1.0
    - **Son Güncelleme:** 5 Mayıs 2026
    
    **⚕️ Tıbbi Danışma:**
    Bu sistem tıbbi danışmanlık sağlamaz. Sağlık sorunları için mutlaka 
    lisanslı bir sağlık profesyoneline başvurun.
    """)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Kaynaklar
    st.markdown("### 📚 Kaynaklar ve Referanslar")
    
    st.markdown("""
    **Model Geliştirme:**
    - **Veri Seti:** Pima Indians Diabetes Database (UCI ML Repository)
    - **Algoritma:** Random Forest Classifier (scikit-learn)
    - **Preprocessing:** Yeo-Johnson, StandardScaler, Feature Engineering
    - **Validation:** 5-Fold Stratified Cross-Validation
    
    **HCI Tasarım Prensipleri:**
    - **Shneiderman'ın 8 Altın Kuralı:** Tutarlılık, kısayollar, geri bildirim, tamamlanmış eylemler, hata önleme, geri alma, kontrol, düşük bellek yükü
    - **Nielsen Kullanılabilirlik İlkeleri:** Görünürlük, gerçek dünya uyumu, kullanıcı kontrolü, standartlar, hata önleme
    - **Don Norman'ın İki Körfezi:** Gulf of Execution, Gulf of Evaluation
    
    **Deployment:**
    - **Framework:** Streamlit
    - **Agent:** Deployment Expert (Agentik Pipeline)
    - **Monitoring:** Prediction logging, basic statistics
    """)
