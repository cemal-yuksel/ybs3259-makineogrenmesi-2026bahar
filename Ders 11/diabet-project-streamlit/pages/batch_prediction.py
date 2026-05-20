"""
Toplu Tahmin Sayfası - CSV Yükleme ile Batch Prediction
Shneiderman Kural 2-5-6: Kısayollar, hata önleme, geri alma kolaylığı
"""

import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
from io import StringIO

def validate_csv_columns(df, expected_columns):
    """CSV kolon kontrolü"""
    missing_cols = [col for col in expected_columns if col not in df.columns]
    extra_cols = [col for col in df.columns if col not in expected_columns]
    
    return missing_cols, extra_cols

def show(model):
    """Toplu tahmin sayfası içeriği"""
    
    st.markdown("""
    <div class="hero-card">
        <h1 style="margin: 0; color: #1F2937;">📊 Toplu Tahmin (Batch Prediction)</h1>
        <p style="margin-top: 8px; color: #6B7280;">
            CSV dosyası yükleyerek çoklu kayıt için otomatik tahmin
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Bilgilendirme
    st.info("""
    **ℹ️ Nasıl Kullanılır?**
    
    1. CSV dosyanızı yükleyin (aşağıdaki format gereklidir)
    2. Kolon uyumluluğu otomatik kontrol edilir
    3. "Tahmin Yap" butonuna tıklayın
    4. Sonuçları görüntüleyin ve CSV olarak indirin
    """)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Gerekli format
    st.markdown("### 📋 Gerekli CSV Formatı")
    
    expected_columns = ["Pregnancies", "Glucose", "BloodPressure", "BMI", "DiabetesPedigreeFunction", "Age"]
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        CSV dosyanız aşağıdaki kolonları **tam olarak** içermelidir:
        
        - `Pregnancies`: Hamilelik sayısı (0-20)
        - `Glucose`: Glikoz seviyesi (0-250 mg/dL)
        - `BloodPressure`: Kan basıncı (0-180 mm Hg)
        - `BMI`: Vücut kitle indeksi (10-70)
        - `DiabetesPedigreeFunction`: Diyabet soy ağacı fonksiyonu (0-3)
        - `Age`: Yaş (18-100)
        
        **Not:** Kolon isimleri büyük/küçük harf duyarlıdır!
        """)
    
    with col2:
        # Örnek CSV indirme
        example_data = pd.DataFrame({
            "Pregnancies": [6, 1, 8, 0],
            "Glucose": [148, 85, 183, 137],
            "BloodPressure": [72, 66, 64, 40],
            "BMI": [33.6, 26.6, 23.3, 43.1],
            "DiabetesPedigreeFunction": [0.627, 0.351, 0.672, 2.288],
            "Age": [50, 31, 32, 33]
        })
        
        csv = example_data.to_csv(index=False)
        st.download_button(
            label="📥 Örnek CSV İndir",
            data=csv,
            file_name="ornek_veri.csv",
            mime="text/csv",
            use_container_width=True
        )
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        st.info("Örnek CSV'yi indirip kendi verilerinizle doldurun!")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # CSV Yükleme
    st.markdown("### 📤 CSV Dosyası Yükle")
    
    uploaded_file = st.file_uploader(
        "CSV dosyanızı buraya yükleyin",
        type=["csv"],
        help="Maksimum dosya boyutu: 200MB"
    )
    
    if uploaded_file is not None:
        try:
            # CSV'yi oku
            df = pd.read_csv(uploaded_file)
            
            st.success(f"✅ Dosya başarıyla yüklendi: **{uploaded_file.name}**")
            
            st.markdown(f"**Satır sayısı:** {len(df)} | **Kolon sayısı:** {len(df.columns)}")
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            # Veri önizleme
            with st.expander("🔍 Veri Önizleme (İlk 10 Satır)", expanded=True):
                st.dataframe(df.head(10), use_container_width=True)
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            # Kolon kontrolü
            missing_cols, extra_cols = validate_csv_columns(df, expected_columns)
            
            if missing_cols or extra_cols:
                st.error("❌ **Kolon Uyumsuzluğu Tespit Edildi!**")
                
                if missing_cols:
                    st.error(f"**Eksik Kolonlar:** {', '.join(missing_cols)}")
                
                if extra_cols:
                    st.warning(f"**Fazla Kolonlar (göz ardı edilecek):** {', '.join(extra_cols)}")
                
                if missing_cols:
                    st.stop()
            
            else:
                st.success("✅ **Kolon Kontrolü Başarılı!** Tüm gerekli kolonlar mevcut.")
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            # Tahmin butonu
            if st.button("🔮 Toplu Tahmin Yap", use_container_width=True):
                
                # Sadece gerekli kolonları al
                input_df = df[expected_columns].copy()
                
                # Veri tipi kontrolü
                try:
                    input_df = input_df.astype(float)
                except Exception as e:
                    st.error(f"❌ Veri tipi hatası: Tüm kolonlar sayısal olmalıdır. Hata: {e}")
                    st.stop()
                
                # Tahmin yap
                with st.spinner("🔄 Tahminler yapılıyor... Lütfen bekleyin."):
                    from app import predict_batch
                    result_df, error = predict_batch(input_df, model)
                
                if error:
                    st.error(f"❌ Tahmin hatası: {error}")
                else:
                    st.success(f"✅ **{len(result_df)} adet tahmin başarıyla tamamlandı!**")
                    
                    st.markdown("<br>", unsafe_allow_html=True)
                    
                    # Sonuç özeti
                    st.markdown("### 📊 Tahmin Sonuç Özeti")
                    
                    col1, col2, col3, col4 = st.columns(4)
                    
                    diyabet_var = (result_df["Tahmin"] == "Diyabet Var").sum()
                    diyabet_yok = (result_df["Tahmin"] == "Diyabet Yok").sum()
                    
                    with col1:
                        st.metric(
                            label="Toplam Kayıt",
                            value=len(result_df)
                        )
                    
                    with col2:
                        st.metric(
                            label="Diyabet Var",
                            value=diyabet_var,
                            delta=f"%{(diyabet_var/len(result_df)*100):.1f}"
                        )
                    
                    with col3:
                        st.metric(
                            label="Diyabet Yok",
                            value=diyabet_yok,
                            delta=f"%{(diyabet_yok/len(result_df)*100):.1f}"
                        )
                    
                    with col4:
                        if "Güven Skoru (%)" in result_df.columns:
                            avg_confidence = result_df["Güven Skoru (%)"].mean()
                            st.metric(
                                label="Ortalama Güven",
                                value=f"%{avg_confidence:.1f}"
                            )
                        else:
                            st.metric(
                                label="Ortalama Güven",
                                value="N/A"
                            )
                    
                    st.markdown("<br>", unsafe_allow_html=True)
                    
                    # Sonuçları göster
                    st.markdown("### 📋 Detaylı Tahmin Sonuçları")
                    
                    # Renkli gösterim için stil
                    def highlight_prediction(row):
                        if row["Tahmin"] == "Diyabet Var":
                            return ['background-color: #FDECEC'] * len(row)
                        else:
                            return ['background-color: #D5F5E3'] * len(row)
                    
                    styled_df = result_df.style.apply(highlight_prediction, axis=1)
                    st.dataframe(styled_df, use_container_width=True, height=400)
                    
                    st.markdown("<br>", unsafe_allow_html=True)
                    
                    # CSV indirme
                    st.markdown("### 📥 Sonuçları İndir")
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        csv_result = result_df.to_csv(index=False)
                        st.download_button(
                            label="📥 Tam Sonuçları İndir (CSV)",
                            data=csv_result,
                            file_name=f"diabetes_predictions_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                            mime="text/csv",
                            use_container_width=True
                        )
                    
                    with col2:
                        # Sadece tahmin ve güven skoru
                        summary_df = result_df[["Tahmin"] + ([col for col in result_df.columns if "%" in col] if any("%" in col for col in result_df.columns) else [])]
                        csv_summary = summary_df.to_csv(index=False)
                        st.download_button(
                            label="📊 Özet Rapor İndir (CSV)",
                            data=csv_summary,
                            file_name=f"diabetes_summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                            mime="text/csv",
                            use_container_width=True
                        )
                    
                    st.markdown("<br>", unsafe_allow_html=True)
                    
                    # Uyarı
                    st.warning("""
                    **⚠️ Önemli Uyarı:**
                    
                    Bu tahminler makine öğrenmesi modelinin otomatik çıktılarıdır. 
                    Özellikle düşük güvenli tahminler dikkatle yorumlanmalıdır. 
                    Kritik sağlık kararları için mutlaka uzman değerlendirmesi alınmalıdır.
                    """)
        
        except Exception as e:
            st.error(f"❌ Dosya okuma hatası: {e}")
    
    else:
        st.markdown("<br>", unsafe_allow_html=True)
        st.info("👆 Lütfen bir CSV dosyası yükleyin.")
