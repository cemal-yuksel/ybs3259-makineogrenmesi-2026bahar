"""
Model Bilgisi Sayfası - Model Detayları ve Karar Özeti
Shneiderman Kural 3-8: Bilgilendirici, düşük bellek yükü
"""

import streamlit as st
from pathlib import Path

def show():
    """Model bilgisi sayfası içeriği"""
    
    st.markdown("""
    <div class="hero-card">
        <h1 style="margin: 0; color: #1F2937;">ℹ️ Model Bilgisi ve Karar Özeti</h1>
        <p style="margin-top: 8px; color: #6B7280;">
            Random Forest modelinin özellikleri, seçim gerekçesi ve sınırlamaları
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Model Kimlik Kartı
    st.markdown("### 🎯 Model Kimlik Kartı")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="metric-card">
            <h4 style="color: #2E86AB; margin: 0;">📋 Temel Bilgiler</h4>
            <table style="width: 100%; margin-top: 12px;">
                <tr><td><b>Model Adı:</b></td><td>Random Forest Classifier</td></tr>
                <tr><td><b>Problem Tipi:</b></td><td>Binary Classification</td></tr>
                <tr><td><b>Hedef Değişken:</b></td><td>Outcome (0: Sağlıklı, 1: Diyabet)</td></tr>
                <tr><td><b>Feature Sayısı:</b></td><td>14 (6 orijinal + 8 engineered)</td></tr>
                <tr><td><b>Eğitim Verisi:</b></td><td>614 satır</td></tr>
                <tr><td><b>Test Verisi:</b></td><td>154 satır</td></tr>
            </table>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-card">
            <h4 style="color: #6A994E; margin: 0;">📊 Performans Metrikleri</h4>
            <table style="width: 100%; margin-top: 12px;">
                <tr><td><b>Test F1-Score:</b></td><td>0.7700</td></tr>
                <tr><td><b>Test Accuracy:</b></td><td>77.3%</td></tr>
                <tr><td><b>ROC-AUC:</b></td><td>0.8306</td></tr>
                <tr><td><b>CV Mean:</b></td><td>0.7547</td></tr>
                <tr><td><b>CV Std:</b></td><td>0.0202</td></tr>
                <tr><td><b>Overfitting:</b></td><td>0.2300</td></tr>
            </table>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Model Seçim Gerekçesi
    st.markdown("### 🏆 Model Seçim Gerekçesi")
    
    st.info("""
    **Random Forest neden seçildi?**
    
    1. **En Yüksek Performans:** 18 model arasında en yüksek Test F1-Score (0.77)
    2. **ROC-AUC Üstünlüğü:** 0.83 ile mükemmel sınıf ayırma gücü
    3. **Ensemble Güveni:** Birden fazla decision tree'nin konsensüsü (robust tahmin)
    4. **Hızlı Eğitim:** 0.3 saniye eğitim süresi (deployment friendly)
    5. **Baseline Karşılaştırması:** Dummy Classifier'a göre %50.6 iyileşme
    6. **CV Kararlılığı:** Düşük standart sapma (0.02) ile tutarlı performans
    """)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Feature Bilgisi
    st.markdown("### 📊 Kullanılan Features")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **🔵 Orijinal Features (6 adet):**
        1. `Pregnancies` - Hamilelik sayısı
        2. `Glucose` - Glikoz seviyesi (mg/dL)
        3. `BloodPressure` - Diyastolik kan basıncı (mm Hg)
        4. `BMI` - Vücut kitle indeksi
        5. `DiabetesPedigreeFunction` - Diyabet soy ağacı skoru
        6. `Age` - Yaş (yıl)
        
        **❌ Çıkarılan Features:**
        - `Insulin` (%48.7 eksik, istatistiksel anlamlılık yok)
        - `SkinThickness` (%29.6 eksik, zayıf öngörü gücü)
        """)
    
    with col2:
        st.markdown("""
        **🟢 Engineered Features (8 adet):**
        
        **Binary Features (4):**
        1. `High_Glucose` - Yüksek glikoz flag
        2. `High_BMI` - Yüksek BMI flag
        3. `Old_Age` - Yaşlı flag
        4. `Many_Pregnancies` - Çok hamilelik flag
        
        **Interaction Features (4):**
        5. `BMI_Age` - BMI × Age
        6. `Glucose_BMI` - Glucose × BMI
        7. `Glucose_Age` - Glucose × Age
        8. `BMI_DiabetesPedigreeFunction` - BMI × DPF
        """)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Veri İşleme Pipeline
    st.markdown("### 🔄 Veri İşleme Pipeline")
    
    st.markdown("""
    <div class="info-box">
        <h4 style="margin: 0;">DataPrep Expert Pipeline (7 Aşama)</h4>
        <ol style="margin-top: 8px;">
            <li><b>Gizli Eksik Veri:</b> 0 değerleri → NaN → Median imputation</li>
            <li><b>Değişken Çıkarma:</b> Insulin ve SkinThickness çıkarıldı</li>
            <li><b>Outlier Yönetimi:</b> BloodPressure için Winsorization (5%-95%)</li>
            <li><b>Çarpıklık Dönüşümü:</b> Yeo-Johnson transformation</li>
            <li><b>Feature Engineering:</b> 8 yeni feature oluşturuldu</li>
            <li><b>Scaling:</b> StandardScaler (pipeline içinde)</li>
            <li><b>Train-Test Split:</b> Stratified split (80-20)</li>
        </ol>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Confusion Matrix Yorumu
    st.markdown("### 🎯 Confusion Matrix Detaylı Yorumu")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **📊 Confusion Matrix:**
        
        ```
                  Predicted 0  Predicted 1
        Actual 0       85           15
        Actual 1       20           34
        ```
        
        **Metrikler:**
        - **Precision:** 0.69 (pozitif tahminlerin %69'u doğru)
        - **Recall:** 0.63 (diyabetlilerin %63'ü yakalandı)
        - **Specificity:** 0.85 (sağlıklıların %85'i doğru tespit)
        """)
    
    with col2:
        st.markdown("""
        **🔍 Hata Analizi:**
        
        - **False Positives (FP): 15**
          - Sağlıklı kişiler yanlış diyabetli tahmin edildi
          - Type I Error (gereksiz alarm)
          - İşletme maliyeti: Gereksiz takip/tetkik
        
        - **False Negatives (FN): 20** ⚠️
          - Diyabetli kişiler yanlış sağlıklı tahmin edildi
          - Type II Error (kaçırılan hasta)
          - İşletme maliyeti: Geç teşhis riski (KRİTİK!)
        """)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    st.warning("""
    **⚠️ Kritik Bulgu: False Negative Riski**
    
    Model, **diyabetli kişileri sağlıklı olarak tahmin etme eğiliminde** (FN=20 > FP=15).
    Bu, sağlık uygulamaları için kritik bir hatadır çünkü hasta olana "sağlıklısın" demek,
    gereksiz alarm vermekten daha risklidir.
    
    **Öneri:** Düşük güvenli pozitif tahminler özellikle dikkatle yorumlanmalıdır.
    """)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Model Sınırlamaları
    st.markdown("### ⚠️ Model Sınırlamaları ve Riskler")
    
    st.error("""
    **🚫 Kritik Sınırlamalar:**
    
    1. **Tek Başına Teşhis Aracı Değildir**
       - Bu model tıbbi teşhis koymaz
       - Uzman değerlendirmesiyle birlikte kullanılmalıdır
       - FDA/CE onaylı tıbbi cihaz değildir
    
    2. **False Negative Riski (%13)**
       - Diyabetli kişilerin yaklaşık %37'si kaçırılabilir
       - Düşük güvenli negatif tahminler şüpheli kabul edilmelidir
    
    3. **Veri Seti Sınırlamaları**
       - Yalnızca 768 kayıt ile eğitildi
       - Pima Indian kadınları üzerinde geliştirildi
       - Farklı etnik/demografik gruplarda performans değişebilir
    
    4. **Feature Sınırlamaları**
       - Insulin ve SkinThickness dahil değil
       - Yalnızca 6 temel sağlık göstergesi kullanılıyor
       - HbA1c, açlık şekeri gibi kritik testler yok
    
    5. **Overfitting Riski**
       - 0.23 overfitting skoru (yüksek)
       - Yeni verilerde performans düşebilir
       - Düzenli retraining gerektirir
    
    6. **Güvenlik ve Etik**
       - Kullanıcı verilerinin güvenliği garanti edilmelidir
       - Yanıltıcı pozitif/negatif tahminler hukuki risk taşır
       - Model bias'ı (önyargı) kontrol edilmelidir
    """)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Kullanım Önerileri
    st.markdown("### 💡 Kullanım Önerileri")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.success("""
        **✅ Uygun Kullanım:**
        - Erken risk taraması (screening)
        - Sağlık merkezi ön değerlendirme
        - Klinik karar destek sistemi
        - Populasyon düzeyinde risk profilleme
        - Eğitim ve farkındalık amaçlı
        """)
    
    with col2:
        st.error("""
        **❌ Uygunsuz Kullanım:**
        - Tek başına kesin teşhis
        - Acil durum değerlendirmesi
        - Tedavi kararı vermek
        - Sigorta/istihdam kararı
        - Legal/forensic amaç
        """)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Sonraki Adımlar
    st.markdown("### 🚀 Model İyileştirme Önerileri")
    
    st.info("""
    **📈 Gelecekteki İyileştirmeler:**
    
    1. **Threshold Optimizasyonu:** Default 0.5 yerine 0.3-0.4 ile FN oranını azalt
    2. **Class Weight Artırımı:** `class_weight={0: 1, 1: 2}` ile pozitif sınıfı güçlendir
    3. **Feature Importance Analizi:** SHAP/LIME ile model yorumlanabilirliğini artır
    4. **Hyperparameter Tuning:** GridSearchCV ile ince ayar
    5. **Ensemble Yöntemleri:** Voting/Stacking ile birden fazla model kombinasyonu
    6. **External Validation:** Farklı hastane/bölge verilerinde test et
    7. **Prospective Study:** Gerçek klinik ortamda performans ölç
    8. **Model Monitoring:** Drift detection ve otomatik retraining
    """)
