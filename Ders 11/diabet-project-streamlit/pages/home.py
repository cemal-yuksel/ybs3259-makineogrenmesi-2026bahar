"""
Ana Sayfa - Yönetici Özeti ve Genel Bilgilendirme
Shneiderman Kural 1-2-8: Tutarlı tasarım, hızlı erişim, düşük bellek yükü
"""

import streamlit as st
import plotly.graph_objects as go

def show(model):
    """Ana sayfa içeriği"""
    
    # Hero Başlık
    st.markdown("""
    <div class="hero-card">
        <h1 style="margin: 0; color: #1F2937; font-size: 2.8rem;">
            🏥 Diabetes Prediction System
        </h1>
        <p style="margin-top: 12px; font-size: 1.25rem; color: #6B7280;">
            HCI İlkeleri ve Shneiderman'ın 8 Altın Kuralı ile Tasarlanmış Profesyonel ML Uygulaması
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Yönetici Özeti
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="metric-card">
            <h3 style="color: #2E86AB; margin: 0;">🎯 Problem</h3>
            <p style="font-size: 1.1rem; margin-top: 12px; color: #1F2937;">
                <b>Binary Classification</b>
            </p>
            <p style="color: #6B7280; font-size: 0.95rem;">
                Kişilerin sağlık verilerine göre diyabet riskini tahmin etme
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-card">
            <h3 style="color: #6A994E; margin: 0;">🤖 Model</h3>
            <p style="font-size: 1.1rem; margin-top: 12px; color: #1F2937;">
                <b>Random Forest</b>
            </p>
            <p style="color: #6B7280; font-size: 0.95rem;">
                18 model arasından en yüksek performans
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="metric-card">
            <h3 style="color: #F18F01; margin: 0;">📊 Performans</h3>
            <p style="font-size: 1.1rem; margin-top: 12px; color: #1F2937;">
                <b>F1-Score: 0.77</b>
            </p>
            <p style="color: #6B7280; font-size: 0.95rem;">
                Baseline'a göre %50.6 iyileşme
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Kullanım Amaçları
    st.markdown("### 🎯 Kullanım Amaçları")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="success-box">
            <h4 style="margin: 0; color: #1F2937;">✅ Uygun Kullanım Alanları</h4>
            <ul style="margin-top: 8px; color: #374151;">
                <li>Erken diyabet risk taraması</li>
                <li>Sağlık merkezi ön değerlendirme</li>
                <li>Bireysel risk farkındalığı</li>
                <li>Klinik karar destek sistemi (uzman onaylı)</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="warning-box">
            <h4 style="margin: 0; color: #1F2937;">⚠️ Kritik Sınırlamalar</h4>
            <ul style="margin-top: 8px; color: #374151;">
                <li><b>Tek başına teşhis aracı değildir</b></li>
                <li>Uzman değerlendirmesiyle birlikte kullanılmalı</li>
                <li>%20 False Negative riski var</li>
                <li>Düşük güvenli tahminler dikkatle yorumlanmalı</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Performans Göstergeleri
    st.markdown("### 📈 Model Performans Göstergeleri")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="Test Accuracy",
            value="77.3%",
            delta="+50.6% vs Baseline"
        )
    
    with col2:
        st.metric(
            label="F1-Score",
            value="0.77",
            delta="Top 1/18 Model"
        )
    
    with col3:
        st.metric(
            label="ROC-AUC",
            value="0.83",
            delta="İyi Ayırma Gücü"
        )
    
    with col4:
        st.metric(
            label="CV Kararlılık",
            value="0.755 ± 0.02",
            delta="Düşük varyans"
        )
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Hızlı Erişim Butonları (Shneiderman Kural 2: Kısayollar)
    st.markdown("### 🚀 Hızlı Erişim")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🔮 Tekil Tahmin Yap", use_container_width=True):
            st.session_state.page = "🔮 Tekil Tahmin"
            st.rerun()
    
    with col2:
        if st.button("📊 Toplu Tahmin (CSV)", use_container_width=True):
            st.session_state.page = "📊 Toplu Tahmin"
            st.rerun()
    
    with col3:
        if st.button("📈 Model Performansı", use_container_width=True):
            st.session_state.page = "📈 Model Performansı"
            st.rerun()
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Sistem Mimarisi
    st.markdown("### 🏗️ Sistem Mimarisi")
    
    st.markdown("""
    <div class="info-box">
        <h4 style="margin: 0;">Agent Zinciri</h4>
        <p style="margin-top: 8px; font-family: monospace; color: #374151;">
            EDA Expert → DataPrep Expert → Model Expert → <b style="color: #2E86AB;">Deployment Expert</b>
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **Veri İşleme Pipeline:**
        - ✅ Gizli eksik veri temizlendi
        - ✅ Outlier yönetimi (Winsorization)
        - ✅ Çarpıklık normalize edildi (Yeo-Johnson)
        - ✅ 8 yeni feature oluşturuldu
        - ✅ StandardScaler uygulandı
        """)
    
    with col2:
        st.markdown("""
        **Model Özellikleri:**
        - ✅ 18 model karşılaştırıldı
        - ✅ Random Forest seçildi
        - ✅ 5-Fold CV ile doğrulandı
        - ✅ Preprocessing pipeline entegre
        - ✅ Prediction logging aktif
        """)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Etik ve Güvenlik Notları
    st.markdown("### 🛡️ Etik ve Güvenlik")
    
    st.info("""
    **ℹ️ Önemli Bilgilendirme:**
    
    Bu sistem makine öğrenmesi tabanlı bir **karar destek aracıdır**. Tıbbi teşhis koymaz ve 
    sağlık profesyonelinin yerini almaz. Düşük güvenli tahminler özellikle dikkatle 
    değerlendirilmelidir. Model %20 oranında diyabetli kişileri yanlışlıkla "sağlıklı" olarak 
    tahmin edebilir (False Negative riski).
    
    **Tüm tahminler uzman değerlendirmesiyle birlikte kullanılmalıdır.**
    """)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <p style="text-align: center; color: #6B7280; font-size: 0.9rem;">
        🏥 Diabetes Prediction System | HCI Odaklı Deployment Expert | 
        Shneiderman'ın 8 Altın Kuralı Uyumlu | Model Version 1.0
    </p>
    """, unsafe_allow_html=True)
