# ================================================================
# PHASE 7: MODEL READINESS ASSESSMENT
# ================================================================
# Verinin modelleme aşamasına hazır olup olmadığını değerlendirmek

import os
import warnings
from pathlib import Path
import pandas as pd

warnings.filterwarnings("ignore")

print("=" * 70)
print("PHASE 7: MODEL READINESS ASSESSMENT")
print("=" * 70)
print()

print("=" * 70)
print("A. VERİ HAZIRLIĞI DEĞERLENDİRMESİ")
print("=" * 70)
print()

assessment_criteria = [
    {
        "Kriter": "Eksik Veri Yönetimi",
        "Durum": "✅ Hazır",
        "Açıklama": "Sadece TotalCharges'da 11 eksik değer var (%0.16). Çok düşük oran.",
        "Aksiyon": "TotalCharges'ı modelden çıkar (multicollinearity) veya tenure × MonthlyCharges ile doldur."
    },
    {
        "Kriter": "Encoding Gereksinimi",
        "Durum": "⚠️ Gerekli",
        "Açıklama": "15 kategorik değişken var. gender, Partner, Contract, InternetService vb.",
        "Aksiyon": "One-Hot Encoding veya Ordinal Encoding (Contract için) uygulanmalı."
    },
    {
        "Kriter": "Scaling Gereksinimi",
        "Durum": "⚠️ Gerekli",
        "Açıklama": "tenure (0-72), MonthlyCharges ($18-118) farklı ölçeklerde.",
        "Aksiyon": "StandardScaler veya MinMaxScaler uygulanmalı (tree-based modeller hariç)."
    },
    {
        "Kriter": "Outlier Yönetimi",
        "Durum": "✅ Hazır",
        "Açıklama": "SeniorCitizen hariç outlier sorunu yok. SeniorCitizen binary değişken.",
        "Aksiyon": "Outlier handling gerekli değil."
    },
    {
        "Kriter": "Target Imbalance",
        "Durum": "✅ Hazır",
        "Açıklama": "Churn=No: %73.46, Churn=Yes: %26.54. Makul dengede.",
        "Aksiyon": "Stratified split yeterli. SMOTE/ADASYN gerekli değil."
    },
    {
        "Kriter": "Leakage Riski",
        "Durum": "⚠️ Dikkat",
        "Açıklama": "TotalCharges = tenure × MonthlyCharges ilişkisi var. Leakage riski yüksek.",
        "Aksiyon": "TotalCharges kesinlikle modelden çıkarılmalı."
    },
    {
        "Kriter": "Train-Test Split Stratejisi",
        "Durum": "⚠️ Planlama Gerekli",
        "Açıklama": "7043 satır var. Stratified split uygulanmalı.",
        "Aksiyon": "80-20 veya 70-30 split, stratify=y (Churn) ile yapılmalı."
    },
    {
        "Kriter": "Feature Selection İhtiyacı",
        "Durum": "⚠️ Opsiyonel",
        "Açıklama": "gender ve PhoneService churn ile anlamlı ilişkiye sahip değil (p>0.05).",
        "Aksiyon": "Model simplicity için bu değişkenler çıkarılabilir veya korunabilir."
    },
    {
        "Kriter": "Multicollinearity",
        "Durum": "⚠️ Dikkat",
        "Açıklama": "tenure ve TotalCharges korelasyonu 0.8259. VIF: 8.08 ve 6.32.",
        "Aksiyon": "TotalCharges çıkarılmalı veya regularization (Ridge/Lasso) kullanılmalı."
    },
    {
        "Kriter": "Veri Kalitesi",
        "Durum": "✅ Çok İyi",
        "Açıklama": "Duplicate yok, negatif değer yok, tutarlılık sorunları yok.",
        "Aksiyon": "Veri kalitesi açısından ek işlem gerekli değil."
    }
]

assessment_df = pd.DataFrame(assessment_criteria)
assessment_df.to_csv('../reports/csv/phase7_model_readiness_assessment.csv', index=False, encoding='utf-8-sig')

print("Model Readiness Değerlendirmesi:")
for i, criterion in enumerate(assessment_criteria, 1):
    print(f"\n{i}. {criterion['Kriter']}")
    print(f"   Durum: {criterion['Durum']}")
    print(f"   📝 {criterion['Açıklama']}")
    print(f"   🎯 Aksiyon: {criterion['Aksiyon']}")

print()
print(f"📄 Model hazırlık değerlendirmesi kaydedildi: ../reports/csv/phase7_model_readiness_assessment.csv")
print()

print("=" * 70)
print("B. MODEL HAZIRLIK KARARI")
print("=" * 70)
print()

# Hazırlık skorlaması
ready_count = sum(1 for c in assessment_criteria if "✅" in c["Durum"])
needs_action_count = sum(1 for c in assessment_criteria if "⚠️" in c["Durum"])
total_count = len(assessment_criteria)

readiness_score = (ready_count / total_count) * 100

print(f"📊 Hazırlık Skoru: %{readiness_score:.1f}")
print(f"   ✅ Hazır Kriterler: {ready_count}/{total_count}")
print(f"   ⚠️  Aksiyon Gerektiren Kriterler: {needs_action_count}/{total_count}")
print()

# Karar
if readiness_score >= 80:
    readiness_status = "Hazır"
    color = "🟢"
elif readiness_score >= 50:
    readiness_status = "Kısmen Hazır"
    color = "🟡"
else:
    readiness_status = "Hazır Değil"
    color = "🔴"

print("=" * 70)
print(f"{color} MODEL HAZIRLİK KARARI: {readiness_status.upper()}")
print("=" * 70)
print()

if readiness_status == "Hazır":
    print("✅ Veri seti modelleme için HAZIR.")
    print()
    print("Gerekçe:")
    print("  • Veri kalitesi çok yüksek (eksik veri minimal, duplicate yok)")
    print("  • Target imbalance makul seviyede")
    print("  • Outlier sorunu yok")
    print("  • Güçlü prediktörler tespit edildi (tenure, Contract, InternetService)")
    print()
    print("⚠️  Ancak modelleme öncesi şu adımlar atılmalı:")
    print("  1. TotalCharges değişkenini modelden çıkar (leakage ve multicollinearity)")
    print("  2. Kategorik değişkenlere encoding uygula (One-Hot veya Ordinal)")
    print("  3. Sayısal değişkenlere scaling uygula (StandardScaler)")
    print("  4. Stratified train-test split yap (80-20 veya 70-30)")
    print()

elif readiness_status == "Kısmen Hazır":
    print("🟡 Veri seti KISMEN HAZIR.")
    print()
    print("Gerekçe:")
    print("  • Bazı preprocessing adımları gerekli")
    print("  • Veri kalitesi genel olarak iyi")
    print("  • Kritik riskler tespit edildi (multicollinearity, leakage)")
    print()
    print("⚠️  Modelleme öncesi mutlaka yapılmalı:")
    print("  1. TotalCharges değişkenini modelden çıkar")
    print("  2. Encoding ve scaling uygula")
    print("  3. Feature engineering değerlendir")
    print()

else:
    print("🔴 Veri seti HAZIR DEĞİL.")
    print()
    print("Gerekçe:")
    print("  • Kritik veri kalitesi sorunları var")
    print("  • Preprocessing gereksinimleri fazla")
    print()
    print("⚠️  Data Prep Expert ile çalışmadan modelleme yapılmamalı.")
    print()

print("=" * 70)
print("C. ÖNERİLEN MODELLİNG PIPELINE")
print("=" * 70)
print()

pipeline_steps = [
    {
        "Adım": "1. Data Cleaning",
        "İşlemler": [
            "TotalCharges değişkenini çıkar (leakage + multicollinearity)",
            "customerID değişkenini çıkar (identifier)",
            "Eksik değerler için strateji belirle (11 değer - çıkar veya impute et)"
        ]
    },
    {
        "Adım": "2. Feature Engineering",
        "İşlemler": [
            "tenure_group oluştur (0-12: new, 13-24: medium, 25+: loyal)",
            "MonthlyCharges_category oluştur (low, medium, high)",
            "Interaction features: InternetService × OnlineSecurity"
        ]
    },
    {
        "Adım": "3. Encoding",
        "İşlemler": [
            "Contract için Ordinal Encoding (month-to-month=0, one year=1, two year=2)",
            "Diğer kategorik değişkenler için One-Hot Encoding",
            "Binary değişkenler için Label Encoding (gender, Partner, Dependents vb.)"
        ]
    },
    {
        "Adım": "4. Scaling",
        "İşlemler": [
            "tenure için StandardScaler veya MinMaxScaler",
            "MonthlyCharges için StandardScaler veya MinMaxScaler",
            "Tree-based modeller için scaling opsiyonel"
        ]
    },
    {
        "Adım": "5. Train-Test Split",
        "İşlemler": [
            "80-20 veya 70-30 split",
            "stratify=y (Churn) kullan",
            "random_state=42 (reproducibility için)"
        ]
    },
    {
        "Adım": "6. Model Selection",
        "İşlemler": [
            "Baseline: Logistic Regression",
            "Tree-based: Random Forest, XGBoost, LightGBM",
            "Ensemble: Voting Classifier, Stacking",
            "Karşılaştırma metriği: AUC-ROC, Precision, Recall, F1-Score"
        ]
    },
    {
        "Adım": "7. Hyperparameter Tuning",
        "İşlemler": [
            "GridSearchCV veya RandomizedSearchCV",
            "Cross-validation (5-fold veya 10-fold)",
            "Early stopping (XGBoost/LightGBM için)"
        ]
    },
    {
        "Adım": "8. Model Evaluation",
        "İşlemler": [
            "Confusion Matrix",
            "ROC Curve ve AUC",
            "Precision-Recall Curve",
            "Feature Importance Analysis"
        ]
    }
]

for step in pipeline_steps:
    print(f"{step['Adım']}")
    for i, operation in enumerate(step['İşlemler'], 1):
        print(f"  {i}. {operation}")
    print()

pipeline_df = pd.DataFrame([
    {"Adım": step["Adım"], "İşlem": op} 
    for step in pipeline_steps 
    for op in step["İşlemler"]
])
pipeline_df.to_csv('../reports/csv/phase7_modeling_pipeline.csv', index=False, encoding='utf-8-sig')
print(f"📄 Modelleme pipeline önerisi kaydedildi: ../reports/csv/phase7_modeling_pipeline.csv")
print()

print("=" * 70)
print("D. SONUÇ VE YOL HARİTASI")
print("=" * 70)
print()

print("🎯 SONUÇ:")
print()
print(f"  Veri Seti Durumu: {color} {readiness_status}")
print(f"  Toplam Gözlem: 7,043 satır")
print(f"  Toplam Değişken: 21 (1'i hedef, 1'i identifier)")
print(f"  Modelleme İçin Kullanılabilir: ~19 değişken")
print(f"  Veri Kalitesi: Çok Yüksek")
print(f"  En Güçlü Prediktörler: tenure, Contract, InternetService, MonthlyCharges, PaymentMethod")
print()

print("🗺️ YOL HARİTASI:")
print()
print("  Bir Sonraki Adım: Data Prep Expert")
print()
print("  Data Prep Expert'e İletilecek Bilgiler:")
print("    1. TotalCharges'ı modelden çıkar (kritik)")
print("    2. Contract için Ordinal Encoding uygula")
print("    3. Diğer kategorikler için One-Hot Encoding")
print("    4. tenure ve MonthlyCharges için StandardScaler")
print("    5. Stratified 80-20 split")
print("    6. Feature engineering: tenure_group, interaction features")
print()

print("  Beklenen Çıktı:")
print("    • Temiz, encode edilmiş, scale edilmiş veri seti")
print("    • X_train, X_test, y_train, y_test")
print("    • Feature engineering ile yeni değişkenler")
print("    • Model-ready format")
print()

print("  Sonraki Aşama: Model Expert")
print("    • Baseline model (Logistic Regression)")
print("    • En az 12 model karşılaştırma")
print("    • Hyperparameter tuning")
print("    • Final model selection")
print()

# Final özet kaydet
summary = {
    "Veri Seti": ["churn.csv"],
    "Satır Sayısı": [7043],
    "Sütun Sayısı": [21],
    "Hazırlık Durumu": [readiness_status],
    "Hazırlık Skoru (%)": [readiness_score],
    "Veri Kalitesi": ["Çok Yüksek"],
    "Öncelikli Aksiyon": ["TotalCharges çıkar, Encoding & Scaling uygula"],
    "Bir Sonraki Adım": ["Data Prep Expert"],
    "Tarih": ["2026-05-05"]
}

summary_df = pd.DataFrame(summary)
summary_df.to_csv('../reports/csv/phase7_final_summary.csv', index=False, encoding='utf-8-sig')
print(f"📄 Final özet raporu kaydedildi: ../reports/csv/phase7_final_summary.csv")
print()

print("=" * 70)
print("✅ PHASE 7 TAMAMLANDI")
print("=" * 70)
print()
print("=" * 70)
print("🎉 7 AŞAMALI EDA SÜRECİ BAŞARIYLA TAMAMLANDI!")
print("=" * 70)
