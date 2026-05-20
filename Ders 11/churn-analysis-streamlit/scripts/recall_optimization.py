"""
================================================================================
RECALL OPTIMIZATION - Threshold Tuning & Business Cost Analysis
================================================================================
Model Expert'ten final modeli devralarak Recall iyileştirme
Strateji: Threshold tuning + Business cost optimization
================================================================================
"""

import os
import joblib
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
from prettytable import PrettyTable

from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    roc_auc_score, confusion_matrix, classification_report,
    precision_recall_curve, roc_curve
)

Path('../figures').mkdir(parents=True, exist_ok=True)
Path('../reports/csv').mkdir(parents=True, exist_ok=True)

# Professional palette
PROFESSIONAL_PALETTE = [
    "#2E86AB", "#A23B72", "#F18F01", "#C73E1D", "#6A994E",
    "#BC4B51", "#8E7DBE", "#F77F00", "#06A77D", "#D4A574"
]

def apply_premium_layout(fig, title):
    """Profesyonel grafik düzeni"""
    fig.update_layout(
        title={
            "text": title,
            "x": 0.03,
            "xanchor": "left",
            "font": {"size": 24, "family": "Arial Black", "color": "#1F2937"}
        },
        template="plotly_white",
        paper_bgcolor="#FBFBF8",
        plot_bgcolor="#FBFBF8",
        font={"family": "Arial", "size": 13, "color": "#374151"},
        margin=dict(l=60, r=40, t=80, b=60)
    )
    fig.update_xaxes(showgrid=True, gridcolor="#E5E7EB", zeroline=False)
    fig.update_yaxes(showgrid=True, gridcolor="#E5E7EB", zeroline=False)
    return fig

def save_figure(fig, filename):
    """Grafik kaydet"""
    html_path = f"../figures/{filename}.html"
    fig.write_html(html_path)
    print(f"   ✅ Grafik kaydedildi: {html_path}")

def calculate_business_cost(tn, fp, fn, tp, fn_cost=3000, fp_cost=50):
    """Business cost hesapla"""
    fn_total = fn * fn_cost  # Müşteri kaybı (LTV)
    fp_total = fp * fp_cost  # Gereksiz kampanya
    return fn_total + fp_total, fn_total, fp_total

print("="*80)
print("RECALL OPTIMIZATION - Threshold Tuning & Business Cost Analysis")
print("="*80)

# ============================================================================
# PHASE 1: MODEL VE VERİ YÜKLEME
# ============================================================================
print("\n" + "="*80)
print("PHASE 1: MODEL VE VERİ YÜKLEME")
print("="*80)

print("\n1. FINAL MODEL YÜKLEME:")
final_model = joblib.load('../models/final_model.pkl')
print(f"   ✅ Model yüklendi: {type(final_model).__name__}")

print("\n2. TEST VERİSİ YÜKLEME:")
X_test = pd.read_csv('../data/model_ready/X_test.csv')
y_test = pd.read_csv('../data/model_ready/y_test.csv').values.ravel()
print(f"   X_test: {X_test.shape}")
print(f"   y_test: {y_test.shape}")

print("\n3. BASELINE PERFORMANS (Threshold=0.5):")
y_pred_proba = final_model.predict_proba(X_test)[:, 1]
y_pred_baseline = (y_pred_proba >= 0.5).astype(int)

baseline_recall = recall_score(y_test, y_pred_baseline, average='weighted')
baseline_precision = precision_score(y_test, y_pred_baseline, average='weighted')
baseline_f1 = f1_score(y_test, y_pred_baseline, average='weighted')

# Binary metrics for Churn class
baseline_recall_churn = recall_score(y_test, y_pred_baseline, pos_label=1)
baseline_precision_churn = precision_score(y_test, y_pred_baseline, pos_label=1)
baseline_f1_churn = f1_score(y_test, y_pred_baseline, pos_label=1)

baseline_cm = confusion_matrix(y_test, y_pred_baseline)
tn_base, fp_base, fn_base, tp_base = baseline_cm.ravel()

print(f"   Recall (Weighted): {baseline_recall:.4f}")
print(f"   Precision (Weighted): {baseline_precision:.4f}")
print(f"   F1-Score (Weighted): {baseline_f1:.4f}")
print(f"   🎯 Recall CHURN CLASS (Business Kritik): {baseline_recall_churn:.4f}")
print(f"   🎯 Precision CHURN CLASS: {baseline_precision_churn:.4f}")
print(f"   🎯 F1 CHURN CLASS: {baseline_f1_churn:.4f}")
print(f"   Confusion Matrix: TN={tn_base}, FP={fp_base}, FN={fn_base}, TP={tp_base}")

baseline_cost, baseline_fn_cost, baseline_fp_cost = calculate_business_cost(
    tn_base, fp_base, fn_base, tp_base
)
print(f"   Business Cost: ${baseline_cost:,} (FN: ${baseline_fn_cost:,}, FP: ${baseline_fp_cost:,})")

# ============================================================================
# PHASE 2: THRESHOLD TUNING ANALYSIS
# ============================================================================
print("\n" + "="*80)
print("PHASE 2: THRESHOLD TUNING ANALYSIS")
print("="*80)

print("\n1. THRESHOLD RANGE: 0.1 - 0.9 (Step: 0.05)")

thresholds = np.arange(0.1, 0.91, 0.05)
results = []

for threshold in thresholds:
    y_pred = (y_pred_proba >= threshold).astype(int)
    
    # Weighted metrics (overall)
    recall = recall_score(y_test, y_pred, average='weighted')
    precision = precision_score(y_test, y_pred, average='weighted')
    f1 = f1_score(y_test, y_pred, average='weighted')
    accuracy = accuracy_score(y_test, y_pred)
    
    # Binary metrics for Churn class (Yes=1) - Business Critical
    recall_churn = recall_score(y_test, y_pred, pos_label=1)
    precision_churn = precision_score(y_test, y_pred, pos_label=1)
    f1_churn = f1_score(y_test, y_pred, pos_label=1)
    
    cm = confusion_matrix(y_test, y_pred)
    tn, fp, fn, tp = cm.ravel()
    
    total_cost, fn_cost, fp_cost = calculate_business_cost(tn, fp, fn, tp)
    
    results.append({
        'Threshold': threshold,
        'Recall': recall,
        'Precision': precision,
        'F1': f1,
        'Accuracy': accuracy,
        'Recall_Churn': recall_churn,
        'Precision_Churn': precision_churn,
        'F1_Churn': f1_churn,
        'TN': tn,
        'FP': fp,
        'FN': fn,
        'TP': tp,
        'Total_Cost': total_cost,
        'FN_Cost': fn_cost,
        'FP_Cost': fp_cost
    })

results_df = pd.DataFrame(results)

# En düşük business cost
best_cost_idx = results_df['Total_Cost'].idxmin()
best_cost_row = results_df.iloc[best_cost_idx]

# En yüksek Recall (Churn class - Business Critical)
best_recall_idx = results_df['Recall_Churn'].idxmax()
best_recall_row = results_df.iloc[best_recall_idx]

# En yüksek F1 (Churn class)
best_f1_idx = results_df['F1_Churn'].idxmax()
best_f1_row = results_df.iloc[best_f1_idx]

print("\n2. THRESHOLD TUNING SONUÇLARI:")
print(f"\n   📊 EN DÜŞÜK BUSINESS COST:")
print(f"      Threshold: {best_cost_row['Threshold']:.2f}")
print(f"      Total Cost: ${best_cost_row['Total_Cost']:,.0f}")
print(f"      Recall (Weighted): {best_cost_row['Recall']:.4f}")
print(f"      🎯 Recall CHURN CLASS: {best_cost_row['Recall_Churn']:.4f}")
print(f"      Precision (Weighted): {best_cost_row['Precision']:.4f}")
print(f"      🎯 Precision CHURN CLASS: {best_cost_row['Precision_Churn']:.4f}")
print(f"      F1 (Weighted): {best_cost_row['F1']:.4f}")
print(f"      🎯 F1 CHURN CLASS: {best_cost_row['F1_Churn']:.4f}")
print(f"      FN: {int(best_cost_row['FN'])}, FP: {int(best_cost_row['FP'])}")

print(f"\n   🎯 EN YÜKSEK RECALL (CHURN CLASS - BUSİNESS KRİTİK):")
print(f"      Threshold: {best_recall_row['Threshold']:.2f}")
print(f"      🎯 Recall CHURN CLASS: {best_recall_row['Recall_Churn']:.4f}")
print(f"      🎯 Precision CHURN CLASS: {best_recall_row['Precision_Churn']:.4f}")
print(f"      🎯 F1 CHURN CLASS: {best_recall_row['F1_Churn']:.4f}")
print(f"      Recall (Weighted): {best_recall_row['Recall']:.4f}")
print(f"      Precision (Weighted): {best_recall_row['Precision']:.4f}")
print(f"      F1 (Weighted): {best_recall_row['F1']:.4f}")
print(f"      Total Cost: ${best_recall_row['Total_Cost']:,.0f}")
print(f"      FN: {int(best_recall_row['FN'])}, FP: {int(best_recall_row['FP'])}")

print(f"\n   ⚖️ EN YÜKSEK F1 (CHURN CLASS - DENGELI):")
print(f"      Threshold: {best_f1_row['Threshold']:.2f}")
print(f"      🎯 F1 CHURN CLASS: {best_f1_row['F1_Churn']:.4f}")
print(f"      🎯 Recall CHURN CLASS: {best_f1_row['Recall_Churn']:.4f}")
print(f"      🎯 Precision CHURN CLASS: {best_f1_row['Precision_Churn']:.4f}")
print(f"      F1 (Weighted): {best_f1_row['F1']:.4f}")
print(f"      Recall (Weighted): {best_f1_row['Recall']:.4f}")
print(f"      Precision (Weighted): {best_f1_row['Precision']:.4f}")
print(f"      Total Cost: ${best_f1_row['Total_Cost']:,.0f}")
print(f"      FN: {int(best_f1_row['FN'])}, FP: {int(best_f1_row['FP'])}")

# CSV kaydet
results_df.to_csv('../reports/csv/threshold_optimization_results.csv', index=False)
print(f"\n   ✅ Sonuçlar kaydedildi: reports/csv/threshold_optimization_results.csv")

# ============================================================================
# PHASE 3: GÖRSEL ANALİZ
# ============================================================================
print("\n" + "="*80)
print("PHASE 3: GÖRSEL ANALİZ")
print("="*80)

print("\n📊 5 PROFESYONEL GRAFİK ÜRETİLİYOR...")

# Grafik 1: Recall vs Threshold (Both Weighted and Churn Class)
print("\n1. Recall vs Threshold...")
fig1 = go.Figure()
fig1.add_trace(go.Scatter(
    x=results_df['Threshold'],
    y=results_df['Recall_Churn'],
    mode='lines+markers',
    name='Recall (Churn Class) - Business Critical',
    line=dict(color='#2E86AB', width=4),
    marker=dict(size=10)
))
fig1.add_trace(go.Scatter(
    x=results_df['Threshold'],
    y=results_df['Recall'],
    mode='lines+markers',
    name='Recall (Weighted - Overall)',
    line=dict(color='#A23B72', width=2, dash='dash'),
    marker=dict(size=6)
))
fig1.add_hline(
    y=baseline_recall_churn, 
    line_dash="dash", 
    line_color="#C73E1D",
    annotation_text=f"Baseline Churn Recall (0.5): {baseline_recall_churn:.4f}"
)
fig1.add_vline(
    x=best_recall_row['Threshold'],
    line_dash="dash",
    line_color="#6A994E",
    annotation_text=f"Max Churn Recall: {best_recall_row['Threshold']:.2f}"
)
fig1.update_xaxes(title="Threshold")
fig1.update_yaxes(title="Recall")
fig1 = apply_premium_layout(fig1, "Recall vs Threshold - Churn Class (Business Critical)")
save_figure(fig1, "recall_optimization_recall_vs_threshold")

# Grafik 2: Precision-Recall Trade-off
print("2. Precision-Recall Trade-off...")
fig2 = go.Figure()
fig2.add_trace(go.Scatter(
    x=results_df['Recall'],
    y=results_df['Precision'],
    mode='lines+markers',
    text=results_df['Threshold'].apply(lambda x: f"Th={x:.2f}"),
    hovertemplate='<b>Threshold: %{text}</b><br>Recall: %{x:.4f}<br>Precision: %{y:.4f}<extra></extra>',
    line=dict(color='#A23B72', width=3),
    marker=dict(size=10, color=results_df['Threshold'], colorscale='Viridis', showscale=True)
))
fig2.add_trace(go.Scatter(
    x=[baseline_recall],
    y=[baseline_precision],
    mode='markers',
    name='Baseline (0.5)',
    marker=dict(size=15, color='gray', symbol='x')
))
fig2.add_trace(go.Scatter(
    x=[best_cost_row['Recall']],
    y=[best_cost_row['Precision']],
    mode='markers',
    name=f"Optimal ({best_cost_row['Threshold']:.2f})",
    marker=dict(size=15, color='#C73E1D', symbol='star')
))
fig2.update_xaxes(title="Recall")
fig2.update_yaxes(title="Precision")
fig2 = apply_premium_layout(fig2, "Precision-Recall Trade-off Curve")
save_figure(fig2, "recall_optimization_precision_recall_tradeoff")

# Grafik 3: Business Cost vs Threshold
print("3. Business Cost vs Threshold...")
fig3 = go.Figure()
fig3.add_trace(go.Scatter(
    x=results_df['Threshold'],
    y=results_df['Total_Cost'],
    mode='lines+markers',
    name='Total Cost',
    line=dict(color='#C73E1D', width=3),
    marker=dict(size=8)
))
fig3.add_trace(go.Scatter(
    x=results_df['Threshold'],
    y=results_df['FN_Cost'],
    mode='lines',
    name='FN Cost (LTV Kaybı)',
    line=dict(color='#F18F01', width=2, dash='dash')
))
fig3.add_trace(go.Scatter(
    x=results_df['Threshold'],
    y=results_df['FP_Cost'],
    mode='lines',
    name='FP Cost (Kampanya)',
    line=dict(color='#6A994E', width=2, dash='dot')
))
fig3.add_vline(
    x=best_cost_row['Threshold'],
    line_dash="dash",
    line_color="gray",
    annotation_text=f"Min Cost: {best_cost_row['Threshold']:.2f}"
)
fig3.update_xaxes(title="Threshold")
fig3.update_yaxes(title="Business Cost ($)")
fig3 = apply_premium_layout(fig3, "Business Cost vs Threshold - Maliyet Optimizasyonu")
save_figure(fig3, "recall_optimization_business_cost")

# Grafik 4: FN vs FP Trade-off
print("4. False Negative vs False Positive Trade-off...")
fig4 = go.Figure()
fig4.add_trace(go.Scatter(
    x=results_df['FP'],
    y=results_df['FN'],
    mode='lines+markers',
    text=results_df['Threshold'].apply(lambda x: f"Th={x:.2f}"),
    hovertemplate='<b>%{text}</b><br>FP: %{x}<br>FN: %{y}<extra></extra>',
    line=dict(color='#8E7DBE', width=3),
    marker=dict(size=10, color=results_df['Threshold'], colorscale='RdYlGn_r', showscale=True)
))
fig4.add_trace(go.Scatter(
    x=[fp_base],
    y=[fn_base],
    mode='markers',
    name='Baseline (0.5)',
    marker=dict(size=15, color='gray', symbol='x')
))
fig4.add_trace(go.Scatter(
    x=[int(best_cost_row['FP'])],
    y=[int(best_cost_row['FN'])],
    mode='markers',
    name=f"Optimal ({best_cost_row['Threshold']:.2f})",
    marker=dict(size=15, color='#C73E1D', symbol='star')
))
fig4.update_xaxes(title="False Positive (Gereksiz Kampanya)")
fig4.update_yaxes(title="False Negative (Kaybedilen Müşteri)")
fig4 = apply_premium_layout(fig4, "False Negative vs False Positive - Hata Trade-off")
save_figure(fig4, "recall_optimization_fn_vs_fp")

# Grafik 5: Multi-Metric Dashboard
print("5. Multi-Metric Dashboard...")
fig5 = go.Figure()

# Normalize metrics to 0-1 for comparison
results_df_norm = results_df.copy()
results_df_norm['Total_Cost_Norm'] = 1 - (results_df_norm['Total_Cost'] - results_df_norm['Total_Cost'].min()) / (results_df_norm['Total_Cost'].max() - results_df_norm['Total_Cost'].min())

fig5.add_trace(go.Scatter(
    x=results_df['Threshold'],
    y=results_df['Recall'],
    mode='lines',
    name='Recall',
    line=dict(color='#2E86AB', width=2)
))
fig5.add_trace(go.Scatter(
    x=results_df['Threshold'],
    y=results_df['Precision'],
    mode='lines',
    name='Precision',
    line=dict(color='#A23B72', width=2)
))
fig5.add_trace(go.Scatter(
    x=results_df['Threshold'],
    y=results_df['F1'],
    mode='lines',
    name='F1-Score',
    line=dict(color='#F18F01', width=2)
))
fig5.add_trace(go.Scatter(
    x=results_df['Threshold'],
    y=results_df_norm['Total_Cost_Norm'],
    mode='lines',
    name='Cost Efficiency (Normalized)',
    line=dict(color='#6A994E', width=2, dash='dash')
))
fig5.update_xaxes(title="Threshold")
fig5.update_yaxes(title="Metric Value", range=[0, 1])
fig5 = apply_premium_layout(fig5, "Multi-Metric Dashboard - Threshold Karşılaştırması")
save_figure(fig5, "recall_optimization_multi_metric_dashboard")

print("\n✅ 5 PROFESYONEL GRAFİK OLUŞTURULDU")

# ============================================================================
# PHASE 4: ÖNERİ VE KARŞILAŞTIRMA
# ============================================================================
print("\n" + "="*80)
print("PHASE 4: FINAL ÖNERİ VE KARŞILAŞTIRMA")
print("="*80)

print("\n📊 THRESHOLD KARŞILAŞTIRMA TABLOSu:")

comparison_table = PrettyTable()
comparison_table.field_names = ["Senaryo", "Threshold", "Recall\nChurn", "Prec.\nChurn", "F1\nChurn", "FN", "FP", "Cost"]

comparison_table.add_row([
    "Baseline (Mevcut)",
    "0.50",
    f"{baseline_recall_churn:.4f}",
    f"{baseline_precision_churn:.4f}",
    f"{baseline_f1_churn:.4f}",
    fn_base,
    fp_base,
    f"${baseline_cost:,}"
])

comparison_table.add_row([
    "En Düşük Maliyet 💰",
    f"{best_cost_row['Threshold']:.2f}",
    f"{best_cost_row['Recall_Churn']:.4f}",
    f"{best_cost_row['Precision_Churn']:.4f}",
    f"{best_cost_row['F1_Churn']:.4f}",
    int(best_cost_row['FN']),
    int(best_cost_row['FP']),
    f"${best_cost_row['Total_Cost']:,.0f}"
])

comparison_table.add_row([
    "En Yüksek Recall 🎯",
    f"{best_recall_row['Threshold']:.2f}",
    f"{best_recall_row['Recall_Churn']:.4f}",
    f"{best_recall_row['Precision_Churn']:.4f}",
    f"{best_recall_row['F1_Churn']:.4f}",
    int(best_recall_row['FN']),
    int(best_recall_row['FP']),
    f"${best_recall_row['Total_Cost']:,.0f}"
])

comparison_table.add_row([
    "En Yüksek F1 ⚖️",
    f"{best_f1_row['Threshold']:.2f}",
    f"{best_f1_row['Recall_Churn']:.4f}",
    f"{best_f1_row['Precision_Churn']:.4f}",
    f"{best_f1_row['F1_Churn']:.4f}",
    int(best_f1_row['FN']),
    int(best_f1_row['FP']),
    f"${best_f1_row['Total_Cost']:,.0f}"
])

print(comparison_table)

# İyileşme hesapla (En yüksek Churn Recall senaryosu)
recall_churn_improvement = best_recall_row['Recall_Churn'] - baseline_recall_churn
fn_reduction = fn_base - int(best_recall_row['FN'])
cost_diff = best_recall_row['Total_Cost'] - baseline_cost  # Pozitif = maliyet artışı

# Business cost optimal senaryosu
cost_saving = baseline_cost - best_cost_row['Total_Cost']
fn_reduction_cost = fn_base - int(best_cost_row['FN'])

print("\n🎯 ÖNERİLEN STRATEJI 1: EN YÜKSEK CHURN RECALL (BUSİNESS KRİTİK)")
print(f"   Threshold: {best_recall_row['Threshold']:.2f}")
print(f"\n   CHURN RECALL İYİLEŞMESİ:")
print(f"      • {baseline_recall_churn:.4f} → {best_recall_row['Recall_Churn']:.4f} (+{recall_churn_improvement:.4f} / {recall_churn_improvement/baseline_recall_churn*100:+.2f}%)")
print(f"\n   FALSE NEGATIVE AZALMA:")
print(f"      • {fn_base} → {int(best_recall_row['FN'])} (-{fn_reduction} churn müşteri kaçırılıyor)")
print(f"      • {fn_reduction} müşteri daha fazla yakalanıyor → Retention kampanyası fırsatı!")
print(f"\n   BUSINESS COST ANALİZİ:")
print(f"      • Mevcut: ${baseline_cost:,} → Optimized: ${best_recall_row['Total_Cost']:,.0f} ({'+' if cost_diff > 0 else ''}{cost_diff:,.0f})")
print(f"\n   TRADE-OFF:")
print(f"      • False Positive artışı: {fp_base} → {int(best_recall_row['FP'])} (+{int(best_recall_row['FP']) - fp_base})")
print(f"      • Ek kampanya maliyeti: ${(int(best_recall_row['FP']) - fp_base) * 50:,}")
print(f"      • FN azalma tasarrufu: ${fn_reduction * 3000:,} (LTV kurtarma)")
print(f"      • Net etki: {'+' if cost_diff > 0 else ''}${abs(cost_diff):,.0f}")

print(f"\n💰 ALTERNATİF STRATEJI 2: EN DÜŞÜK BUSINESS COST")
print(f"   Threshold: {best_cost_row['Threshold']:.2f}")
print(f"   Churn Recall: {best_cost_row['Recall_Churn']:.4f}")
print(f"   FN: {int(best_cost_row['FN'])}, FP: {int(best_cost_row['FP'])}")
print(f"   Cost: ${best_cost_row['Total_Cost']:,.0f} (${cost_saving:,.0f} tasarruf)")

print("\n💡 UYGULAMA ÖNERİSİ:")
print(f"   Model prediction'ı değiştirin:")
print(f"   ```python")
print(f"   y_pred_proba = model.predict_proba(X_test)[:, 1]")
print(f"   ")
print(f"   # Strateji 1: Max Churn Recall (Business Kritik)")
print(f"   y_pred_max_recall = (y_pred_proba >= {best_recall_row['Threshold']:.2f}).astype(int)")
print(f"   ")
print(f"   # Strateji 2: Min Cost (Maliyet Optimize)")
print(f"   y_pred_min_cost = (y_pred_proba >= {best_cost_row['Threshold']:.2f}).astype(int)")
print(f"   ```")

print("\n✅ RECALL OPTİMİZASYONU TAMAMLANDI")
print("="*80)
