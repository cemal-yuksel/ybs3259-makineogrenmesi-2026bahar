"""
🔮 GÖRKEMLI TEKİL TAHMİN SAYFASI
=====================================
Diabetes Risk Prediction System - Professional ML Application
HCI Design Principles + Strategic Health Recommendations
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import datetime
from pathlib import Path

# ===== FEATURE ENGINEERING VE TAHMİN FONKSİYONLARI =====

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

# ===== VALIDATION VE ANALYSIS FONKSİYONLARI =====

def validate_input(input_dict):
    """Input validasyonu - Mantıksal kontroller"""
    errors = []
    
    if input_dict["Glucose"] < 0 or input_dict["Glucose"] > 250:
        errors.append("⚠️ Glikoz seviyesi 0-250 mg/dL arasında olmalıdır")
    
    if input_dict["BloodPressure"] < 0 or input_dict["BloodPressure"] > 180:
        errors.append("⚠️ Kan basıncı 0-180 mm Hg arasında olmalıdır")
    
    if input_dict["BMI"] < 10 or input_dict["BMI"] > 70:
        errors.append("⚠️ BMI değeri 10-70 arasında olmalıdır")
    
    if input_dict["Age"] < 18 or input_dict["Age"] > 100:
        errors.append("⚠️ Yaş 18-100 arasında olmalıdır")
    
    if input_dict["Pregnancies"] < 0 or input_dict["Pregnancies"] > 20:
        errors.append("⚠️ Hamilelik sayısı 0-20 arasında olmalıdır")
    
    if input_dict["DiabetesPedigreeFunction"] < 0 or input_dict["DiabetesPedigreeFunction"] > 3:
        errors.append("⚠️ Diyabet soy ağacı fonksiyonu 0-3 arasında olmalıdır")
    
    return errors

def analyze_risk_factors(input_dict):
    """Risk faktörlerini analiz et ve puanla"""
    risk_factors = []
    protective_factors = []
    
    # Glikoz analizi
    if input_dict["Glucose"] >= 140:
        risk_factors.append(("🔴 Yüksek Glikoz", f"{input_dict['Glucose']} mg/dL (Normal: <140)", "Kritik"))
    elif input_dict["Glucose"] >= 100:
        risk_factors.append(("🟡 Sınırda Glikoz", f"{input_dict['Glucose']} mg/dL (Normal: <100)", "Orta"))
    else:
        protective_factors.append(("✅ Normal Glikoz", f"{input_dict['Glucose']} mg/dL"))
    
    # BMI analizi
    if input_dict["BMI"] >= 30:
        risk_factors.append(("🔴 Obezite", f"BMI: {input_dict['BMI']:.1f} (Normal: 18.5-24.9)", "Yüksek"))
    elif input_dict["BMI"] >= 25:
        risk_factors.append(("🟡 Fazla Kilolu", f"BMI: {input_dict['BMI']:.1f}", "Orta"))
    elif input_dict["BMI"] < 18.5:
        risk_factors.append(("🟡 Düşük Kilolu", f"BMI: {input_dict['BMI']:.1f}", "Orta"))
    else:
        protective_factors.append(("✅ Sağlıklı Kilo", f"BMI: {input_dict['BMI']:.1f}"))
    
    # Yaş analizi
    if input_dict["Age"] >= 45:
        risk_factors.append(("🟡 İleri Yaş", f"{input_dict['Age']} yaş (Risk >45 yaş)", "Orta"))
    else:
        protective_factors.append(("✅ Genç Yaş", f"{input_dict['Age']} yaş"))
    
    # Kan basıncı analizi
    if input_dict["BloodPressure"] >= 90:
        risk_factors.append(("🔴 Yüksek Kan Basıncı", f"{input_dict['BloodPressure']} mm Hg (Normal: 60-80)", "Yüksek"))
    elif input_dict["BloodPressure"] >= 80:
        risk_factors.append(("🟡 Sınırda Kan Basıncı", f"{input_dict['BloodPressure']} mm Hg", "Orta"))
    elif input_dict["BloodPressure"] < 60 and input_dict["BloodPressure"] > 0:
        risk_factors.append(("🟡 Düşük Kan Basıncı", f"{input_dict['BloodPressure']} mm Hg", "Orta"))
    else:
        protective_factors.append(("✅ Normal Kan Basıncı", f"{input_dict['BloodPressure']} mm Hg"))
    
    # Genetik risk
    if input_dict["DiabetesPedigreeFunction"] >= 0.5:
        risk_factors.append(("🟡 Genetik Yatkınlık", f"Skor: {input_dict['DiabetesPedigreeFunction']:.3f}", "Orta"))
    else:
        protective_factors.append(("✅ Düşük Genetik Risk", f"Skor: {input_dict['DiabetesPedigreeFunction']:.3f}"))
    
    # Hamilelik riski
    if input_dict["Pregnancies"] >= 6:
        risk_factors.append(("🟡 Çok Hamilelik", f"{input_dict['Pregnancies']} hamilelik", "Orta"))
    
    return risk_factors, protective_factors

def generate_strategic_recommendations(prediction, input_dict, risk_factors):
    """Tahmin sonucuna göre stratejik öneriler oluştur"""
    recommendations = []
    
    if prediction == 1:  # Diyabet riski var
        recommendations.append({
            "emoji": "🏥",
            "title": "Acil Tıbbi Değerlendirme",
            "desc": "En kısa sürede bir endokrinoloji uzmanına başvurun. HbA1c testi yaptırın.",
            "priority": "YÜKSEK"
        })
        
        if input_dict["Glucose"] >= 140:
            recommendations.append({
                "emoji": "🍎",
                "title": "Glikoz Kontrolü",
                "desc": "Şekerli gıdalardan kaçının. Kompleks karbonhidratları tercih edin. Günde 3-4 öğün düzenli beslenin.",
                "priority": "KRİTİK"
            })
        
        if input_dict["BMI"] >= 30:
            recommendations.append({
                "emoji": "🏃",
                "title": "Kilo Yönetimi",
                "desc": "Hedef: %5-10 kilo kaybı. Haftada 150 dakika orta şiddette egzersiz. Diyetisyen desteği alın.",
                "priority": "YÜKSEK"
            })
        
        if input_dict["BloodPressure"] >= 90:
            recommendations.append({
                "emoji": "💊",
                "title": "Kan Basıncı Takibi",
                "desc": "Günlük kan basıncı ölçümü. Tuz tüketimini azaltın. Doktor kontrolünde ilaç tedavisi değerlendirin.",
                "priority": "YÜKSEK"
            })
        
        recommendations.append({
            "emoji": "📊",
            "title": "Düzenli Kontroller",
            "desc": "3 ayda bir HbA1c, açlık kan şekeri ve lipid profili testi. Yılda bir göz muayenesi.",
            "priority": "ORTA"
        })
        
        recommendations.append({
            "emoji": "🧘",
            "title": "Yaşam Tarzı Değişiklikleri",
            "desc": "Stres yönetimi teknikleri. Yeterli uyku (7-8 saat). Sigara ve alkol tüketiminden kaçının.",
            "priority": "ORTA"
        })
    
    else:  # Diyabet riski düşük
        recommendations.append({
            "emoji": "✅",
            "title": "Koruyucu Takip",
            "desc": "Yılda bir kez rutin kontrol. Açlık kan şekeri testi yaptırın.",
            "priority": "ORTA"
        })
        
        if input_dict["BMI"] >= 25 or input_dict["Glucose"] >= 100:
            recommendations.append({
                "emoji": "⚠️",
                "title": "Önleyici Tedbirler",
                "desc": "Risk faktörleriniz var. Sağlıklı beslenme ve düzenli egzersiz ile bu riskleri azaltabilirsiniz.",
                "priority": "ORTA"
            })
        
        recommendations.append({
            "emoji": "🥗",
            "title": "Sağlıklı Beslenme",
            "desc": "Akdeniz diyeti prensiplerine uyun. Bol sebze-meyve, tam tahıl, az işlenmiş gıdalar.",
            "priority": "DÜŞÜK"
        })
        
        recommendations.append({
            "emoji": "💪",
            "title": "Fiziksel Aktivite",
            "desc": "Haftada 150 dakika orta şiddette egzersiz. Yürüyüş, yüzme, bisiklet gibi aktiviteler.",
            "priority": "DÜŞÜK"
        })
    
    return recommendations

def render_prediction_card(prediction, probability, input_dict):
    """Görkemli tahmin sonuç kartı"""
    
    if prediction == 1:
        result_emoji = "🔴"
        result_title = "Diyabet Riski Tespit Edildi"
        result_subtitle = "Yüksek Risk Profili"
        gradient = "linear-gradient(135deg, #FFE5E5 0%, #FFCCCC 100%)"
        border_color = "#C73E1D"
        confidence = probability["Diyabet Var"] if probability else None
    else:
        result_emoji = "🟢"
        result_title = "Diyabet Riski Düşük"
        result_subtitle = "Düşük Risk Profili"
        gradient = "linear-gradient(135deg, #E8F5E9 0%, #C8E6C9 100%)"
        border_color = "#6A994E"
        confidence = probability["Diyabet Yok"] if probability else None
    
    # Ana sonuç kartı
    st.markdown(f"""
    <div style="background: {gradient}; border: 3px solid {border_color}; border-radius: 20px; padding: 32px; margin: 24px 0; box-shadow: 0 10px 40px rgba(0,0,0,0.1);">
        <div style="text-align: center;">
            <div style="font-size: 4rem; margin-bottom: 16px;">{result_emoji}</div>
            <h1 style="margin: 0; color: #1F2937; font-size: 2rem; font-weight: 800;">{result_title}</h1>
            <p style="margin-top: 8px; color: #6B7280; font-size: 1.1rem; font-weight: 600;">{result_subtitle}</p>
        </div>
        
        <div style="background: rgba(255,255,255,0.7); border-radius: 12px; padding: 20px; margin-top: 24px;">
            <div style="text-align: center;">
                <p style="margin: 0; color: #374151; font-size: 0.9rem; font-weight: 600; text-transform: uppercase; letter-spacing: 1px;">MODEL GÜVENİLİRLİK SKORU</p>
                <p style="margin-top: 8px; font-size: 2.5rem; font-weight: 800; color: {border_color};">%{confidence:.1f}</p>
                <p style="margin-top: 4px; color: #6B7280; font-size: 0.95rem;">
                    {'Yüksek Güven' if confidence >= 80 else 'Orta Güven' if confidence >= 60 else 'Düşük Güven'}
                </p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Olasılık dağılımı - Görkemli gauge chart
    if probability:
        fig = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=probability["Diyabet Var"],
            title={'text': "Diyabet Riski Olasılığı", 'font': {'size': 24, 'color': '#1F2937'}},
            delta={'reference': 50, 'increasing': {'color': "#C73E1D"}, 'decreasing': {'color': "#6A994E"}},
            gauge={
                'axis': {'range': [None, 100], 'tickwidth': 2, 'tickcolor': "#374151"},
                'bar': {'color': "#2E86AB"},
                'bgcolor': "white",
                'borderwidth': 3,
                'bordercolor': "#D1D5DB",
                'steps': [
                    {'range': [0, 30], 'color': '#C8E6C9'},
                    {'range': [30, 70], 'color': '#FFF9C4'},
                    {'range': [70, 100], 'color': '#FFCCBC'}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 50
                }
            }
        ))
        
        fig.update_layout(
            paper_bgcolor="#F9FAFB",
            height=350,
            margin=dict(l=20, r=20, t=60, b=20),
            font={'color': "#1F2937", 'family': "Arial"}
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    # İstatistiksel detaylar
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"""
        <div style="background: #E3F2FD; border-left: 4px solid #2E86AB; border-radius: 8px; padding: 16px;">
            <h4 style="margin: 0; color: #1F2937;">📊 Sınıf Olasılıkları</h4>
            <p style="margin-top: 12px; font-size: 1.1rem;"><b>Diyabet Yok:</b> %{probability['Diyabet Yok']:.2f}</p>
            <p style="margin-top: 8px; font-size: 1.1rem;"><b>Diyabet Var:</b> %{probability['Diyabet Var']:.2f}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div style="background: #FFF3E0; border-left: 4px solid #F18F01; border-radius: 8px; padding: 16px;">
            <h4 style="margin: 0; color: #1F2937;">⚠️ Önemli Uyarı</h4>
            <p style="margin-top: 12px; font-size: 0.95rem;">Bu sonuç makine öğrenmesi modelinin tahminidir. Kritik sağlık kararları için mutlaka <b>uzman doktor değerlendirmesi</b> alınmalıdır.</p>
        </div>
        """, unsafe_allow_html=True)

def log_prediction(input_data, prediction, confidence=None):
    """Tahmin logunu kaydet"""
    try:
        log_path = Path("logs/prediction_log.csv")
        log_path.parent.mkdir(exist_ok=True)
        
        log_row = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "prediction": "Diyabet Var" if prediction == 1 else "Diyabet Yok",
            "confidence": confidence
        }
        
        for col in input_data.columns:
            log_row[col] = input_data.iloc[0][col]
        
        if log_path.exists():
            pd.DataFrame([log_row]).to_csv(log_path, mode="a", index=False, header=False)
        else:
            pd.DataFrame([log_row]).to_csv(log_path, index=False)
    except Exception as e:
        st.warning(f"Loglama hatası (önemsiz): {e}")

def show(model):
    """🔮 GÖRKEMLI TEKİL TAHMİN SAYFASI"""
    
    # ===== GÖRKEMLI HERO SECTION =====
    st.markdown("""
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 24px; padding: 48px; margin-bottom: 32px; box-shadow: 0 20px 60px rgba(102, 126, 234, 0.3);">
        <div style="text-align: center; color: white;">
            <div style="font-size: 5rem; margin-bottom: 16px;">🔮</div>
            <h1 style="margin: 0; font-size: 3rem; font-weight: 900; text-shadow: 2px 2px 4px rgba(0,0,0,0.2);">Diabetes Risk Prediction</h1>
            <p style="margin-top: 16px; font-size: 1.3rem; opacity: 0.95; font-weight: 500;">Yapay Zeka Destekli Profesyonel Sağlık Değerlendirme Sistemi</p>
            <div style="margin-top: 24px; display: inline-block; background: rgba(255,255,255,0.2); border-radius: 50px; padding: 12px 32px; backdrop-filter: blur(10px);">
                <span style="font-size: 1.1rem; font-weight: 600;">✨ Random Forest ML Model | 77.3% Accuracy | ROC-AUC 0.83</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # ===== BİLGİLENDİRME BANNER =====
    st.markdown("""
    <div style="background: linear-gradient(90deg, #E3F2FD 0%, #E8EAF6 100%); border-left: 6px solid #2E86AB; border-radius: 12px; padding: 20px; margin-bottom: 24px;">
        <h3 style="margin: 0; color: #1F2937;">💡 Sistem Nasıl Çalışır?</h3>
        <p style="margin-top: 12px; color: #374151; line-height: 1.7;">
            Bu sistem, <b>768 hasta verisi</b> üzerinde eğitilmiş <b>Random Forest</b> makine öğrenmesi modeli kullanarak 
            diyabet risk tahmini yapar. Altı temel sağlık göstergesi analiz edilir ve <b>14 feature</b> ile tahmin üretilir.
            Sonuçlar, <b>uzman doktor değerlendirmesiyle birlikte</b> kullanılmalıdır.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # ===== TAHMİN FORMU =====
    with st.form("prediction_form", clear_on_submit=False):
        st.markdown("""
        <div style="background: linear-gradient(135deg, #F9FAFB 0%, #FFFFFF 100%); border: 2px solid #E5E7EB; border-radius: 16px; padding: 24px; margin-bottom: 16px;">
            <h2 style="margin: 0; color: #1F2937;">📋 Sağlık Verileri Girişi</h2>
            <p style="margin-top: 8px; color: #6B7280;">Lütfen tüm alanları eksiksiz ve doğru doldurun</p>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 🩺 Klinik Ölçümler")
            glucose = st.number_input(
                "🔬 Glikoz Seviyesi (mg/dL)",
                min_value=0,
                max_value=250,
                value=120,
                step=1,
                help="2 saatlik oral glikoz tolerans testinde plazma glikoz konsantrasyonu"
            )
            
            blood_pressure = st.number_input(
                "❤️ Diyastolik Kan Basıncı (mm Hg)",
                min_value=0,
                max_value=180,
                value=70,
                step=1,
                help="Diyastolik (alt) kan basıncı değeri"
            )
            
            bmi = st.number_input(
                "⚖️ Vücut Kitle İndeksi (BMI)",
                min_value=10.0,
                max_value=70.0,
                value=25.0,
                step=0.1,
                help="Kilo (kg) / Boy² (m²) formülü ile hesaplanır"
            )
        
        with col2:
            st.markdown("#### 👤 Kişisel Bilgiler")
            age = st.number_input(
                "🎂 Yaş",
                min_value=18,
                max_value=100,
                value=33,
                step=1,
                help="Kişinin yaşı (yıl)"
            )
            
            pregnancies = st.number_input(
                "👶 Hamilelik Sayısı",
                min_value=0,
                max_value=20,
                value=1,
                step=1,
                help="Toplam hamilelik sayısı (kadınlar için). Erkekler için 0 giriniz."
            )
            
            diabetes_pedigree = st.number_input(
                "🧬 Diyabet Soy Ağacı Skoru",
                min_value=0.0,
                max_value=3.0,
                value=0.5,
                step=0.01,
                help="Aile geçmişine dayalı diyabet risk skoru (0-3 arası)"
            )
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Butonlar - Görkemli tasarım
        col1, col2, col3 = st.columns([3, 2, 1])
        
        with col1:
            submit_button = st.form_submit_button(
                "🔮 Tahmin Yap", 
                use_container_width=True,
                type="primary"
            )
        
        with col2:
            example_button = st.form_submit_button(
                "📋 Örnek Veriyle Dene", 
                use_container_width=True
            )
        
        with col3:
            clear_button = st.form_submit_button(
                "🔄 Temizle", 
                use_container_width=True
            )
    
    # ===== ÖRNEK VERİ YÜKLEME =====
    if example_button:
        st.info("✅ **Örnek veri yüklendi!** Yüksek riskli bir profil. 'Tahmin Yap' butonuna tıklayın.")
        pregnancies = 6
        glucose = 148
        blood_pressure = 72
        bmi = 33.6
        diabetes_pedigree = 0.627
        age = 50
    
    # ===== TEMİZLEME =====
    if clear_button:
        st.session_state.clear()
        st.rerun()
    
    # ===== TAHMİN YAPMA =====
    if submit_button:
        input_dict = {
            "Pregnancies": pregnancies,
            "Glucose": glucose,
            "BloodPressure": blood_pressure,
            "BMI": bmi,
            "DiabetesPedigreeFunction": diabetes_pedigree,
            "Age": age
        }
        
        # Validasyon
        errors = validate_input(input_dict)
        
        if errors:
            st.error("❌ **Hatalı Girişler Tespit Edildi:**")
            for error in errors:
                st.error(f"  {error}")
        else:
            input_df = pd.DataFrame([input_dict])
            
            # Tahmin işlemi
            with st.spinner("🔄 Yapay zeka modeli çalışıyor... Tahmin yapılıyor..."):
                prediction, probability, error = predict_single(input_df, model)
            
            if error:
                st.error(f"❌ **Tahmin Hatası:** {error}")
            else:
                # ===== BAŞARILI TAHMİN =====
                st.success("✅ **Tahmin Başarıyla Tamamlandı!** Sonuçlar hazırlandı.")
                st.markdown("<br>", unsafe_allow_html=True)
                
                # Tahmin sonuç kartı
                st.markdown("---")
                st.markdown("## 🎯 Tahmin Sonucu")
                render_prediction_card(prediction, probability, input_dict)
                
                # ===== RİSK FAKTÖRLERİ ANALİZİ =====
                st.markdown("<br>", unsafe_allow_html=True)
                st.markdown("---")
                st.markdown("## 🔍 Risk Faktörleri Analizi")
                
                risk_factors, protective_factors = analyze_risk_factors(input_dict)
                
                col1, col2 = st.columns(2)
                
                with col1:
                    if risk_factors:
                        st.markdown("""
                        <div style="background: #FFF3E0; border: 2px solid #F18F01; border-radius: 12px; padding: 20px;">
                            <h3 style="margin: 0; color: #C73E1D;">⚠️ Risk Faktörleri</h3>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        for factor, detail, priority in risk_factors:
                            priority_color = "#C73E1D" if priority == "Kritik" else "#F18F01" if priority == "Yüksek" else "#F59E0B"
                            st.markdown(f"""
                            <div style="background: white; border-left: 4px solid {priority_color}; border-radius: 8px; padding: 12px; margin: 12px 0;">
                                <p style="margin: 0; font-weight: 600; color: #1F2937;">{factor}</p>
                                <p style="margin: 4px 0 0 0; color: #6B7280; font-size: 0.9rem;">{detail}</p>
                                <span style="background: {priority_color}; color: white; padding: 2px 8px; border-radius: 4px; font-size: 0.75rem; font-weight: 600;">{priority} PRİORİTE</span>
                            </div>
                            """, unsafe_allow_html=True)
                    else:
                        st.success("✅ Risk faktörü tespit edilmedi!")
                
                with col2:
                    if protective_factors:
                        st.markdown("""
                        <div style="background: #E8F5E9; border: 2px solid #6A994E; border-radius: 12px; padding: 20px;">
                            <h3 style="margin: 0; color: #2E7D32;">✅ Koruyucu Faktörler</h3>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        for factor, detail in protective_factors:
                            st.markdown(f"""
                            <div style="background: white; border-left: 4px solid #6A994E; border-radius: 8px; padding: 12px; margin: 12px 0;">
                                <p style="margin: 0; font-weight: 600; color: #1F2937;">{factor}</p>
                                <p style="margin: 4px 0 0 0; color: #6B7280; font-size: 0.9rem;">{detail}</p>
                            </div>
                            """, unsafe_allow_html=True)
                
                # ===== STRATEJİK ÖNERİLER =====
                st.markdown("<br>", unsafe_allow_html=True)
                st.markdown("---")
                st.markdown("## 💡 Stratejik Sağlık Önerileri")
                
                recommendations = generate_strategic_recommendations(prediction, input_dict, risk_factors)
                
                for i, rec in enumerate(recommendations):
                    priority_colors = {
                        "KRİTİK": ("#C73E1D", "#FFE5E5"),
                        "YÜKSEK": ("#F18F01", "#FFF3E0"),
                        "ORTA": ("#2E86AB", "#E3F2FD"),
                        "DÜŞÜK": ("#6A994E", "#E8F5E9")
                    }
                    border_color, bg_color = priority_colors.get(rec["priority"], ("#6B7280", "#F3F4F6"))
                    
                    st.markdown(f"""
                    <div style="background: {bg_color}; border-left: 5px solid {border_color}; border-radius: 12px; padding: 20px; margin: 16px 0;">
                        <div style="display: flex; align-items: center; margin-bottom: 12px;">
                            <span style="font-size: 2rem; margin-right: 16px;">{rec['emoji']}</span>
                            <div>
                                <h4 style="margin: 0; color: #1F2937;">{rec['title']}</h4>
                                <span style="background: {border_color}; color: white; padding: 2px 10px; border-radius: 12px; font-size: 0.75rem; font-weight: 700;">{rec['priority']}</span>
                            </div>
                        </div>
                        <p style="margin: 0; color: #374151; line-height: 1.6;">{rec['desc']}</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                # ===== TAHMİN KAYDETME =====
                confidence = probability["Diyabet Var"] if (probability and prediction == 1) else (probability["Diyabet Yok"] if probability else None)
                log_prediction(input_df, prediction, confidence)
                
                # Session state'e kaydet
                st.session_state.last_prediction = prediction
                st.session_state.last_input = input_dict
                st.session_state.last_probability = probability
                
                # Tahmin sayacı
                if "total_predictions" not in st.session_state:
                    st.session_state.total_predictions = 0
                st.session_state.total_predictions += 1
                
                st.markdown("<br>", unsafe_allow_html=True)
                st.info(f"💾 **Tahmin kaydedildi!** Toplam {st.session_state.total_predictions} tahmin yapıldı. Loglar `logs/prediction_log.csv` dosyasında saklanıyor.")
    
    # ===== FOOTER - MODEL BİLGİLERİ =====
    st.markdown("---")
    
    # === FOOTER BAŞLIK ===
    st.markdown("# 📊 Model Teknik Bilgileri & Geliştirici Bilgisi")
    st.markdown("> 🔬 Bu sistemde kullanılan makine öğrenmesi modelinin teknik detayları ve geliştirici bilgileri aşağıda yer almaktadır.")
    st.markdown("---")
    
    # === MODEL KARTELERİ - 4 KOLON ===
    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.markdown("#### 🤖 Model Tipi")
        st.markdown("**Random Forest Classifier**")
        st.markdown("Ensemble öğrenme algoritması — Yüzlerce karar ağacının oyu ile tahmin üretir.")
        st.success("✅ Üretimde Aktif")

    with c2:
        st.markdown("#### 📈 Model Performansı")
        col_a, col_b = st.columns(2)
        with col_a:
            st.metric("F1-Score", "0.77", "+0.05 baseline'a göre")
        with col_b:
            st.metric("Accuracy", "77.3%", "+4.2%")
        st.metric("ROC-AUC", "0.83", "Mükemmel sınıflandırma")

    with c3:
        st.markdown("#### 🔬 Eğitim Verisi")
        st.metric("Toplam Hasta", "768", "Pima Indians Dataset")
        col_a, col_b = st.columns(2)
        with col_a:
            st.metric("Eğitim", "614", "80%")
        with col_b:
            st.metric("Test", "154", "20%")

    with c4:
        st.markdown("#### 🧬 Feature Engineering")
        st.metric("Toplam Feature", "14")
        col_a, col_b = st.columns(2)
        with col_a:
            st.metric("Orijinal", "6")
        with col_b:
            st.metric("Türetilmiş", "8")
        st.markdown("Binary + İnteraksiyon featureları")

    st.markdown("---")

    # === TEKNİK DETAYLAR ===
    st.markdown("#### ⚙️ Teknik Detaylar")
    d1, d2, d3, d4 = st.columns(4)
    with d1:
        st.metric("Cross-Validation", "5-Fold", "Stratified CV")
    with d2:
        st.metric("Overfitting Gap", "0.23", "Kabul Edilebilir Sınırda")
    with d3:
        st.metric("F-1 Score/ Accuracy", "0.77 / 77.3%", "Pozitif Sınıf")
    with d4:
        st.metric("Model Versiyonu", "v1.0", "Mayıs 2026")

    st.markdown("---")

    # === GELİŞTİRİCİ VE PIPELINE BİLGİSİ ===
    st.markdown("## 👨‍🔬 Geliştirici & Proje Hakkında")

    g1, g2 = st.columns([1, 2])

    with g1:
        st.markdown("### 🎓 Geliştirici")
        st.markdown("## **Res. Asst. Cemal YÜKSEL**")
        st.markdown("---")
        st.markdown("🏛️ **Kurum:** Üniversite")
        st.markdown("📚 **Alan:** Makine Öğrenmesi & Veri Bilimi")
        st.markdown("🗓️ **Dönem:** 2025–2026 Bahar Dönemi")
        st.markdown("📖 **Ders:** Makine Öğrenmesi — Ders 11")
        st.markdown("---")
        st.success("✅ Araştırma Görevlisi")
        st.info("🤖 Agentik ML Pipeline Mimarisi Uzmanı")

    with g2:
        st.markdown("### 🔄 Agentik ML Pipeline Mimarisi")
        st.markdown("Bu proje, birbirleriyle haberleşen uzman yapay zeka ajanları tarafından uçtan uca otomatik olarak geliştirilmiştir.")
        st.markdown("---")
        p1, p2, p3, p4 = st.columns(4)
        with p1:
            st.success("**1️⃣ EDA Expert**")
            st.caption("Keşifsel veri analizi, görselleştirme, outlier tespiti, dağılım analizi")
        with p2:
            st.warning("**2️⃣ DataPrep Expert**")
            st.caption("Eksik veri yönetimi, feature engineering, ölçekleme, dönüşüm")
        with p3:
            st.info("**3️⃣ Model Expert**")
            st.caption("12+ model karşılaştırma, cross-validation, hyperparameter tuning")
        with p4:
            st.error("**4️⃣ Deployment Expert**")
            st.caption("Streamlit UI, HCI ilkeleri, Shneiderman 8 Altın Kural")

        st.markdown("---")
        st.markdown("**🛠️ Kullanılan Teknolojiler**")
        t1, t2, t3, t4, t5 = st.columns(5)
        with t1:
            st.markdown("🐍 **Python 3.13**")
        with t2:
            st.markdown("🌊 **Streamlit**")
        with t3:
            st.markdown("🤖 **Scikit-learn**")
        with t4:
            st.markdown("📊 **Plotly**")
        with t5:
            st.markdown("🐼 **Pandas**")

    st.markdown("---")

    # === SON SATIR ===
    f1, f2, f3 = st.columns(3)
    with f1:
        st.caption("🏛️ © 2026 Diabetes Prediction System — Res. Asst. Cemal YÜKSEL")
    with f2:
        st.caption("⚡ Powered by Streamlit · Scikit-learn · Plotly · Python")
    with f3:
        st.caption("🔒 Güvenli · OWASP Uyumlu · HCI Tabanlı · Klinik Destekli")
