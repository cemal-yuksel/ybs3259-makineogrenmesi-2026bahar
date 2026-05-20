"""
Model Performans Sayfası - Detaylı Model Karşılaştırması ve Grafikler
Shneiderman Kural 7-8: Kullanıcı kontrolü, düşük bellek yükü
"""

import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
from pathlib import Path

def render_html_figure(path, height=550):
    """HTML grafikleri render et"""
    try:
        with open(path, "r", encoding="utf-8") as f:
            html_content = f.read()
        components.html(html_content, height=height, scrolling=True)
        return True
    except Exception as e:
        st.error(f"Grafik yüklenemedi: {path.name} - {e}")
        return False

def show():
    """Model performans sayfası içeriği"""
    
    st.markdown("""
    <div class="hero-card">
        <h1 style="margin: 0; color: #1F2937;">📈 Model Performansı</h1>
        <p style="margin-top: 8px; color: #6B7280;">
            18 model karşılaştırması ve performans analizi
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Yönetici Özeti
    st.markdown("### 📊 Yönetici Özeti")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="Eğitilen Model",
            value="18",
            delta="Hedef: 12+ ✅"
        )
    
    with col2:
        st.metric(
            label="En İyi Model",
            value="Random Forest",
            delta="Top 1"
        )
    
    with col3:
        st.metric(
            label="Test F1-Score",
            value="0.77",
            delta="+50.6% vs Baseline"
        )
    
    with col4:
        st.metric(
            label="ROC-AUC",
            value="0.83",
            delta="İyi Ayırma"
        )
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Model Karşılaştırma Tablosu
    st.markdown("### 📋 Model Karşılaştırma Tablosu")
    
    try:
        # PrettyTable çıktısını göster
        table_path = Path("reports/model_comparison_prettytable.txt")
        
        if table_path.exists():
            with open(table_path, "r", encoding="utf-8") as f:
                table_content = f.read()
            
            st.code(table_content, language="text")
            
            st.info("""
            **📊 Tablonun Okunması:**
            - **Ana Metrik:** Test F1-Score (modeller bu metriğe göre sıralandı)
            - **Overfit:** Train F1 - Test F1 farkı (düşük değer tercih edilir)
            - **CV Mean:** 5-Fold Cross-Validation ortalaması
            - **CV Std:** Cross-Validation standart sapması (düşük = kararlı)
            """)
        else:
            st.warning("Model karşılaştırma tablosu bulunamadı.")
    
    except Exception as e:
        st.error(f"Tablo yükleme hatası: {e}")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Grafikler
    st.markdown("### 📊 Performans Grafikleri")
    
    # Tab menüsü ile grafikler
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "📊 Model Karşılaştırma",
        "📉 CV Kararlılık",
        "🔍 Overfitting Analizi",
        "⏱️ Eğitim Süresi",
        "🏆 Leadership Matrix",
        "🎯 Confusion Matrix"
    ])
    
    with tab1:
        st.markdown("#### 📊 Model Performans Karşılaştırması")
        st.markdown("Test F1-Score'a göre tüm modellerin performans sıralaması")
        
        figure_path = Path("figures/model_phase7_performance_comparison.html")
        if figure_path.exists():
            render_html_figure(figure_path)
        else:
            st.warning("Grafik dosyası bulunamadı.")
    
    with tab2:
        st.markdown("#### 📉 Cross-Validation Kararlılık Analizi")
        st.markdown("Modellerin 5-Fold CV ortalaması ve standart sapması")
        
        figure_path = Path("figures/model_phase7_cv_stability.html")
        if figure_path.exists():
            render_html_figure(figure_path)
        else:
            st.warning("Grafik dosyası bulunamadı.")
    
    with tab3:
        st.markdown("#### 🔍 Overfitting Analizi")
        st.markdown("Train ve Test F1-Score farkı (düşük overfitting tercih edilir)")
        
        figure_path = Path("figures/model_phase7_overfitting_analysis.html")
        if figure_path.exists():
            render_html_figure(figure_path)
        else:
            st.warning("Grafik dosyası bulunamadı.")
    
    with tab4:
        st.markdown("#### ⏱️ Eğitim Süresi Karşılaştırması")
        st.markdown("Modellerin eğitim süresi (saniye)")
        
        figure_path = Path("figures/model_phase7_training_time.html")
        if figure_path.exists():
            render_html_figure(figure_path)
        else:
            st.warning("Grafik dosyası bulunamadı.")
    
    with tab5:
        st.markdown("#### 🏆 Leadership Matrix (F1 vs Overfitting)")
        st.markdown("X ekseninde F1-Score, Y ekseninde Overfitting (düşük = iyi)")
        
        figure_path = Path("figures/model_phase7_leadership_matrix.html")
        if figure_path.exists():
            render_html_figure(figure_path)
        else:
            st.warning("Grafik dosyası bulunamadı.")
    
    with tab6:
        st.markdown("#### 🎯 Final Model Confusion Matrix")
        st.markdown("Random Forest modelinin test seti confusion matrix'i")
        
        figure_path = Path("figures/model_phase10_final_confusion_matrix.html")
        if figure_path.exists():
            render_html_figure(figure_path)
        else:
            st.warning("Grafik dosyası bulunamadı.")
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        st.info("""
        **🔍 Confusion Matrix Yorumu:**
        
        - **True Negatives (TN):** 85 - Sağlıklı kişileri doğru tahmin
        - **True Positives (TP):** 34 - Diyabetli kişileri doğru tahmin
        - **False Positives (FP):** 15 - Sağlıklıyı yanlış diyabetli tahmin (Type I Error)
        - **False Negatives (FN):** 20 - Diyabetliyi yanlış sağlıklı tahmin (Type II Error) ⚠️
        
        **⚠️ Kritik Bulgu:** Model FN > FP, yani diyabetli kişileri kaçırma riski var!
        """)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # ROC Curve (varsa)
    st.markdown("### 📈 ROC Curve")
    
    roc_path = Path("figures/model_phase10_roc_curve.html")
    if roc_path.exists():
        render_html_figure(roc_path)
    else:
        st.info("ROC Curve grafiği bulunamadı (opsiyonel).")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Top 5 Model Kıyaslaması
    st.markdown("### 🏆 Top 5 Model Kıyaslaması")
    
    top5_data = {
        "Sıra": ["🥇 1", "🥈 2", "🥉 3", "4", "5"],
        "Model": ["Random Forest", "Extra Trees", "Bagging", "XGBoost", "LightGBM"],
        "Test F1": [0.7700, 0.7700, 0.7640, 0.7602, 0.7473],
        "CV Mean": [0.7547, 0.7582, 0.7315, 0.7374, 0.7372],
        "CV Std": [0.0202, 0.0144, 0.0363, 0.0316, 0.0308],
        "Overfit": [0.2300, 0.2300, 0.2360, 0.2398, 0.2527],
        "Eğitim Süresi (s)": [0.300, 0.260, 0.229, 3.021, 0.480]
    }
    
    top5_df = pd.DataFrame(top5_data)
    st.dataframe(top5_df, use_container_width=True, hide_index=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    st.success("""
    **✅ Final Model Seçimi: Random Forest**
    
    **Seçim Gerekçesi:**
    - En yüksek Test F1-Score (0.77)
    - Makul CV kararlılığı (std: 0.02)
    - Hızlı eğitim süresi (0.3s)
    - Ensemble yöntemi (robust)
    - ROC-AUC: 0.83 (iyi ayırma gücü)
    """)
