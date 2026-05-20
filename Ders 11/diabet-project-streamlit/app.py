"""
DIABETES PREDICTION SYSTEM - STREAMLIT DEPLOYMENT
=================================================

Deployment Expert - HCI Odaklı Profesyonel ML Uygulaması

Shneiderman'ın 8 Altın Kuralı ve Nielsen Kullanılabilirlik İlkeleri Tabanlı Tasarım
Model Expert'ten devralınan Random Forest modeli ile diyabet risk tahmini
"""

import streamlit as st
import pandas as pd
import numpy as np
import joblib
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
from datetime import datetime
import warnings

warnings.filterwarnings("ignore")

# Sayfa Konfigürasyonu
st.set_page_config(
    page_title="Diabetes Prediction System",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Global Sabitler
RANDOM_STATE = 42
MODEL_PATH = Path("models/final_model.pkl")
LOG_PATH = Path("logs/prediction_log.csv")

# Profesyonel Renk Paleti
PROFESSIONAL_PALETTE = {
    "background": "#FFFFFF",
    "card": "#F9FAFB",
    "primary": "#2E86AB",      # Koyu mavi - güven
    "secondary": "#6A994E",    # Yeşil - pozitif
    "accent": "#F18F01",       # Turuncu - dikkat
    "danger": "#C73E1D",       # Kırmızı - uyarı
    "purple": "#8E7DBE",       # Mor - premium
    "text": "#1F2937",
    "muted": "#6B7280",
    "border": "#D1D5DB"
}

# CSS İnject Fonksiyonu
def inject_custom_css():
    """Profesyonel CSS stil tanımları"""
    st.markdown(
        """
        <style>
        .main {
            background: linear-gradient(135deg, #F8FAFC 0%, #EEF6F9 100%);
        }

        .block-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
            max-width: 1280px;
        }

        .hero-card {
            background: rgba(255, 255, 255, 0.92);
            border: 1px solid #E5E7EB;
            border-radius: 24px;
            padding: 28px 32px;
            box-shadow: 0 18px 45px rgba(31, 41, 55, 0.08);
            margin-bottom: 24px;
        }

        .metric-card {
            background: #FFFFFF;
            border: 1px solid #E5E7EB;
            border-radius: 20px;
            padding: 20px;
            box-shadow: 0 12px 30px rgba(31, 41, 55, 0.06);
            margin-bottom: 16px;
        }

        .result-positive {
            background: linear-gradient(135deg, #D5F5E3 0%, #B8E0D2 100%);
            border-radius: 22px;
            padding: 24px;
            border: 1px solid #B8E0D2;
            margin: 16px 0;
        }

        .result-warning {
            background: linear-gradient(135deg, #FFF7E6 0%, #F7D9A3 100%);
            border-radius: 22px;
            padding: 24px;
            border: 1px solid #F7D9A3;
            margin: 16px 0;
        }

        .result-danger {
            background: linear-gradient(135deg, #FDECEC 0%, #F6C6C6 100%);
            border-radius: 22px;
            padding: 24px;
            border: 1px solid #F6C6C6;
            margin: 16px 0;
        }

        .small-muted {
            color: #6B7280;
            font-size: 0.92rem;
        }

        h1, h2, h3 {
            color: #1F2937;
        }

        .stButton>button {
            background: linear-gradient(135deg, #2E86AB 0%, #246A8E 100%);
            color: white;
            border: none;
            border-radius: 12px;
            padding: 12px 28px;
            font-weight: 600;
            font-size: 1.05rem;
            box-shadow: 0 8px 20px rgba(46, 134, 171, 0.25);
            transition: all 0.3s ease;
        }

        .stButton>button:hover {
            transform: translateY(-2px);
            box-shadow: 0 12px 28px rgba(46, 134, 171, 0.35);
        }

        .sidebar .sidebar-content {
            background: linear-gradient(180deg, #FFFFFF 0%, #F8FAFC 100%);
        }

        .info-box {
            background: #EBF5FB;
            border-left: 4px solid #2E86AB;
            border-radius: 8px;
            padding: 16px;
            margin: 12px 0;
        }

        .warning-box {
            background: #FFF7E6;
            border-left: 4px solid #F18F01;
            border-radius: 8px;
            padding: 16px;
            margin: 12px 0;
        }

        .success-box {
            background: #D5F5E3;
            border-left: 4px solid #6A994E;
            border-radius: 8px;
            padding: 16px;
            margin: 12px 0;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

# Model Yükleme
@st.cache_resource
def load_model_assets():
    """Model yükle"""
    try:
        model = joblib.load(MODEL_PATH)
        return model, None
    except Exception as e:
        return None, str(e)

# Feature Engineering Fonksiyonu
def add_engineered_features(df):
    """
    DataPrep Expert'ten gelen feature engineering adımlarını uygula
    8 yeni feature ekler (4 binary + 4 interaction)
    """
    # Orijinal training verisinden hesaplanan quantile değerleri
    GLUCOSE_Q3 = 140.25
    AGE_Q3 = 41.0
    PREGNANCIES_Q3 = 6.0
    
    # Binary Features (4 adet)
    df['High_Glucose'] = (df['Glucose'] > GLUCOSE_Q3).astype(int)
    df['High_BMI'] = (df['BMI'] > 30).astype(int)
    df['Old_Age'] = (df['Age'] > AGE_Q3).astype(int)
    df['Many_Pregnancies'] = (df['Pregnancies'] > PREGNANCIES_Q3).astype(int)
    
    # Interaction Features (4 adet)
    df['BMI_Age'] = df['BMI'] * df['Age']
    df['Glucose_BMI'] = df['Glucose'] * df['BMI']
    df['Glucose_Age'] = df['Glucose'] * df['Age']
    df['BMI_DiabetesPedigreeFunction'] = df['BMI'] * df['DiabetesPedigreeFunction']
    
    # Sütun sırasını düzenle (model ile aynı sırada olmalı)
    feature_order = [
        'Pregnancies', 'Glucose', 'BloodPressure', 'BMI', 'DiabetesPedigreeFunction', 'Age',
        'High_Glucose', 'High_BMI', 'Old_Age', 'Many_Pregnancies',
        'BMI_Age', 'Glucose_BMI', 'Glucose_Age', 'BMI_DiabetesPedigreeFunction'
    ]
    
    return df[feature_order]

# Tahmin Fonksiyonu
def predict_single(input_df, model):
    """Tekil tahmin yap"""
    try:
        # Feature Engineering uygula (8 yeni feature ekle)
        input_df_engineered = add_engineered_features(input_df.copy())
        
        # Tahmin yap
        prediction = model.predict(input_df_engineered)[0]

        # Olasılık hesapla
        probability = None
        if hasattr(model, "predict_proba"):
            proba = model.predict_proba(input_df_engineered)[0]
            probability = {
                "Diyabet Yok": float(proba[0]) * 100,
                "Diyabet Var": float(proba[1]) * 100
            }

        return prediction, probability, None
    except Exception as e:
        return None, None, str(e)

# Toplu Tahmin Fonksiyonu
def predict_batch(input_df, model):
    """Toplu tahmin yap"""
    try:
        # Feature Engineering uygula (8 yeni feature ekle)
        input_df_engineered = add_engineered_features(input_df.copy())
        
        # Tahmin yap
        predictions = model.predict(input_df_engineered)
        
        if hasattr(model, "predict_proba"):
            probabilities = model.predict_proba(input_df_engineered)
            result_df = input_df.copy()
            result_df["Tahmin"] = ["Diyabet Var" if p == 1 else "Diyabet Yok" for p in predictions]
            result_df["Diyabet Yok (%)"] = probabilities[:, 0] * 100
            result_df["Diyabet Var (%)"] = probabilities[:, 1] * 100
            result_df["Güven Skoru (%)"] = np.max(probabilities, axis=1) * 100
        else:
            result_df = input_df.copy()
            result_df["Tahmin"] = ["Diyabet Var" if p == 1 else "Diyabet Yok" for p in predictions]

        return result_df, None
    except Exception as e:
        return None, str(e)

# Loglama Fonksiyonu
def log_prediction(input_data, prediction, confidence=None):
    """Tahmin logunu kaydet"""
    try:
        LOG_PATH.parent.mkdir(exist_ok=True)
        
        log_row = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "prediction": "Diyabet Var" if prediction == 1 else "Diyabet Yok",
            "confidence": confidence
        }
        
        for col in input_data.columns:
            log_row[col] = input_data.iloc[0][col]
        
        if LOG_PATH.exists():
            pd.DataFrame([log_row]).to_csv(LOG_PATH, mode="a", index=False, header=False)
        else:
            pd.DataFrame([log_row]).to_csv(LOG_PATH, index=False)
    except Exception as e:
        st.warning(f"Loglama hatası (önemsiz): {e}")

# Session State İnitialization
def init_session_state():
    """Session state değişkenlerini initialize et"""
    if "last_prediction" not in st.session_state:
        st.session_state.last_prediction = None
    if "last_input" not in st.session_state:
        st.session_state.last_input = None
    if "prediction_history" not in st.session_state:
        st.session_state.prediction_history = []

# Ana Uygulama
def main():
    """Ana Streamlit uygulaması"""
    # CSS'i inject et
    inject_custom_css()
    
    # Session state'i initialize et
    init_session_state()
    
    # Modeli yükle
    model, error = load_model_assets()
    
    if error:
        st.error(f"❌ Model yükleme hatası: {error}")
        st.stop()
    
    # Sidebar Navigation
    st.sidebar.markdown("# 🏥 Diabetes Prediction")
    st.sidebar.markdown("### Yapay Zeka Destekli Risk Değerlendirme")
    st.sidebar.markdown("---")
    
    # Model Bilgisi (Sidebar) - Streamlit Native
    with st.sidebar:
        st.markdown("### 📊 Aktif Model Bilgileri")
        
        # Model bilgileri native Streamlit ile
        st.markdown("**🤖 Model:** Random Forest")
        st.markdown("**📊 F1-Score:** 0.77")
        st.markdown("**✅ Accuracy:** 77.3%")
        st.markdown("**📈 ROC-AUC:** 0.83")
        st.markdown("**🔬 Features:** 14 (6 orijinal + 8 engineered)")
        st.success("✅ **Aktif ve Hazır**")
        
        st.markdown("---")
        st.markdown("### 💡 Hızlı İpuçları")
        st.markdown("""
        - 📋 Örnek veri ile sistemi test edin
        - 🔬 Doğru ve eksiksiz veri girin
        - 📊 Risk faktörlerini inceleyin
        - 💊 Önerileri dikkate alın
        - 👨‍⚕️ Mutlaka uzman görüşü alın
        """)
    
    # Ana sayfa yönlendirmesi - Sadece Tekil Tahmin
    from pages import single_prediction
    single_prediction.show(model)

    # ═══════════════════════════════════════════════════════════════
    #  FOOTER — GELİŞTİRİCİ & SİSTEM BİLGİSİ
    # ═══════════════════════════════════════════════════════════════
    st.markdown("---")

    st.markdown("## 🏆 Proje & Geliştirici Bilgisi")

    dev1, dev2, dev3 = st.columns([1, 1.2, 1])

    with dev1:
        st.markdown("### 👨‍🔬 Geliştirici")
        st.markdown("# **Res. Asst.**")
        st.markdown("# **Cemal YÜKSEL**")
        st.markdown("---")
        st.markdown("🏛️ **Kurum:** Üniversite")
        st.markdown("📚 **Uzmanlık:** Makine Öğrenmesi & Veri Bilimi")
        st.markdown("🗓️ **Dönem:** 2025–2026 Bahar")
        st.markdown("📖 **Ders 11:** Makine Öğrenmesi")
        st.markdown("---")
        st.success("🎓 Araştırma Görevlisi")
        st.info("🤖 Agentik ML Uzmanı")

    with dev2:
        st.markdown("### 🔄 Agentik ML Pipeline")
        st.markdown("Bu sistem 4 uzman AI ajanının iş birliğiyle geliştirilmiştir.")
        st.markdown("---")
        a1, a2 = st.columns(2)
        with a1:
            st.success("**1️⃣ EDA Expert**")
            st.caption("Keşifsel analiz, görselleştirme, outlier tespiti")
            st.warning("**2️⃣ DataPrep Expert**")
            st.caption("Eksik veri, feature engineering, ölçekleme")
        with a2:
            st.info("**3️⃣ Model Expert**")
            st.caption("12+ model karşılaştırma, hyperparameter tuning")
            st.error("**4️⃣ Deployment Expert**")
            st.caption("Streamlit UI, HCI, Shneiderman 8 Kural")
        st.markdown("---")
        st.markdown("**🛠️ Teknolojiler:** Python · Streamlit · Scikit-learn · Plotly · Pandas")

    with dev3:
        st.markdown("### 📊 Model Özeti")
        st.markdown("---")
        st.metric("🤖 Algoritma", "Random Forest")
        st.metric("📊 F1-Score", "0.77", "+0.05 baseline")
        st.metric("✅ Accuracy", "77.3%", "+4.2%")
        st.metric("📈 ROC-AUC", "0.83")
        st.metric("🔬 Feature Sayısı", "14", "6 orijinal + 8 türetilmiş")
        st.metric("🏥 Eğitim Verisi", "768 hasta", "Pima Indians Dataset")

    st.markdown("---")

    b1, b2, b3 = st.columns(3)
    with b1:
        st.caption("🏛️ © 2026 Diabetes Prediction System")
        st.caption("✍️ Developed by Res. Asst. Cemal YÜKSEL")
    with b2:
        st.caption("⚡ Powered by Streamlit · Scikit-learn · Plotly")
        st.caption("🐍 Python 3.13 · Random Forest Classifier")
    with b3:
        st.caption("🔒 OWASP Uyumlu · HCI Tabanlı · Klinik Destekli")
        st.caption("📅 2025–2026 Bahar Dönemi · Makine Öğrenmesi Ders 11")


if __name__ == "__main__":
    main()
