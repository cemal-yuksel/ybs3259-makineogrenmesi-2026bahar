# -*- coding: utf-8 -*-
"""
ROC-AUC CURVE ANALYSIS - LOGISTIC REGRESSION
Final model için ROC eğrisi ve AUC değeri analizi
"""

import joblib
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from sklearn.metrics import roc_curve, auc, roc_auc_score

# Model ve veriyi yükle
print("\n" + "="*80)
print("📈 ROC-AUC CURVE ANALYSIS - LOGISTIC REGRESSION")
print("="*80 + "\n")

print("📂 Model ve test verisi yükleniyor...")
final_model = joblib.load('../models/final_model.pkl')
X_test = pd.read_csv('../data/model_ready/X_test.csv')
y_test = pd.read_csv('../data/model_ready/y_test.csv').values.ravel()

print(f"✅ Model yüklendi: {type(final_model).__name__}")
print(f"✅ Test verisi: X_test {X_test.shape}, y_test {y_test.shape}")

# Tahmin olasılıklarını al
print("\n📊 Tahmin olasılıkları hesaplanıyor...")
y_pred_proba = final_model.predict_proba(X_test)[:, 1]  # Churn=1 olasılığı

# ROC Curve hesapla
print("📈 ROC eğrisi hesaplanıyor...")
fpr, tpr, thresholds = roc_curve(y_test, y_pred_proba)
roc_auc = auc(fpr, tpr)

# Alternatif hesaplama (kontrol için)
roc_auc_score_val = roc_auc_score(y_test, y_pred_proba)

print(f"\n✅ ROC-AUC Hesaplamaları:")
print(f"   • ROC-AUC (auc fonksiyonu): {roc_auc:.4f}")
print(f"   • ROC-AUC (roc_auc_score): {roc_auc_score_val:.4f}")
print(f"   • False Positive Rate (FPR) points: {len(fpr)}")
print(f"   • True Positive Rate (TPR) points: {len(tpr)}")
print(f"   • Threshold points: {len(thresholds)}")

# Önemli threshold noktalarını bul
print(f"\n📍 Önemli Threshold Noktaları:")

# Varsayılan threshold (0.5)
idx_05 = np.argmin(np.abs(thresholds - 0.5))
print(f"\n   Threshold = 0.5:")
print(f"     FPR: {fpr[idx_05]:.4f} (False Positive Rate)")
print(f"     TPR: {tpr[idx_05]:.4f} (True Positive Rate / Recall)")
print(f"     Specificity: {1 - fpr[idx_05]:.4f}")

# Youden's Index (optimal threshold)
youden_index = tpr - fpr
idx_optimal = np.argmax(youden_index)
print(f"\n   Optimal Threshold (Youden's Index): {thresholds[idx_optimal]:.4f}")
print(f"     FPR: {fpr[idx_optimal]:.4f}")
print(f"     TPR: {tpr[idx_optimal]:.4f}")
print(f"     Specificity: {1 - fpr[idx_optimal]:.4f}")
print(f"     Youden's J: {youden_index[idx_optimal]:.4f}")

# En yakın köşe (0,1) noktasına
distances = np.sqrt((fpr - 0)**2 + (tpr - 1)**2)
idx_nearest = np.argmin(distances)
print(f"\n   Nearest to (0,1) point - Threshold: {thresholds[idx_nearest]:.4f}")
print(f"     FPR: {fpr[idx_nearest]:.4f}")
print(f"     TPR: {tpr[idx_nearest]:.4f}")
print(f"     Distance to (0,1): {distances[idx_nearest]:.4f}")

# ROC Eğrisi çiz
print(f"\n🎨 ROC eğrisi çiziliyor...")

fig = go.Figure()

# ROC Curve
fig.add_trace(go.Scatter(
    x=fpr,
    y=tpr,
    mode='lines',
    name=f'Logistic Regression (AUC = {roc_auc:.4f})',
    line=dict(color='#2E86AB', width=3),
    hovertemplate='<b>FPR:</b> %{x:.4f}<br><b>TPR:</b> %{y:.4f}<extra></extra>'
))

# Diagonal (Random Classifier)
fig.add_trace(go.Scatter(
    x=[0, 1],
    y=[0, 1],
    mode='lines',
    name='Random Classifier (AUC = 0.5000)',
    line=dict(color='#C73E1D', width=2, dash='dash'),
    hovertemplate='<b>Random</b><extra></extra>'
))

# Optimal Point
fig.add_trace(go.Scatter(
    x=[fpr[idx_optimal]],
    y=[tpr[idx_optimal]],
    mode='markers',
    name=f'Optimal Threshold = {thresholds[idx_optimal]:.3f}',
    marker=dict(color='#F18F01', size=12, symbol='star'),
    hovertemplate=f'<b>Optimal Point</b><br>Threshold: {thresholds[idx_optimal]:.4f}<br>FPR: {fpr[idx_optimal]:.4f}<br>TPR: {tpr[idx_optimal]:.4f}<extra></extra>'
))

# Current Threshold (0.5)
fig.add_trace(go.Scatter(
    x=[fpr[idx_05]],
    y=[tpr[idx_05]],
    mode='markers',
    name='Current Threshold = 0.500',
    marker=dict(color='#6A994E', size=10, symbol='circle'),
    hovertemplate=f'<b>Current Point</b><br>Threshold: 0.5000<br>FPR: {fpr[idx_05]:.4f}<br>TPR: {tpr[idx_05]:.4f}<extra></extra>'
))

# Layout
fig.update_layout(
    title={
        'text': f'ROC Curve - Logistic Regression<br><sub>AUC = {roc_auc:.4f} (Excellent Discriminative Power)</sub>',
        'x': 0.5,
        'xanchor': 'center',
        'font': {'size': 22, 'family': 'Arial Black', 'color': '#1F2937'}
    },
    xaxis_title='False Positive Rate (FPR) - 1 - Specificity',
    yaxis_title='True Positive Rate (TPR) - Recall / Sensitivity',
    template='plotly_white',
    paper_bgcolor='#FBFBF8',
    plot_bgcolor='#FBFBF8',
    font={'family': 'Arial', 'size': 13, 'color': '#374151'},
    showlegend=True,
    legend=dict(
        x=0.98,
        y=0.02,
        xanchor='right',
        yanchor='bottom',
        bgcolor='rgba(255,255,255,0.9)',
        bordercolor='#E5E7EB',
        borderwidth=1
    ),
    width=900,
    height=700,
    margin=dict(l=80, r=40, t=100, b=80)
)

fig.update_xaxes(
    showgrid=True,
    gridcolor='#E5E7EB',
    zeroline=True,
    zerolinecolor='#9CA3AF',
    range=[-0.02, 1.02]
)

fig.update_yaxes(
    showgrid=True,
    gridcolor='#E5E7EB',
    zeroline=True,
    zerolinecolor='#9CA3AF',
    range=[-0.02, 1.02]
)

# Grafik kaydet
html_path = '../figures/roc_curve_logistic_regression.html'
png_path = '../figures/roc_curve_logistic_regression.png'

fig.write_html(html_path)
print(f"✅ ROC eğrisi kaydedildi: {html_path}")

try:
    fig.write_image(png_path)
    print(f"✅ PNG formatı kaydedildi: {png_path}")
except Exception as e:
    print(f"⚠️  PNG kaydı yapılamadı: {png_path}")

# CSV rapor oluştur
roc_data = pd.DataFrame({
    'Threshold': thresholds,
    'FPR': fpr,
    'TPR': tpr,
    'Specificity': 1 - fpr,
    'Youden_Index': tpr - fpr
})

csv_path = '../reports/csv/roc_curve_analysis.csv'
roc_data.to_csv(csv_path, index=False, encoding='utf-8-sig')
print(f"✅ ROC veri tablosu kaydedildi: {csv_path}")

# Summary rapor
print("\n" + "="*80)
print("📊 ROC-AUC ANALIZ ÖZETİ")
print("="*80)

print(f"\n🎯 ROC-AUC Değeri: {roc_auc:.4f}")
print(f"\n   Yorumlama:")
if roc_auc >= 0.9:
    print(f"   ⭐⭐⭐ Mükemmel (Excellent): AUC ≥ 0.90")
elif roc_auc >= 0.8:
    print(f"   ⭐⭐ İyi (Good): 0.80 ≤ AUC < 0.90")
    print(f"   → Model sınıf ayrımında başarılı")
elif roc_auc >= 0.7:
    print(f"   ⭐ Kabul Edilebilir (Fair): 0.70 ≤ AUC < 0.80")
elif roc_auc >= 0.6:
    print(f"   ⚠️  Zayıf (Poor): 0.60 ≤ AUC < 0.70")
else:
    print(f"   ❌ Başarısız (Fail): AUC < 0.60")

print(f"\n📍 Threshold Önerileri:")
print(f"\n   1️⃣ Current (0.5000):")
print(f"      • Recall (TPR): {tpr[idx_05]:.2%} (Churn müşterilerinin {tpr[idx_05]:.0%}'ini yakala)")
print(f"      • FPR: {fpr[idx_05]:.2%} (No Churn'ün {fpr[idx_05]:.0%}'ü yanlış churn denir)")
print(f"      • Specificity: {1 - fpr[idx_05]:.2%}")

print(f"\n   2️⃣ Optimal ({thresholds[idx_optimal]:.4f}):")
print(f"      • Recall (TPR): {tpr[idx_optimal]:.2%} (Churn müşterilerinin {tpr[idx_optimal]:.0%}'ini yakala)")
print(f"      • FPR: {fpr[idx_optimal]:.2%} (No Churn'ün {fpr[idx_optimal]:.0%}'ü yanlış churn denir)")
print(f"      • Specificity: {1 - fpr[idx_optimal]:.2%}")
print(f"      • Youden's J: {youden_index[idx_optimal]:.4f} (maksimize edildi)")

print(f"\n💡 Business Insight:")
if thresholds[idx_optimal] < 0.5:
    print(f"   • Optimal threshold (Threshold = {thresholds[idx_optimal]:.3f}) şu ankinden DÜŞÜK")
    print(f"   • Bu threshold'u kullanmak:")
    print(f"     ✅ ARTIRIYOR: Recall ({tpr[idx_05]:.2%} → {tpr[idx_optimal]:.2%}) - Daha fazla churn müşterisi yakalanır")
    print(f"     ❌ ARTIRIYOR: False Positive Rate ({fpr[idx_05]:.2%} → {fpr[idx_optimal]:.2%}) - Daha fazla yanlış alarm")
    print(f"   • Karar: Müşteri kaybetmek maliyetliyse, düşük threshold tercih edilebilir")
else:
    print(f"   • Optimal threshold (Threshold = {thresholds[idx_optimal]:.3f}) şu ankinden YÜKSEK")
    print(f"   • Bu threshold'u kullanmak:")
    print(f"     ❌ AZALTIYOR: Recall - Daha az churn müşterisi yakalanır")
    print(f"     ✅ AZALTIYOR: False Positive Rate - Daha az yanlış alarm")
    print(f"   • Karar: Gereksiz retention kampanyası maliyetliyse, yüksek threshold tercih edilebilir")

print(f"\n⚖️  Hassasiyet-Duyarlılık Dengesi:")
print(f"   • Yüksek Recall istiyorsan → Threshold'u düşür (daha fazla churn yakalarsın, ama false positive artar)")
print(f"   • Düşük FPR istiyorsan → Threshold'u yükselt (daha az yanlış alarm, ama churn kaçırırsın)")
print(f"   • Optimal denge → Youden's Index maksimum olan nokta (Threshold = {thresholds[idx_optimal]:.4f})")

print("\n" + "="*80)
print("✅ ROC-AUC ANALİZİ TAMAMLANDI")
print("="*80 + "\n")

print("📁 Oluşturulan Dosyalar:")
print(f"   • {html_path}")
print(f"   • {png_path if 'Exception' not in str(e) else '(PNG kaydedilemedi)'}")
print(f"   • {csv_path}")
print()
