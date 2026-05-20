"""
Monitoring Sayfası - Tahmin Geçmişi ve Sistem İzleme
Shneiderman Kural 3-7: Bilgilendirici geri bildirim, kullanıcı kontrolü
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
from datetime import datetime, timedelta

def load_prediction_log():
    """Tahmin logunu yükle"""
    log_path = Path("logs/prediction_log.csv")
    
    if log_path.exists():
        try:
            df = pd.read_csv(log_path)
            df["timestamp"] = pd.to_datetime(df["timestamp"])
            return df, None
        except Exception as e:
            return None, str(e)
    else:
        return pd.DataFrame(), "Log dosyası henüz oluşturulmadı"

def show():
    """Monitoring sayfası içeriği"""
    
    st.markdown("""
    <div class="hero-card">
        <h1 style="margin: 0; color: #1F2937;">📡 Monitoring ve Tahmin Geçmişi</h1>
        <p style="margin-top: 8px; color: #6B7280;">
            Sistem performansı, tahmin istatistikleri ve kullanım analizi
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Log verilerini yükle
    log_df, error = load_prediction_log()
    
    if error and log_df is not None and len(log_df) == 0:
        st.info("""
        **ℹ️ Henüz Tahmin Yapılmadı**
        
        Tahmin geçmişi görüntülemek için önce "Tekil Tahmin" veya "Toplu Tahmin" 
        sayfalarından tahmin yapın. Tüm tahminler otomatik olarak loglanacaktır.
        """)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Placeholder metrikler
        st.markdown("### 📊 Sistem Durumu")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(label="Toplam Tahmin", value="0")
        
        with col2:
            st.metric(label="Diyabet Var", value="0")
        
        with col3:
            st.metric(label="Diyabet Yok", value="0")
        
        with col4:
            st.metric(label="Ort. Güven", value="N/A")
        
        st.stop()
    
    elif error:
        st.error(f"❌ Log yükleme hatası: {error}")
        st.stop()
    
    # İstatistikler
    st.markdown("### 📊 Tahmin İstatistikleri")
    
    total_predictions = len(log_df)
    diyabet_var = (log_df["prediction"] == "Diyabet Var").sum()
    diyabet_yok = (log_df["prediction"] == "Diyabet Yok").sum()
    
    if "confidence" in log_df.columns:
        avg_confidence = log_df["confidence"].mean()
    else:
        avg_confidence = None
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="Toplam Tahmin",
            value=total_predictions,
            delta=f"Son 24 saat" if total_predictions > 0 else None
        )
    
    with col2:
        st.metric(
            label="Diyabet Var",
            value=diyabet_var,
            delta=f"%{(diyabet_var/total_predictions*100):.1f}" if total_predictions > 0 else None
        )
    
    with col3:
        st.metric(
            label="Diyabet Yok",
            value=diyabet_yok,
            delta=f"%{(diyabet_yok/total_predictions*100):.1f}" if total_predictions > 0 else None
        )
    
    with col4:
        if avg_confidence is not None:
            st.metric(
                label="Ortalama Güven",
                value=f"%{avg_confidence:.1f}",
                delta="Yüksek" if avg_confidence >= 80 else "Orta" if avg_confidence >= 60 else "Düşük"
            )
        else:
            st.metric(label="Ortalama Güven", value="N/A")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Zaman Serisi Analizi
    st.markdown("### 📈 Tahmin Zaman Serisi")
    
    if len(log_df) > 0:
        # Günlük tahmin sayısı
        log_df["date"] = log_df["timestamp"].dt.date
        daily_counts = log_df.groupby("date").size().reset_index(name="count")
        
        fig = px.line(
            daily_counts,
            x="date",
            y="count",
            title="Günlük Tahmin Sayısı",
            labels={"date": "Tarih", "count": "Tahmin Sayısı"},
            markers=True
        )
        
        fig.update_layout(
            template="plotly_white",
            height=400,
            hovermode="x unified"
        )
        
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Zaman serisi için yeterli veri yok.")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Tahmin Dağılımı
    st.markdown("### 📊 Tahmin Dağılımı")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Pie chart
        prediction_counts = log_df["prediction"].value_counts()
        
        fig = go.Figure(data=[go.Pie(
            labels=prediction_counts.index,
            values=prediction_counts.values,
            hole=0.4,
            marker=dict(colors=["#6A994E", "#C73E1D"])
        )])
        
        fig.update_layout(
            title="Tahmin Sınıf Dağılımı",
            template="plotly_white",
            height=350
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Güven skoru dağılımı
        if "confidence" in log_df.columns and log_df["confidence"].notna().any():
            fig = px.histogram(
                log_df.dropna(subset=["confidence"]),
                x="confidence",
                nbins=20,
                title="Güven Skoru Dağılımı",
                labels={"confidence": "Güven Skoru (%)", "count": "Frekans"},
                color_discrete_sequence=["#2E86AB"]
            )
            
            fig.update_layout(
                template="plotly_white",
                height=350
            )
            
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Güven skoru verisi mevcut değil.")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Son Tahminler
    st.markdown("### 📋 Son 20 Tahmin")
    
    recent_df = log_df.tail(20).sort_values("timestamp", ascending=False)
    
    # Görüntüleme için kolon seçimi
    display_cols = ["timestamp", "prediction"]
    if "confidence" in recent_df.columns:
        display_cols.append("confidence")
    
    # Feature kolonlarını ekle (varsa)
    feature_cols = [col for col in recent_df.columns if col not in ["timestamp", "prediction", "confidence"]]
    display_cols.extend(feature_cols[:5])  # İlk 5 feature'ı göster
    
    st.dataframe(
        recent_df[display_cols].reset_index(drop=True),
        use_container_width=True,
        height=400
    )
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Sistem Durumu
    st.markdown("### 🖥️ Sistem Durumu")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="success-box">
            <h4 style="margin: 0;">✅ Model Durumu</h4>
            <p style="margin-top: 8px;">
                <b>Durum:</b> Aktif<br>
                <b>Model:</b> Random Forest<br>
                <b>Version:</b> 1.0<br>
                <b>Son Güncelleme:</b> 5 Mayıs 2026
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="info-box">
            <h4 style="margin: 0;">📊 Loglama</h4>
            <p style="margin-top: 8px;">
                <b>Durum:</b> Aktif<br>
                <b>Log Dosyası:</b> prediction_log.csv<br>
                <b>Toplam Kayıt:</b> {len(log_df)}<br>
                <b>Son Tahmin:</b> {log_df['timestamp'].max().strftime('%Y-%m-%d %H:%M') if len(log_df) > 0 else 'N/A'}
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="warning-box">
            <h4 style="margin: 0;">⚠️ Uyarılar</h4>
            <p style="margin-top: 8px;">
                <b>Drift Detection:</b> Devre Dışı<br>
                <b>Retraining:</b> Planlanmadı<br>
                <b>Model Monitoring:</b> Manuel<br>
                <b>Alert System:</b> Devre Dışı
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Feature Drift Placeholder
    st.markdown("### 🔍 Feature Drift Analizi (Placeholder)")
    
    st.info("""
    **ℹ️ Feature Drift İzleme (Gelecek Özellik)**
    
    Bu bölümde şunlar izlenebilir:
    - Input feature dağılımlarının zaman içinde kayması
    - Train verisi ile production verisi karşılaştırması
    - Anomali tespiti
    - Model performance degradation uyarısı
    
    **Not:** Bu özellik şu anda aktif değildir. Manuel inceleme önerilir.
    """)
    
    st.markdown("<br>", unsafe_help=True)
    
    # Log İndirme
    st.markdown("### 📥 Log Dosyasını İndir")
    
    col1, col2 = st.columns(2)
    
    with col1:
        csv = log_df.to_csv(index=False)
        st.download_button(
            label="📥 Tam Log İndir (CSV)",
            data=csv,
            file_name=f"prediction_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv",
            use_container_width=True
        )
    
    with col2:
        # Son 100 kayıt
        recent_csv = log_df.tail(100).to_csv(index=False)
        st.download_button(
            label="📊 Son 100 Kayıt İndir",
            data=recent_csv,
            file_name=f"recent_predictions_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv",
            use_container_width=True
        )
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Öneriler
    st.success("""
    **💡 Monitoring En İyi Pratikleri:**
    
    1. **Düzenli Kontrol:** Tahmin istatistiklerini haftalık inceleyin
    2. **Drift İzleme:** Feature dağılımlarındaki değişimleri takip edin
    3. **Performance Monitoring:** Gerçek sonuçlarla model tahminlerini karşılaştırın
    4. **Log Arşivleme:** Prediction log dosyasını düzenli yedekleyin
    5. **Alert Sistemi:** Anormal tahmin patternleri için uyarı kurun
    6. **Retraining:** Performans düşüşünde modeli yeniden eğitin
    """)
