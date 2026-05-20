"""
🎯 Telekom Müşteri Churn Risk Değerlendirme Platformu
Wizard Yaklaşımı + Apple Bento Grid Tasarımı
HCI İlkeleri ve Shneiderman'ın 8 Altın Kuralı Uygulamalı
"""

import streamlit as st
import pandas as pd
import numpy as np
import joblib
import plotly.graph_objects as go
import plotly.express as px
from pathlib import Path
from datetime import datetime

# ============================================================================
# SAYFA KONFIGÜRASYONU
# ============================================================================

st.set_page_config(
    page_title="Churn Risk Değerlendirme",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ============================================================================
# SABITLER VE RENKLER (APPLE BENTO STYLE)
# ============================================================================

RANDOM_STATE = 42

# Apple-inspired Premium Palette (görkemli, modern)
COLORS = {
    # Ana renkler
    "primary": "#007AFF",        # Apple Blue
    "secondary": "#34C759",      # Apple Green
    "danger": "#FF3B30",         # Apple Red
    "warning": "#FF9500",        # Apple Orange
    "purple": "#AF52DE",         # Apple Purple
    "teal": "#5AC8FA",           # Apple Teal
    
    # Arka plan ve kartlar
    "bg_primary": "#F5F5F7",     # Apple Light Gray
    "bg_card": "#FFFFFF",
    "bg_hero": "rgba(255, 255, 255, 0.85)",
    
    # Metin
    "text_primary": "#1D1D1F",
    "text_secondary": "#86868B",
    "text_muted": "#6E6E73",
    
    # Glassmorphism
    "glass": "rgba(255, 255, 255, 0.7)",
    "glass_border": "rgba(255, 255, 255, 0.3)",
    
    # Gradient'ler
    "gradient_blue": "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
    "gradient_green": "linear-gradient(135deg, #84fab0 0%, #8fd3f4 100%)",
    "gradient_orange": "linear-gradient(135deg, #fa709a 0%, #fee140 100%)",
    "gradient_purple": "linear-gradient(135deg, #a8edea 0%, #fed6e3 100%)",
}

# Model paths
MODEL_PATH = Path("models/final_model.pkl")
PIPELINE_PATH = Path("models/preprocessing_pipeline.pkl")

# ============================================================================
# APPLE BENTO GRID CSS - GÖRKEMLI TASARIM
# ============================================================================

def inject_apple_bento_css():
    st.markdown(
        f"""
        <style>
        /* Ana Sayfa Arka Planı - Canlı Gradient */
        .main {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 25%, #f093fb 50%, #4facfe 100%);
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, sans-serif;
            animation: gradientShift 15s ease infinite;
            background-size: 400% 400%;
        }}
        
        @keyframes gradientShift {{
            0% {{ background-position: 0% 50%; }}
            50% {{ background-position: 100% 50%; }}
            100% {{ background-position: 0% 50%; }}
        }}
        
        /* Streamlit Container */
        .block-container {{
            padding-top: 3rem;
            padding-bottom: 3rem;
            max-width: 1400px;
        }}
        
        /* Hero Card - Glassmorphism Effect */
        .hero-card {{
            background: linear-gradient(135deg, rgba(255,255,255,0.95) 0%, rgba(255,255,255,0.85) 100%);
            backdrop-filter: blur(30px);
            -webkit-backdrop-filter: blur(30px);
            border: 2px solid rgba(255, 255, 255, 0.5);
            border-radius: 32px;
            padding: 48px 56px;
            box-shadow: 0 30px 70px rgba(102, 126, 234, 0.25),
                        0 15px 40px rgba(118, 75, 162, 0.15);
            margin-bottom: 32px;
            transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
            position: relative;
            overflow: hidden;
        }}
        
        .hero-card::before {{
            content: '';
            position: absolute;
            top: -50%;
            left: -50%;
            width: 200%;
            height: 200%;
            background: linear-gradient(45deg, transparent, rgba(102, 126, 234, 0.1), transparent);
            transform: rotate(45deg);
            animation: shimmer 3s infinite;
        }}
        
        @keyframes shimmer {{
            0% {{ transform: translateX(-100%) translateY(-100%) rotate(45deg); }}
            100% {{ transform: translateX(100%) translateY(100%) rotate(45deg); }}
        }}
        
        .hero-card:hover {{
            transform: translateY(-8px);
            box-shadow: 0 35px 90px rgba(102, 126, 234, 0.35),
                        0 20px 50px rgba(118, 75, 162, 0.25);
            border-color: rgba(255, 255, 255, 0.8);
        }}
        
        /* Bento Grid Card - Görkemli Style */
        .bento-card {{
            background: linear-gradient(135deg, rgba(255,255,255,0.98) 0%, rgba(255,255,255,0.92) 100%);
            border-radius: 24px;
            padding: 28px 32px;
            box-shadow: 0 12px 40px rgba(102, 126, 234, 0.12),
                        0 5px 15px rgba(118, 75, 162, 0.08);
            border: 2px solid rgba(255, 255, 255, 0.6);
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            margin-bottom: 20px;
            backdrop-filter: blur(10px);
        }}
        
        .bento-card:hover {{
            transform: translateY(-5px) scale(1.01);
            box-shadow: 0 18px 50px rgba(102, 126, 234, 0.18),
                        0 8px 20px rgba(118, 75, 162, 0.12);
            border-color: rgba(102, 126, 234, 0.3);
        }}
        
        /* Progress Bar - Apple Style */
        .progress-container {{
            background: {COLORS['bg_card']};
            border-radius: 20px;
            padding: 32px 40px;
            box-shadow: 0 8px 28px rgba(0, 0, 0, 0.08);
            margin-bottom: 32px;
        }}
        
        .progress-steps {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            position: relative;
            margin-bottom: 12px;
        }}
        
        .progress-line {{
            position: absolute;
            top: 20px;
            left: 0;
            right: 0;
            height: 3px;
            background: linear-gradient(90deg, 
                {COLORS['primary']} 0%, 
                {COLORS['teal']} 50%, 
                {COLORS['secondary']} 100%);
            z-index: 0;
            opacity: 0.3;
        }}
        
        .progress-step {{
            width: 44px;
            height: 44px;
            border-radius: 50%;
            background: {COLORS['bg_card']};
            border: 3px solid #E5E5EA;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: 700;
            font-size: 16px;
            color: {COLORS['text_secondary']};
            position: relative;
            z-index: 1;
            transition: all 0.3s ease;
        }}
        
        .progress-step.active {{
            background: {COLORS['primary']};
            border-color: {COLORS['primary']};
            color: white;
            transform: scale(1.15);
            box-shadow: 0 8px 20px rgba(0, 122, 255, 0.35);
        }}
        
        .progress-step.completed {{
            background: {COLORS['secondary']};
            border-color: {COLORS['secondary']};
            color: white;
            box-shadow: 0 5px 15px rgba(52, 199, 89, 0.3);
        }}
        
        .step-label {{
            font-size: 13px;
            color: {COLORS['text_secondary']};
            margin-top: 8px;
            text-align: center;
            font-weight: 500;
        }}
        
        .step-label.active {{
            color: {COLORS['primary']};
            font-weight: 700;
        }}
        
        /* Result Card - Risk Level Based */
        .result-card {{
            border-radius: 28px;
            padding: 40px 48px;
            margin: 24px 0;
            box-shadow: 0 20px 50px rgba(0, 0, 0, 0.1);
            position: relative;
            overflow: hidden;
        }}
        
        .result-card::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 6px;
        }}
        
        .result-low {{
            background: linear-gradient(135deg, #d4fc79 0%, #96e6a1 100%);
            border: 2px solid rgba(52, 199, 89, 0.3);
        }}
        
        .result-low::before {{
            background: linear-gradient(90deg, #34C759 0%, #30D158 100%);
        }}
        
        .result-medium {{
            background: linear-gradient(135deg, #ffeaa7 0%, #fdcb6e 100%);
            border: 2px solid rgba(255, 149, 0, 0.3);
        }}
        
        .result-medium::before {{
            background: linear-gradient(90deg, #FF9500 0%, #FFAA00 100%);
        }}
        
        .result-high {{
            background: linear-gradient(135deg, #ff9a9e 0%, #fecfef 100%);
            border: 2px solid rgba(255, 59, 48, 0.3);
        }}
        
        .result-high::before {{
            background: linear-gradient(90deg, #FF3B30 0%, #FF6B6B 100%);
        }}
        
        /* Metric Card - Görkemli Style */
        .metric-bento {{
            background: linear-gradient(135deg, rgba(255,255,255,0.95) 0%, rgba(255,255,255,0.85) 100%);
            border-radius: 22px;
            padding: 28px;
            text-align: center;
            box-shadow: 0 10px 35px rgba(102, 126, 234, 0.15);
            transition: all 0.3s ease;
            border: 2px solid rgba(255, 255, 255, 0.5);
            backdrop-filter: blur(10px);
        }}
        
        .metric-bento:hover {{
            transform: translateY(-6px) scale(1.03);
            box-shadow: 0 15px 45px rgba(102, 126, 234, 0.25);
            border-color: rgba(102, 126, 234, 0.4);
        }}
        
        .metric-value {{
            font-size: 42px;
            font-weight: 800;
            line-height: 1.2;
            margin: 12px 0;
            text-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        }}
        
        .metric-label {{
            font-size: 14px;
            color: #1D1D1F;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.8px;
            text-shadow: 0 1px 2px rgba(255, 255, 255, 0.8);
        }}
        
        /* Buttons - Görkemli Style - Maximum Kontrast */
        .stButton > button {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
            color: #FFFFFF !important;
            border: none;
            border-radius: 16px;
            padding: 20px 36px;
            font-size: 18px;
            font-weight: 900 !important;
            transition: all 0.3s ease;
            box-shadow: 0 12px 35px rgba(102, 126, 234, 0.6);
            position: relative;
            overflow: hidden;
            text-shadow: 0 4px 8px rgba(0, 0, 0, 0.5), 0 2px 4px rgba(0, 0, 0, 0.7) !important;
            letter-spacing: 0.4px;
            line-height: 1.5;
        }}
        
        .stButton > button * {{
            color: #FFFFFF !important;
            text-shadow: 0 4px 8px rgba(0, 0, 0, 0.5), 0 2px 4px rgba(0, 0, 0, 0.7) !important;
        }}
        
        .stButton > button::before {{
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255,255,255,0.3), transparent);
            transition: left 0.5s;
        }}
        
        .stButton > button:hover {{
            background: linear-gradient(135deg, #764ba2 0%, #667eea 100%) !important;
            transform: translateY(-3px) scale(1.02);
            box-shadow: 0 15px 40px rgba(102, 126, 234, 0.5);
            color: #FFFFFF !important;
        }}
        
        .stButton > button:hover * {{
            color: #FFFFFF !important;
        }}
        
        .stButton > button:hover::before {{
            left: 100%;
        }}
        
        .stButton > button:active {{
            transform: translateY(-1px) scale(0.98);
        }}
        
        /* Download Button - Yüksek Kontrast */
        .stDownloadButton > button {{
            background: linear-gradient(135deg, #34C759 0%, #30D158 100%) !important;
            color: #FFFFFF !important;
            border: none;
            border-radius: 16px;
            padding: 20px 36px;
            font-size: 18px;
            font-weight: 900 !important;
            transition: all 0.3s ease;
            box-shadow: 0 12px 35px rgba(52, 199, 89, 0.6);
            text-shadow: 0 4px 8px rgba(0, 0, 0, 0.5), 0 2px 4px rgba(0, 0, 0, 0.7) !important;
            letter-spacing: 0.4px;
        }}
        
        .stDownloadButton > button * {{
            color: #FFFFFF !important;
            text-shadow: 0 4px 8px rgba(0, 0, 0, 0.5), 0 2px 4px rgba(0, 0, 0, 0.7) !important;
        }}
        
        .stDownloadButton > button:hover {{
            background: linear-gradient(135deg, #30D158 0%, #34C759 100%) !important;
            transform: translateY(-3px) scale(1.02);
            box-shadow: 0 15px 40px rgba(52, 199, 89, 0.5);
            color: #FFFFFF !important;
        }}
        
        .stDownloadButton > button:hover * {{
            color: #FFFFFF !important;
        }}
        
        /* Typography */
        h1 {{
            color: {COLORS['text_primary']};
            font-weight: 800;
            font-size: 52px;
            letter-spacing: -1px;
            margin-bottom: 16px;
        }}
        
        h2 {{
            color: {COLORS['text_primary']};
            font-weight: 700;
            font-size: 36px;
            margin-top: 32px;
            margin-bottom: 20px;
        }}
        
        h3 {{
            color: {COLORS['text_primary']};
            font-weight: 700;
            font-size: 24px;
            margin-bottom: 12px;
        }}
        
        p {{
            color: {COLORS['text_secondary']};
            font-size: 17px;
            line-height: 1.6;
        }}
        
        /* Input Labels - Yüksek Kontrast */
        label, .stSelectbox label, .stNumberInput label, .stSlider label {{
            color: #1D1D1F !important;
            font-weight: 600 !important;
            font-size: 16px !important;
            text-shadow: 0 1px 2px rgba(255, 255, 255, 0.8);
        }}
        
        .big-emoji {{
            font-size: 72px;
            margin: 20px 0;
            display: block;
            text-align: center;
        }}
        
        /* Input Fields - Apple Style */
        .stSelectbox, .stNumberInput, .stRadio {{
            margin-bottom: 20px;
        }}
        
        .stSelectbox > div > div {{
            border-radius: 12px;
            border: 1.5px solid #E5E5EA;
            transition: all 0.3s ease;
        }}
        
        .stSelectbox > div > div:focus-within {{
            border-color: {COLORS['primary']};
            box-shadow: 0 0 0 4px rgba(0, 122, 255, 0.1);
        }}
        
        /* Action Card */
        .action-card {{
            background: {COLORS['bg_card']};
            border-radius: 20px;
            padding: 24px 28px;
            margin: 16px 0;
            border-left: 5px solid {COLORS['secondary']};
            box-shadow: 0 6px 20px rgba(0, 0, 0, 0.05);
        }}
        
        .action-icon {{
            font-size: 32px;
            margin-right: 12px;
        }}
        
        /* Badge */
        .badge {{
            display: inline-block;
            padding: 6px 16px;
            border-radius: 20px;
            font-size: 13px;
            font-weight: 700;
            letter-spacing: 0.3px;
        }}
        
        .badge-success {{
            background: {COLORS['secondary']};
            color: white;
        }}
        
        .badge-warning {{
            background: {COLORS['warning']};
            color: white;
        }}
        
        .badge-danger {{
            background: {COLORS['danger']};
            color: white;
        }}
        
        /* Animation */
        @keyframes fadeInUp {{
            from {{
                opacity: 0;
                transform: translateY(20px);
            }}
            to {{
                opacity: 1;
                transform: translateY(0);
            }}
        }}
        
        .animate-in {{
            animation: fadeInUp 0.6s ease-out;
        }}
        
        /* Hide Streamlit Branding */
        #MainMenu {{visibility: hidden;}}
        footer {{visibility: hidden;}}
        header {{visibility: hidden;}}
        
        </style>
        """,
        unsafe_allow_html=True
    )

# ============================================================================
# MODEL YÜKLEME
# ============================================================================

@st.cache_resource
def load_model_assets():
    """Model ve preprocessing pipeline'ı yükle"""
    try:
        model = joblib.load(MODEL_PATH)
        pipeline = joblib.load(PIPELINE_PATH) if PIPELINE_PATH.exists() else None
        return model, pipeline, None
    except Exception as e:
        return None, None, str(e)

# ============================================================================
# SESSION STATE İNİTİALİZASYON
# ============================================================================

def init_session_state():
    """Session state değişkenlerini başlat (Shneiderman Kural 6: Geri Alma)"""
    
    if "current_step" not in st.session_state:
        st.session_state.current_step = 1
    
    if "form_data" not in st.session_state:
        st.session_state.form_data = {}
    
    if "prediction_result" not in st.session_state:
        st.session_state.prediction_result = None
    
    if "prediction_history" not in st.session_state:
        st.session_state.prediction_history = []

def reset_form():
    """Formu sıfırla (Shneiderman Kural 6: Geri Alma)"""
    st.session_state.current_step = 1
    st.session_state.form_data = {}
    st.session_state.prediction_result = None

# ============================================================================
# PROGRESS BAR (APPLE STYLE)
# ============================================================================

def render_progress_bar(current_step):
    """Apple tarzı progress bar göster - Tamamen Düzeltilmiş"""
    
    steps = [
        {"num": 1, "label": "Profil", "emoji": "👤"},
        {"num": 2, "label": "Hizmetler", "emoji": "📱"},
        {"num": 3, "label": "Sözleşme", "emoji": "📄"},
        {"num": 4, "label": "Sonuç", "emoji": "🎯"},
        {"num": 5, "label": "Aksiyon", "emoji": "💡"}
    ]
    
    progress_percent = (current_step / len(steps)) * 100
    
    # Adımlar için kompakt HTML
    steps_parts = []
    for step in steps:
        if step["num"] <= current_step:
            bg = "linear-gradient(135deg, #667eea 0%, #764ba2 100%)"
            shadow = "0 8px 25px rgba(102, 126, 234, 0.4)" if step["num"] == current_step else "0 4px 15px rgba(102, 126, 234, 0.2)"
            scale = "scale(1.15)" if step["num"] == current_step else "scale(1)"
            icon = step["emoji"]
        else:
            bg = "#E5E5EA"
            shadow = "none"
            scale = "scale(1)"
            icon = str(step["num"])
        
        fw = "700" if step["num"] == current_step else "500"
        color = "#667eea" if step["num"] == current_step else "#6E6E73"
        icon_color = "white" if step["num"] <= current_step else "#1D1D1F"
        
        step_html = f'<div style="text-align:center;flex:1"><div style="width:50px;height:50px;margin:0 auto;border-radius:50%;background:{bg};display:flex;align-items:center;justify-content:center;color:{icon_color};font-size:24px;font-weight:800;box-shadow:{shadow};transform:{scale};transition:all 0.3s ease">{icon}</div><div style="margin-top:10px;font-size:13px;font-weight:{fw};color:{color}">{step["label"]}</div></div>'
        steps_parts.append(step_html)
    
    all_steps = "".join(steps_parts)
    
    html = f'<div style="background:rgba(255,255,255,0.95);border-radius:20px;padding:30px 40px;box-shadow:0 10px 40px rgba(0,0,0,0.15);margin-bottom:30px"><div style="display:flex;justify-content:space-between;margin-bottom:15px">{all_steps}</div><div style="width:100%;height:8px;background:#E5E5EA;border-radius:10px;overflow:hidden"><div style="width:{progress_percent}%;height:100%;background:linear-gradient(90deg,#667eea 0%,#764ba2 50%,#f093fb 100%);transition:width 0.5s ease"></div></div><div style="text-align:center;margin-top:12px;color:#667eea;font-weight:600;font-size:15px">Adım {current_step}/{len(steps)} - {int(progress_percent)}% Tamamlandı</div></div>'
    
    st.markdown(html, unsafe_allow_html=True)

# ============================================================================
# ADIM 1: MÜŞTERİ PROFİLİ
# ============================================================================

def step_1_customer_profile():
    """Adım 1: Müşteri Profil Bilgileri"""
    
    st.markdown('<div class="bento-card animate-in">', unsafe_allow_html=True)
    st.markdown("""
    <h2 style="color: #667eea;
               margin-bottom: 8px;
               font-weight: 800;
               text-shadow: 0 2px 4px rgba(102, 126, 234, 0.3);">
        👤 Müşteri Profil Bilgileri
    </h2>
    <p style="color: #6E6E73; font-size: 16px;">Müşterinin demografik bilgilerini girin.</p>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="bento-card">', unsafe_allow_html=True)
        gender = st.selectbox(
            "Cinsiyet",
            ["Male", "Female"],
            help="📊 Müşterinin cinsiyeti. Cinsiyet bazlı churn oranları farklılık gösterebilir ve demografik segmentasyon için önemlidir."
        )
        
        senior_citizen = st.selectbox(
            "Yaşlı Vatandaş (65+)",
            [0, 1],
            format_func=lambda x: "Evet" if x == 1 else "Hayır",
            help="👴 65 yaş üstü müşterilerin hizmet kullanım alışkanlıkları ve sadakat davranışları genç müşterilerden farklı olabilir. Yaş segmentasyonu risk modellemesinde kritik rol oynar."
        )
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="bento-card">', unsafe_allow_html=True)
        partner = st.selectbox(
            "Eşi/Partneri Var Mı?",
            ["Yes", "No"],
            format_func=lambda x: "Evet" if x == "Yes" else "Hayır",
            help="👥 Partneri olan müşterilerin churn riski genellikle %18-25 daha düşüktür. Aile bağları müşteri sadakatini güçlendirir ve hizmet değiştirme eğilimini azaltır."
        )
        
        dependents = st.selectbox(
            "Bakmakla Yükümlü Olduğu Kişi Var Mı?",
            ["Yes", "No"],
            format_func=lambda x: "Evet" if x == "Yes" else "Hayır",
            help="👶 Bakmakla yükümlü kişisi olan müşteriler (çocuk, yaşlı ebeveyn vb.) daha istikrarlı hizmet kullanım profili gösterir. Ailevi sorumluluklar churn oranını %20-30 azaltabilir."
        )
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="bento-card">', unsafe_allow_html=True)
    tenure = st.slider(
        "Müşteri Süresi (Ay)",
        min_value=0,
        max_value=72,
        value=12,
        help="⏱️ Müşteri süreklilik süresi en kritik risk faktörüdür. İlk 6 ay %45 churn riski taşırken, 24+ ay müşterilerde bu oran %8'e düşer. Yeni müşterilere özel onboarding programları önerilir."
    )
    st.markdown('</div>', unsafe_allow_html=True)
    
    # İleri butonu
    st.markdown("<br>", unsafe_allow_html=True)
    col_btn1, col_btn2, col_btn3 = st.columns([1, 1, 1])
    
    with col_btn2:
        if st.button("Devam Et: Hizmetler Seçimi ➡️", use_container_width=True, type="primary"):
            # Veriyi kaydet
            st.session_state.form_data["gender"] = gender
            st.session_state.form_data["SeniorCitizen"] = senior_citizen
            st.session_state.form_data["Partner"] = partner
            st.session_state.form_data["Dependents"] = dependents
            st.session_state.form_data["tenure"] = tenure
            
            # Sonraki adıma geç
            st.session_state.current_step = 2
            st.rerun()

# ============================================================================
# ADIM 2: HİZMET PAKETİ
# ============================================================================

def step_2_service_package():
    """Adım 2: Hizmet Paketi Seçimi"""
    
    st.markdown('<div class="bento-card animate-in">', unsafe_allow_html=True)
    st.markdown("""
    <h2 style="color: #f093fb;
               margin-bottom: 8px;
               font-weight: 800;
               text-shadow: 0 2px 4px rgba(240, 147, 251, 0.3);">
        📱 Hizmet Paketi
    </h2>
    <p style="color: #6E6E73; font-size: 16px;">Müşterinin kullandığı hizmetleri seçin.</p>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Telefon Hizmetleri
    st.markdown('<div class="bento-card">', unsafe_allow_html=True)
    st.markdown("""
    <h3 style="color: #667eea;
               font-weight: 800;
               text-shadow: 0 2px 4px rgba(102, 126, 234, 0.3);">
        ☎️ Telefon Hizmetleri
    </h3>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        phone_service = st.selectbox(
            "Telefon Hizmeti",
            ["Yes", "No"],
            format_func=lambda x: "Var" if x == "Yes" else "Yok"
        )
    
    with col2:
        if phone_service == "Yes":
            multiple_lines = st.selectbox(
                "Birden Fazla Hat",
                ["Yes", "No"],
                format_func=lambda x: "Var" if x == "Yes" else "Yok"
            )
        else:
            multiple_lines = "No phone service"
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # İnternet Hizmetleri
    st.markdown('<div class="bento-card">', unsafe_allow_html=True)
    st.markdown("""
    <h3 style="color: #4facfe;
               font-weight: 800;
               text-shadow: 0 2px 4px rgba(79, 172, 254, 0.3);">
        🌐 İnternet Hizmetleri
    </h3>
    """, unsafe_allow_html=True)
    
    internet_service = st.selectbox(
        "İnternet Hizmeti",
        ["DSL", "Fiber optic", "No"],
        format_func=lambda x: "DSL" if x == "DSL" else ("Fiber" if x == "Fiber optic" else "Yok")
    )
    
    if internet_service != "No":
        col3, col4 = st.columns(2)
        
        with col3:
            online_security = st.selectbox(
                "Online Güvenlik",
                ["Yes", "No"],
                format_func=lambda x: "Var" if x == "Yes" else "Yok"
            )
            
            online_backup = st.selectbox(
                "Online Yedekleme",
                ["Yes", "No"],
                format_func=lambda x: "Var" if x == "Yes" else "Yok"
            )
            
            device_protection = st.selectbox(
                "Cihaz Koruma",
                ["Yes", "No"],
                format_func=lambda x: "Var" if x == "Yes" else "Yok"
            )
        
        with col4:
            tech_support = st.selectbox(
                "Teknik Destek",
                ["Yes", "No"],
                format_func=lambda x: "Var" if x == "Yes" else "Yok"
            )
            
            streaming_tv = st.selectbox(
                "TV Streaming",
                ["Yes", "No"],
                format_func=lambda x: "Var" if x == "Yes" else "Yok"
            )
            
            streaming_movies = st.selectbox(
                "Film Streaming",
                ["Yes", "No"],
                format_func=lambda x: "Var" if x == "Yes" else "Yok"
            )
    else:
        online_security = "No internet service"
        online_backup = "No internet service"
        device_protection = "No internet service"
        tech_support = "No internet service"
        streaming_tv = "No internet service"
        streaming_movies = "No internet service"
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Butonlar
    st.markdown("<br>", unsafe_allow_html=True)
    col_btn1, col_btn2, col_btn3 = st.columns([1, 1, 1])
    
    with col_btn1:
        if st.button("⬅️ Profil Bilgilerine Dön", use_container_width=True):
            st.session_state.current_step = 1
            st.rerun()
    
    with col_btn3:
        if st.button("Devam Et: Sözleşme & Ödeme ➡️", use_container_width=True, type="primary"):
            # Veriyi kaydet
            st.session_state.form_data["PhoneService"] = phone_service
            st.session_state.form_data["MultipleLines"] = multiple_lines
            st.session_state.form_data["InternetService"] = internet_service
            st.session_state.form_data["OnlineSecurity"] = online_security
            st.session_state.form_data["OnlineBackup"] = online_backup
            st.session_state.form_data["DeviceProtection"] = device_protection
            st.session_state.form_data["TechSupport"] = tech_support
            st.session_state.form_data["StreamingTV"] = streaming_tv
            st.session_state.form_data["StreamingMovies"] = streaming_movies
            
            # Sonraki adıma geç
            st.session_state.current_step = 3
            st.rerun()

# ============================================================================
# ADIM 3: SÖZLEŞME & ÖDEME
# ============================================================================

def step_3_contract_payment():
    """Adım 3: Sözleşme ve Ödeme Bilgileri"""
    
    st.markdown('<div class="bento-card animate-in">', unsafe_allow_html=True)
    st.markdown("""
    <h2 style="color: #4facfe;
               margin-bottom: 8px;
               font-weight: 800;
               text-shadow: 0 2px 4px rgba(79, 172, 254, 0.3);">
        📄 Sözleşme & Ödeme
    </h2>
    <p style="color: #6E6E73; font-size: 16px;">Sözleşme tipi ve ödeme yöntemi bilgilerini girin.</p>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="bento-card">', unsafe_allow_html=True)
        contract = st.selectbox(
            "Sözleşme Tipi",
            ["Month-to-month", "One year", "Two year"],
            format_func=lambda x: {
                "Month-to-month": "Aylık",
                "One year": "1 Yıl",
                "Two year": "2 Yıl"
            }[x],
            help="📋 Sözleşme tipi en güçlü tahmin edicidir. Aylık sözleşmelerde churn riski %42, 1 yıllıkta %11, 2 yıllıkta ise sadece %3'tür. Uzun vadeli sözleşmeler müşteri tutma garantisi sağlar."
        )
        
        paperless_billing = st.selectbox(
            "Kağıtsız Fatura",
            ["Yes", "No"],
            format_func=lambda x: "Evet" if x == "Yes" else "Hayır",
            help="🌱 Dijital fatura kullanan müşteriler genellikle teknolojiye daha yakındır. Kağıtsız fatura kullanımı çevre bilinci ve maliyet optimizasyonu için önerilir."
        )
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="bento-card">', unsafe_allow_html=True)
        payment_method = st.selectbox(
            "Ödeme Yöntemi",
            ["Electronic check", "Mailed check", "Bank transfer (automatic)", "Credit card (automatic)"],
            format_func=lambda x: {
                "Electronic check": "Elektronik Çek",
                "Mailed check": "Posta ile Çek",
                "Bank transfer (automatic)": "Otomatik Banka Transferi",
                "Credit card (automatic)": "Otomatik Kredi Kartı"
            }[x],
            help="💳 Otomatik ödeme yöntemleri (banka transferi, kredi kartı) %35 daha düşük churn oranına sahiptir. Manuel ödemeler ödeme sürecinde sürtünme yaratır ve müşteri kaybına yol açabilir."
        )
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="bento-card">', unsafe_allow_html=True)
    st.markdown("### 💰 Ücretlendirme")
    
    col3, col4 = st.columns(2)
    
    with col3:
        monthly_charges = st.number_input(
            "Aylık Ücret ($)",
            min_value=0.0,
            max_value=150.0,
            value=50.0,
            step=5.0,
            help="💰 Aylık ücret tutarı fiyat hassasiyetini gösterir. $80+ ödemeler yapan müşterilerde churn riski %28 artar. Fiyat optimizasyonu ve değer algısı yönetimi kritiktir."
        )
    
    with col4:
        # TotalCharges otomatik hesaplama
        tenure = st.session_state.form_data.get("tenure", 12)
        total_charges = tenure * monthly_charges
        st.metric("Toplam Ödeme (Tahmini)", f"${total_charges:.2f}")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Butonlar
    st.markdown("<br>", unsafe_allow_html=True)
    col_btn1, col_btn2, col_btn3 = st.columns([1, 1, 1])
    
    with col_btn1:
        if st.button("⬅️ Hizmet Seçimine Dön", use_container_width=True):
            st.session_state.current_step = 2
            st.rerun()
    
    with col_btn3:
        if st.button("🎯 Risk Analizi Yap", use_container_width=True, type="primary"):
            # Veriyi kaydet
            st.session_state.form_data["Contract"] = contract
            st.session_state.form_data["PaperlessBilling"] = paperless_billing
            st.session_state.form_data["PaymentMethod"] = payment_method
            st.session_state.form_data["MonthlyCharges"] = monthly_charges
            st.session_state.form_data["TotalCharges"] = total_charges
            
            # Tahmin yap
            success = make_prediction()
            
            # Sadece başarılı ise sonraki adıma geç
            if success:
                st.session_state.current_step = 4
                st.rerun()
            else:
                st.warning("⚠️ Tahmin yapılamadı. Lütfen hata mesajlarını kontrol edin ve tekrar deneyin.")

# ============================================================================
# PREPROCESSING FONKSİYONU
# ============================================================================

def preprocess_input(raw_data, pipeline_dict):
    """
    Ham form verisini model için hazırla
    
    Args:
        raw_data: dict - Ham form verisi
        pipeline_dict: dict - Pipeline bilgileri (scaler, numeric_cols, feature_names)
    
    Returns:
        numpy array - Modele hazır işlenmiş veri
    """
    import numpy as np
    
    # DataFrame'e çevir
    df = pd.DataFrame([raw_data]).copy()
    
    # Binary encoding: Yes/No -> 1/0
    binary_cols = ['SeniorCitizen', 'Partner', 'Dependents', 'PhoneService', 'PaperlessBilling']
    for col in binary_cols:
        if col in df.columns:
            df[col] = df[col].map({'Yes': 1, 'No': 0}).fillna(0)
        else:
            df[col] = 0
    
    # Gender encoding: Male -> 1, Female -> 0
    if 'gender' in df.columns:
        df['gender'] = df['gender'].map({'Male': 1, 'Female': 0}).fillna(0)
    else:
        df['gender'] = 0
    
    # Feature Engineering
    tenure = df.get('tenure', 12).iloc[0] if 'tenure' in df.columns else 12
    if pd.isna(tenure):
        tenure = 12
    
    # 1. is_new_customer
    df['is_new_customer'] = int(tenure <= 6)
    
    # 2. total_services_count
    service_cols = ['PhoneService', 'MultipleLines', 'InternetService', 
                    'OnlineSecurity', 'OnlineBackup', 'DeviceProtection', 
                    'TechSupport', 'StreamingTV', 'StreamingMovies']
    services_count = 0
    for col in service_cols:
        if col in df.columns:
            val = df[col].iloc[0]
            if val not in ['No', 'No internet service', 'No phone service', 0]:
                services_count += 1
    df['total_services_count'] = services_count
    
    # 3. is_fiber_customer
    internet_service = df.get('InternetService', 'No').iloc[0] if 'InternetService' in df.columns else 'No'
    df['is_fiber_customer'] = int(internet_service == 'Fiber optic')
    
    # 4. is_auto_pay
    payment_method = df.get('PaymentMethod', 'Electronic check').iloc[0] if 'PaymentMethod' in df.columns else 'Electronic check'
    df['is_auto_pay'] = int(payment_method in ['Bank transfer (automatic)', 'Credit card (automatic)'])
    
    # 5. is_electronic_check_risk
    df['is_electronic_check_risk'] = int(payment_method == 'Electronic check')
    
    # 6. is_high_risk_contract
    contract = df.get('Contract', 'Month-to-month').iloc[0] if 'Contract' in df.columns else 'Month-to-month'
    df['is_high_risk_contract'] = int(contract == 'Month-to-month')
    
    # 7. has_protection_services
    protection_count = 0
    for col in ['OnlineSecurity', 'OnlineBackup', 'DeviceProtection', 'TechSupport']:
        if df.get(col, 'No').iloc[0] == 'Yes':
            protection_count += 1
    df['has_protection_services'] = int(protection_count > 0)
    
    # 8. service_bundle_score
    df['service_bundle_score'] = protection_count
    
    # 9. high_paying_customer
    monthly_charges = df.get('MonthlyCharges', 0).iloc[0] if 'MonthlyCharges' in df.columns else 0
    if pd.isna(monthly_charges):
        monthly_charges = 0
    df['high_paying_customer'] = int(monthly_charges > 80)
    
    # 10. tenure_group
    if tenure <= 6:
        tenure_group = '0-6ay'
    elif tenure <= 12:
        tenure_group = '7-12ay'
    elif tenure <= 24:
        tenure_group = '13-24ay'
    elif tenure <= 48:
        tenure_group = '25-48ay'
    else:
        tenure_group = '49+ay'
    
    # Tenure group one-hot encoding
    for group in ['7-12ay', '13-24ay', '25-48ay', '49+ay']:
        df[f'tenure_group_{group}'] = int(tenure_group == group)
    
    # Categorical one-hot encoding
    categorical_mappings = {
        'MultipleLines': ['No phone service', 'Yes'],
        'InternetService': ['Fiber optic', 'No'],
        'OnlineSecurity': ['No internet service', 'Yes'],
        'OnlineBackup': ['No internet service', 'Yes'],
        'DeviceProtection': ['No internet service', 'Yes'],
        'TechSupport': ['No internet service', 'Yes'],
        'StreamingTV': ['No internet service', 'Yes'],
        'StreamingMovies': ['No internet service', 'Yes'],
        'Contract': ['One year', 'Two year'],
        'PaymentMethod': ['Credit card (automatic)', 'Electronic check', 'Mailed check']
    }
    
    for col, values in categorical_mappings.items():
        if col in df.columns:
            col_value = df[col].iloc[0]
            for val in values:
                df[f'{col}_{val}'] = int(col_value == val)
        else:
            # Kolon yoksa tüm dummy kolonları 0 yap
            for val in values:
                df[f'{col}_{val}'] = 0
    
    # Feature sıralamasını ayarla
    feature_names = pipeline_dict['feature_names']
    
    # Eksik kolonları 0 ile doldur
    for feature in feature_names:
        if feature not in df.columns:
            df[feature] = 0
    
    # Sadece gerekli kolonları seç
    df_processed = df[feature_names]
    
    # TÜM NaN değerleri 0 ile doldur (KRİTİK!)
    df_processed = df_processed.fillna(0)
    
    # Numeric kolonları scale et
    scaler = pipeline_dict['scaler']
    numeric_cols = pipeline_dict['numeric_cols']
    
    df_scaled = df_processed.copy()
    df_scaled[numeric_cols] = scaler.transform(df_processed[numeric_cols])
    
    # Final NaN kontrolü ve temizleme
    df_scaled = df_scaled.fillna(0)
    
    return df_scaled.values

# ============================================================================
# TAHMİN FONKSİYONU
# ============================================================================

def make_prediction():
    """Model ile tahmin yap"""
    
    # Model yükle
    model, pipeline, error = load_model_assets()
    
    if error:
        st.error(f"❌ Model yüklenirken hata oluştu: {error}")
        st.error("Lütfen models/ klasöründe final_model.pkl dosyasının var olduğundan emin olun.")
        return False
    
    # Pipeline kontrolü (dictionary olmalı)
    if not isinstance(pipeline, dict):
        st.error("❌ Pipeline dosyası geçersiz format. Dictionary bekleniyordu.")
        return False
    
    # Tahmin yap
    try:
        # Ham veriyi preprocess et
        processed_data = preprocess_input(st.session_state.form_data, pipeline)
        
        # NaN kontrolü (DEBUG)
        if np.isnan(processed_data).any():
            nan_count = np.isnan(processed_data).sum()
            st.error(f"⚠️ İşlenmiş veride {nan_count} adet NaN değer tespit edildi!")
            st.error("Bu bir hata durumudur. Lütfen geliştiriciye bildirin.")
            return False
        
        # Model prediction
        prediction = model.predict(processed_data)[0]
        
        # Probability varsa al
        if hasattr(model, "predict_proba"):
            probability = model.predict_proba(processed_data)[0]
            churn_prob = probability[1]  # Churn (Yes) olasılığı
        else:
            churn_prob = 0.5  # Default değer
        
        # Sonucu kaydet
        st.session_state.prediction_result = {
            "prediction": "Churn Riski Yüksek" if prediction == 1 else "Churn Riski Düşük",
            "prediction_class": prediction,
            "churn_probability": churn_prob,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        # Geçmişe ekle
        st.session_state.prediction_history.append(st.session_state.prediction_result)
        
        return True
        
    except Exception as e:
        st.error(f"❌ Tahmin yapılırken hata oluştu: {str(e)}")
        import traceback
        st.error(f"Detaylı hata: {traceback.format_exc()}")
        return False

# ============================================================================
# ADIM 4: RİSK DEĞERLENDİRMESİ
# ============================================================================

def step_4_risk_assessment():
    """Adım 4: Risk Değerlendirme Sonucu"""
    
    result = st.session_state.prediction_result
    
    if result is None or not isinstance(result, dict):
        st.error("❌ Tahmin sonucu bulunamadı!")
        st.warning("⚠️ Lütfen önceki adımda 'Risk Analizi Yap' butonuna tıklayın.")
        
        # Geri dönme butonu
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("⬅️ Geri Dön: Sözleşme & Ödeme", use_container_width=True, type="secondary"):
                st.session_state.current_step = 3
                st.rerun()
        return
    
    churn_prob = result.get("churn_probability", 0.5)
    prediction_class = result.get("prediction_class", 0)
    
    # Risk seviyesi belirle
    if churn_prob is not None:
        if churn_prob >= 0.7:
            risk_level = "high"
            risk_emoji = "🔴"
            risk_text = "Yüksek Risk"
            risk_color = COLORS['danger']
        elif churn_prob >= 0.4:
            risk_level = "medium"
            risk_emoji = "🟡"
            risk_text = "Orta Risk"
            risk_color = COLORS['warning']
        else:
            risk_level = "low"
            risk_emoji = "🟢"
            risk_text = "Düşük Risk"
            risk_color = COLORS['secondary']
    else:
        risk_level = "medium" if prediction_class == 1 else "low"
        risk_emoji = "🟡" if prediction_class == 1 else "🟢"
        risk_text = "Orta Risk" if prediction_class == 1 else "Düşük Risk"
        risk_color = COLORS['warning'] if prediction_class == 1 else COLORS['secondary']
    
    # Hero Card - Sonuç
    st.markdown(f"""
    <div class="result-card result-{risk_level} animate-in">
        <div style="text-align: center;">
            <span class="big-emoji">{risk_emoji}</span>
            <h1 style="color: {risk_color}; margin: 20px 0; text-shadow: 0 2px 8px rgba(0,0,0,0.15);">{risk_text}</h1>
            <p style="font-size: 22px; color: #1D1D1F; font-weight: 700; text-shadow: 0 1px 3px rgba(255,255,255,0.8);">
                Bu müşterinin churn etme riski <b style="color: {risk_color};">{risk_text.lower()}</b> seviyesindedir.
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Metrikler
    st.markdown("<br>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if churn_prob is not None:
            st.markdown(f"""
            <div class="metric-bento">
                <div class="metric-label">Churn Olasılığı</div>
                <div class="metric-value" style="color: {risk_color};">%{churn_prob*100:.1f}</div>
            </div>
            """, unsafe_allow_html=True)
    
    with col2:
        confidence = churn_prob if churn_prob is not None else 0.5
        confidence_level = "Yüksek" if abs(confidence - 0.5) > 0.3 else "Orta"
        st.markdown(f"""
        <div class="metric-bento">
            <div class="metric-label">Güven Seviyesi</div>
            <div class="metric-value" style="color: {COLORS['primary']};">{confidence_level}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        tenure = st.session_state.form_data.get("tenure", 0)
        st.markdown(f"""
        <div class="metric-bento">
            <div class="metric-label">Müşteri Süresi</div>
            <div class="metric-value" style="color: {COLORS['purple']};">{tenure} Ay</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Risk Faktörleri Analizi
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown('<div class="bento-card">', unsafe_allow_html=True)
    st.markdown("""
    <h3 style="color: #667eea;
               font-weight: 800;
               text-shadow: 0 2px 4px rgba(102, 126, 234, 0.3);">
        📊 Risk Faktörleri Analizi
    </h3>
    """, unsafe_allow_html=True)
    
    risk_factors = analyze_risk_factors(st.session_state.form_data)
    
    for factor in risk_factors[:3]:  # Top 3 faktör
        st.markdown(f"""
        <div style="padding: 16px; margin: 10px 0; background: rgba(255,255,255,0.9); 
                    border-radius: 14px; border-left: 5px solid {factor['color']};
                    box-shadow: 0 4px 12px rgba(0,0,0,0.08);">
            <b style="font-size: 18px; color: #1D1D1F; font-weight: 700;">
                {factor['icon']} {factor['factor']}
            </b><br>
            <span style="color: #1D1D1F; font-size: 15px; font-weight: 500; line-height: 1.6; margin-top: 6px; display: block;">
                {factor['explanation']}
            </span>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Butonlar
    st.markdown("<br>", unsafe_allow_html=True)
    col_btn1, col_btn2, col_btn3 = st.columns([1, 1, 1])
    
    with col_btn1:
        if st.button("⬅️ Sözleşme Bilgilerine Dön", use_container_width=True):
            st.session_state.current_step = 3
            st.rerun()
    
    with col_btn3:
        if st.button("💡 Aksiyon Önerilerine Geç", use_container_width=True, type="primary"):
            st.session_state.current_step = 5
            st.rerun()

# ============================================================================
# ADIM 5: AKSİYON ÖNERİLERİ
# ============================================================================

def step_5_action_recommendations():
    """Adım 5: Aksiyon Önerileri"""
    
    result = st.session_state.prediction_result
    churn_prob = result.get("churn_probability", 0.5)
    
    st.markdown('<div class="bento-card animate-in">', unsafe_allow_html=True)
    st.markdown("""
    <h2 style="color: #fa709a;
               margin-bottom: 8px;
               font-weight: 800;
               text-shadow: 0 2px 4px rgba(250, 112, 154, 0.3);">
        🎯 Önerilen Aksiyonlar
    </h2>
    <p style="color: #6E6E73; font-size: 16px;">Churn riskini azaltmak için önerilen stratejiler.</p>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Önerileri oluştur
    recommendations = generate_recommendations(st.session_state.form_data, churn_prob)
    
    if not recommendations or len(recommendations) == 0:
        st.warning("⚠️ Kişiselleştirilmiş öneri oluşturulamadı. Lütfen müşteri verilerini kontrol edin.")
        st.info("💡 Genel öneri: Müşteri ile iletişime geçin ve memnuniyetini değerlendirin.")
    else:
        for i, rec in enumerate(recommendations, 1):
            st.markdown(f"""
            <div class="action-card">
                <span class="action-icon">{rec['icon']}</span>
                <b style="font-size: 19px; color: #1D1D1F; font-weight: 800;">
                    {i}. {rec['title']}
                </b>
                <p style="margin: 10px 0 8px 44px; color: #1D1D1F; font-weight: 500; line-height: 1.6;">
                    {rec['description']}
                </p>
                <span class="badge badge-success" style="margin-left: 44px; font-weight: 800; text-shadow: 0 1px 2px rgba(0,0,0,0.2);">
                    Risk Azalması: ~{rec['impact']}%
                </span>
            </div>
            """, unsafe_allow_html=True)
    
    # İş Etkisi
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="bento-card">', unsafe_allow_html=True)
    st.markdown("""
    <h3 style="color: #667eea;
               font-weight: 800;
               text-shadow: 0 2px 4px rgba(102, 126, 234, 0.3);">
        💰 İş Etkisi Analizi
    </h3>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"""
        <div style="padding: 24px; background: rgba(255,255,255,0.9); border-radius: 16px; box-shadow: 0 6px 20px rgba(0,0,0,0.1);">
            <h4 style="color: {COLORS['danger']}; font-weight: 800; text-shadow: 0 2px 4px rgba(0,0,0,0.1);">❌ Churn Maliyeti</h4>
            <p style="font-size: 36px; font-weight: 800; color: {COLORS['danger']}; text-shadow: 0 2px 4px rgba(0,0,0,0.1);">$3,000</p>
            <p style="color: #1D1D1F; font-weight: 600;">Ortalama müşteri yaşam boyu değeri (LTV)</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div style="padding: 24px; background: rgba(255,255,255,0.9); border-radius: 16px; box-shadow: 0 6px 20px rgba(0,0,0,0.1);">
            <h4 style="color: {COLORS['secondary']}; font-weight: 800; text-shadow: 0 2px 4px rgba(0,0,0,0.1);">✅ Retention Maliyeti</h4>
            <p style="font-size: 36px; font-weight: 800; color: {COLORS['secondary']}; text-shadow: 0 2px 4px rgba(0,0,0,0.1);">$150</p>
            <p style="color: #1D1D1F; font-weight: 600;">Ortalama kampanya/indirim maliyeti</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # ROI Açıklaması (HTML ile LaTeX sorunu çözüldü)
    st.markdown("""
    <div style="padding: 16px; background: linear-gradient(135deg, #e0f7fa 0%, #e1f5fe 100%); 
                border-radius: 12px; border-left: 5px solid #0288d1; 
                box-shadow: 0 4px 12px rgba(2, 136, 209, 0.15);">
        <p style="color: #01579b; font-size: 17px; font-weight: 700; margin: 0; line-height: 1.6;">
            📊 <strong>Yatırım Getirisi (ROI):</strong> 
            Her <span style="color: #d32f2f; font-weight: 800;">1 USD</span> harcanan retention çabası için 
            potansiyel <span style="color: #2e7d32; font-weight: 800;">20 USD</span> tasarruf
        </p>
        <p style="color: #0277bd; font-size: 14px; margin: 8px 0 0 0; font-weight: 500;">
            ⚡ Yeni müşteri kazanma maliyeti, mevcut müşteri tutma maliyetinden 5-25 kat daha yüksektir.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Final Butonlar
    st.markdown("<br><br>", unsafe_allow_html=True)
    col_btn1, col_btn2, col_btn3 = st.columns([1, 1, 1])
    
    with col_btn1:
        if st.button("⬅️ Risk Sonuçlarına Dön", use_container_width=True):
            st.session_state.current_step = 4
            st.rerun()
    
    with col_btn2:
        if st.button("🔄 Baştan Başla", use_container_width=True):
            reset_form()
            st.rerun()
    
    with col_btn3:
        # Rapor indirme butonu (simüle)
        st.download_button(
            label="📥 Rapor İndir",
            data=generate_report_text(),
            file_name=f"churn_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
            mime="text/plain",
            use_container_width=True
        )

# ============================================================================
# YARDIMCI FONKSİYONLAR
# ============================================================================

def analyze_risk_factors(form_data):
    """Risk faktörlerini analiz et"""
    
    risk_factors = []
    
    # Contract
    if form_data.get("Contract") == "Month-to-month":
        risk_factors.append({
            "factor": "Aylık Sözleşme",
            "icon": "📅",
            "explanation": "Aylık sözleşmeler %42 daha yüksek churn riskine sahiptir. Uzun vadeli sözleşme önerilir.",
            "color": COLORS['danger']
        })
    
    # Internet Service
    if form_data.get("InternetService") == "Fiber optic":
        risk_factors.append({
            "factor": "Fiber İnternet",
            "icon": "🌐",
            "explanation": "Fiber müşterileri DSL'e göre %28 daha fazla churn ediyor. Fiyat rekabeti yüksek.",
            "color": COLORS['warning']
        })
    
    # Tenure
    if form_data.get("tenure", 12) < 12:
        risk_factors.append({
            "factor": "Yeni Müşteri",
            "icon": "⏰",
            "explanation": "İlk 12 ay kritik dönemdir. Yeni müşterilerin %34'ü ilk yıl içinde ayrılıyor.",
            "color": COLORS['danger']
        })
    
    # Tech Support
    if form_data.get("TechSupport") == "No" and form_data.get("InternetService") != "No":
        risk_factors.append({
            "factor": "Teknik Destek Yok",
            "icon": "🔧",
            "explanation": "Teknik destek almayan müşterilerin churn oranı %23 daha yüksektir.",
            "color": COLORS['warning']
        })
    
    # Payment Method
    if form_data.get("PaymentMethod") == "Electronic check":
        risk_factors.append({
            "factor": "Elektronik Çek Ödemesi",
            "icon": "💳",
            "explanation": "E-çek kullanıcıları otomatik ödemelere göre %18 daha fazla churn ediyor.",
            "color": COLORS['warning']
        })
    
    # Online Security
    if form_data.get("OnlineSecurity") == "No" and form_data.get("InternetService") != "No":
        risk_factors.append({
            "factor": "Güvenlik Paketi Yok",
            "icon": "🔒",
            "explanation": "Güvenlik paketi eklemek churn riskini %15 azaltabilir.",
            "color": COLORS['warning']
        })
    
    return risk_factors

def generate_recommendations(form_data, churn_prob):
    """Kişiselleştirilmiş öneriler oluştur"""
    
    recommendations = []
    
    # Contract upgrade
    if form_data.get("Contract") == "Month-to-month":
        recommendations.append({
            "icon": "📄",
            "title": "Uzun Vadeli Sözleşme Öner",
            "description": "1 veya 2 yıllık sözleşmeye geçişte %20 indirim sunun. Bu churn riskini %34 azaltır.",
            "impact": 34
        })
    elif form_data.get("Contract") == "One year":
        recommendations.append({
            "icon": "📄",
            "title": "2 Yıllık Sözleşmeye Yükselt",
            "description": "Mevcut 1 yıllık sözleşmeyi 2 yıla uzatmak için özel indirim sunun. Churn riskini %22 azaltır.",
            "impact": 22
        })
    
    # Tech Support
    if form_data.get("TechSupport") == "No" and form_data.get("InternetService") != "No":
        recommendations.append({
            "icon": "🔧",
            "title": "Teknik Destek Paketi Ekle",
            "description": "İlk 3 ay ücretsiz teknik destek paketi sunun. Müşteri memnuniyetini artırır ve churn riskini %18 azaltır.",
            "impact": 18
        })
    
    # Online Security
    if form_data.get("OnlineSecurity") == "No" and form_data.get("InternetService") != "No":
        recommendations.append({
            "icon": "🔒",
            "title": "Güvenlik Paketi Tanıtımı",
            "description": "Online güvenlik paketini 2 ay deneme süresi ile sunun. Veri güvenliği sağlar, churn riskini %15 azaltır.",
            "impact": 15
        })
    
    # Online Backup
    if form_data.get("OnlineBackup") == "No" and form_data.get("InternetService") != "No":
        recommendations.append({
            "icon": "💾",
            "title": "Yedekleme Hizmeti Ekle",
            "description": "Cloud yedekleme hizmetini 1 ay ücretsiz deneyin. Veri kaybı riskini azaltır.",
            "impact": 13
        })
    
    # Payment Method
    if form_data.get("PaymentMethod") == "Electronic check":
        recommendations.append({
            "icon": "💳",
            "title": "Otomatik Ödeme Teşvik Et",
            "description": "Kredi kartı veya banka transferi ile otomatik ödemeye geçişte $5 aylık indirim sunun. Churn riskini %12 azaltır.",
            "impact": 12
        })
    elif form_data.get("PaymentMethod") == "Mailed check":
        recommendations.append({
            "icon": "💳",
            "title": "Dijital Ödemeye Geçiş",
            "description": "Posta çeki yerine dijital ödeme yöntemlerine geçişi teşvik edin. İşlem kolaylığı sağlar.",
            "impact": 10
        })
    
    # Loyalty Program (tenure based)
    tenure = form_data.get("tenure", 0)
    if tenure >= 24:
        recommendations.append({
            "icon": "🎁",
            "title": "VIP Sadakat Programı",
            "description": "Uzun süreli müşteriler için özel avantajlar, indirimler ve öncelikli destek sunun.",
            "impact": 25
        })
    elif tenure >= 12:
        recommendations.append({
            "icon": "🎁",
            "title": "Sadakat Ödülü",
            "description": "1 yılı aşkın müşteriler için teşekkür hediyesi ve özel kampanyalar sunun.",
            "impact": 20
        })
    elif tenure <= 6:
        recommendations.append({
            "icon": "👋",
            "title": "Hoş Geldin Programı",
            "description": "Yeni müşterilere özel onboarding süreci ve ilk 3 ay ekstra destek sunun.",
            "impact": 28
        })
    
    # Device Protection
    if form_data.get("DeviceProtection") == "No" and form_data.get("InternetService") != "No":
        recommendations.append({
            "icon": "📱",
            "title": "Cihaz Koruma Paketi",
            "description": "Modem/router ve diğer cihazlar için koruma sigortası sunun.",
            "impact": 11
        })
    
    # Streaming Services
    if form_data.get("StreamingTV") == "No" and form_data.get("StreamingMovies") == "No" and form_data.get("InternetService") != "No":
        recommendations.append({
            "icon": "📺",
            "title": "Eğlence Paketi Öner",
            "description": "TV ve film streaming hizmetlerini paket indirimiyle sunun. Hizmet değerini artırır.",
            "impact": 16
        })
    
    # High Monthly Charges
    if form_data.get("MonthlyCharges", 0) > 80:
        recommendations.append({
            "icon": "💰",
            "title": "Ödeme Planı Optimizasyonu",
            "description": "Yüksek aylık ücretler için paket optimizasyonu yapın, gereksiz hizmetleri kaldırın.",
            "impact": 19
        })
    
    # Risk Level Based (Fallback Recommendations)
    if churn_prob >= 0.7:  # High risk
        recommendations.append({
            "icon": "🚨",
            "title": "Acil Müşteri İlişkileri Görüşmesi",
            "description": "Yüksek risk nedeniyle kişisel görüşme ayarlayın, sorunları dinleyin ve özel çözümler sunun.",
            "impact": 35
        })
    elif churn_prob >= 0.4:  # Medium risk
        recommendations.append({
            "icon": "📞",
            "title": "Proaktif Müşteri Memnuniyeti Anketi",
            "description": "Müşteri deneyimini değerlendirmek için anket gönderin ve geri bildirimlere hızlı yanıt verin.",
            "impact": 17
        })
    else:  # Low risk
        recommendations.append({
            "icon": "⭐",
            "title": "Referans Programı",
            "description": "Memnun müşterilerinizden yeni müşteri kazanmak için referans teşvikleri sunun.",
            "impact": 8
        })
    
    # Genel Öneriler (Her zaman dahil)
    recommendations.append({
        "icon": "📊",
        "title": "Düzenli İletişim ve Takip",
        "description": "Aylık hizmet kullanım raporları gönderin, özel kampanyalardan haberdar edin.",
        "impact": 14
    })
    
    # Impact'e göre sırala ve top 5 döndür
    recommendations_sorted = sorted(recommendations, key=lambda x: x['impact'], reverse=True)
    return recommendations_sorted[:5]

def generate_report_text():
    """İndirilebilir rapor oluştur"""
    
    result = st.session_state.prediction_result
    form_data = st.session_state.form_data
    
    report = f"""
    =====================================
    CHURN RİSK DEĞERLENDİRME RAPORU
    =====================================
    
    Tarih: {result.get('timestamp', 'N/A')}
    
    SONUÇ
    -----
    Tahmin: {result.get('prediction', 'N/A')}
    Churn Olasılığı: {result.get('churn_probability', 0)*100:.2f}%
    
    MÜŞTERİ BİLGİLERİ
    -----------------
    Cinsiyet: {form_data.get('gender', 'N/A')}
    Yaşlı Vatandaş: {'Evet' if form_data.get('SeniorCitizen') == 1 else 'Hayır'}
    Partner: {form_data.get('Partner', 'N/A')}
    Bakmakla Yükümlü: {form_data.get('Dependents', 'N/A')}
    Müşteri Süresi: {form_data.get('tenure', 'N/A')} ay
    
    HİZMETLER
    ---------
    İnternet: {form_data.get('InternetService', 'N/A')}
    Sözleşme: {form_data.get('Contract', 'N/A')}
    Ödeme: {form_data.get('PaymentMethod', 'N/A')}
    Aylık Ücret: ${form_data.get('MonthlyCharges', 0):.2f}
    
    ÖNERİLER
    --------
    1. Risk faktörlerini gözden geçirin
    2. Uzun vadeli sözleşme teşvik edin
    3. Ekstra hizmetler önerin
    4. Müşteri memnuniyeti takibi yapın
    
    =====================================
    Bu rapor AI tahmin modeli tarafından oluşturulmuştur.
    Kritik kararlar için uzman değerlendirmesi gereklidir.
    =====================================
    """
    
    return report

# ============================================================================
# ANA UYGULAMA
# ============================================================================

def main():
    """Ana uygulama"""
    
    # CSS injection
    inject_apple_bento_css()
    
    # Session state başlat
    init_session_state()
    
    # Model dosyalarını kontrol et
    if not MODEL_PATH.exists():
        st.error(f"❌ Model dosyası bulunamadı: {MODEL_PATH}")
        st.info("💡 Lütfen models/ klasöründe final_model.pkl dosyasının var olduğundan emin olun.")
        st.stop()
    
    if not PIPELINE_PATH.exists():
        st.warning(f"⚠️ Preprocessing pipeline dosyası bulunamadı: {PIPELINE_PATH}")
        st.info("Model ham veri ile çalışacak (pipeline olmadan).")
    
    # Hero Header
    st.markdown("""
    <div class="hero-card">
        <div style="position: relative; z-index: 1;">
            <h1 style="text-align: center; margin-bottom: 16px; 
                       color: #667eea;
                       background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
                       -webkit-background-clip: text;
                       -webkit-text-fill-color: transparent;
                       background-clip: text;
                       font-size: 58px;
                       font-weight: 900;
                       letter-spacing: -0.5px;
                       line-height: 1.2;
                       text-shadow: 0 2px 8px rgba(102, 126, 234, 0.4);">
                Müşteri Churn Risk Analiz Platformu
            </h1>
            <p style="text-align: center; font-size: 22px; color: #1D1D1F; font-weight: 600; line-height: 1.5; max-width: 800px; margin: 0 auto;">
                Gelişmiş makine öğrenmesi algoritmaları ile müşteri kayıp riskini değerlendirin,<br>
                <span style="color: #667eea; font-weight: 700;">proaktif stratejiler</span> geliştirin ve <span style="color: #764ba2; font-weight: 700;">müşteri sadakatini</span> artırın
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Progress Bar
    render_progress_bar(st.session_state.current_step)
    
    # Adımlara göre içerik göster
    if st.session_state.current_step == 1:
        step_1_customer_profile()
    elif st.session_state.current_step == 2:
        step_2_service_package()
    elif st.session_state.current_step == 3:
        step_3_contract_payment()
    elif st.session_state.current_step == 4:
        step_4_risk_assessment()
    elif st.session_state.current_step == 5:
        step_5_action_recommendations()
    
    # Footer
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown(f"""
    <div style="text-align: center; padding: 40px 20px; background: rgba(255,255,255,0.95); border-radius: 20px; 
                box-shadow: 0 8px 30px rgba(0,0,0,0.12); max-width: 1000px; margin: 0 auto;">
        <h3 style="color: #1D1D1F; font-size: 22px; font-weight: 800; margin-bottom: 20px; line-height: 1.4;">
            Model Performans Bilgileri
        </h3>
        <p style="color: #1D1D1F; font-size: 17px; font-weight: 600; line-height: 1.8; margin-bottom: 16px;">
            Bu platform <span style="color: #667eea; 
            font-weight: 800; font-size: 18px; text-shadow: 0 2px 4px rgba(102, 126, 234, 0.3);">Calibrated Classifier</span> makine öğrenmesi modeli ile çalışmaktadır.
        </p>
        <div style="display: flex; justify-content: center; gap: 40px; margin: 24px 0; flex-wrap: wrap;">
            <div style="text-align: center;">
                <p style="color: #667eea; font-size: 32px; font-weight: 900; margin-bottom: 4px;">0.7917</p>
                <p style="color: #6E6E73; font-size: 14px; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px;">F1 Score</p>
            </div>
            <div style="text-align: center;">
                <p style="color: #764ba2; font-size: 32px; font-weight: 900; margin-bottom: 4px;">0.8404</p>
                <p style="color: #6E6E73; font-size: 14px; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px;">ROC-AUC</p>
            </div>
            <div style="text-align: center;">
                <p style="color: #f093fb; font-size: 32px; font-weight: 900; margin-bottom: 4px;">0.8020</p>
                <p style="color: #6E6E73; font-size: 14px; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px;">Recall</p>
            </div>
            <div style="text-align: center;">
                <p style="color: #4facfe; font-size: 32px; font-weight: 900; margin-bottom: 4px;">0.7908</p>
                <p style="color: #6E6E73; font-size: 14px; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px;">Precision</p>
            </div>
        </div>
        <p style="color: #6E6E73; font-size: 15px; font-weight: 500; line-height: 1.7; margin-top: 20px; font-style: italic;">
            Model 10-fold cross-validation ile test edilmiş olup, <b style="color: #1D1D1F;">0.0073 overfitting skoru</b> ile 
            yüksek genelleme performansı göstermektedir. Kritik iş kararlarında mutlaka <b style="color: #1D1D1F;">uzman değerlendirmesi</b> 
            ile birlikte kullanılmalıdır.
        </p>
    </div>
    """, unsafe_allow_html=True)

# ============================================================================
# ÇALIŞTIR
# ============================================================================

if __name__ == "__main__":
    main()
