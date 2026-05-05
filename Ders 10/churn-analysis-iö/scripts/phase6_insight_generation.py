# ================================================================
# PHASE 6: INSIGHT GENERATION
# ================================================================
# Teknik sonuçları anlamlı içgörülere dönüştürmek

import os
import warnings
from pathlib import Path
import pandas as pd
import numpy as np

warnings.filterwarnings("ignore")

print("=" * 70)
print("PHASE 6: INSIGHT GENERATION")
print("=" * 70)
print()

# Önceki analizlerden elde edilen önemli bulguları özetleyelim

print("=" * 70)
print("A. KRİTİK TEKNİK BULGULAR ÖZETİ")
print("=" * 70)
print()

critical_findings = [
    {
        "Bulgu": "Hedef Değişken Dağılımı",
        "Kanıt": "Churn=No: %73.46, Churn=Yes: %26.54",
        "Teknik Yorum": "Hedef değişken makul dengede, ciddi imbalance yok",
        "İş Değeri": "Müşteri kaybı oranı %26.54 - iş açısından kritik bir oran",
        "Modelleme Etkisi": "Hafif dengesizlik var ama SMOTE gerekli değil. Stratified split yeterli olabilir."
    },
    {
        "Bulgu": "tenure - Churn İlişkisi",
        "Kanıt": "Churn=Yes ortalama 17.98 ay, Churn=No ortalama 37.57 ay (p<0.0001)",
        "Teknik Yorum": "En güçlü prediktör. Yeni müşteriler çok daha fazla churn ediyor.",
        "İş Değeri": "İlk 18 ay kritik dönem. Müşteri sadakati programları bu döneme odaklanmalı.",
        "Modelleme Etkisi": "Tenure modelin en önemli değişkenlerinden biri olacak."
    },
    {
        "Bulgu": "Contract - Churn İlişkisi",
        "Kanıt": "Month-to-month: %42.71 churn, One year: %11.27 churn, Two year: %2.83 churn",
        "Teknik Yorum": "En yüksek churn oranına sahip kategorik değişken",
        "İş Değeri": "Uzun vadeli sözleşmeler churn'ü dramatik şekilde azaltıyor. Stratejik aksiyon noktası.",
        "Modelleme Etkisi": "Contract modelin en kritik kategorik değişkeni olacak."
    },
    {
        "Bulgu": "InternetService - Churn İlişkisi",
        "Kanıt": "Fiber optic: %41.89 churn, DSL: %18.96 churn, No: %7.40 churn",
        "Teknik Yorum": "Fiber optic müşterileri beklenmedik şekilde yüksek churn gösteriyor",
        "İş Değeri": "Fiber optic hizmet kalitesi, fiyatlandırma veya rekabet analizi gerekli",
        "Modelleme Etkisi": "InternetService güçlü bir prediktör olacak."
    },
    {
        "Bulgu": "MonthlyCharges - Churn İlişkisi",
        "Kanıt": "Churn=Yes ortalama $74.44, Churn=No ortalama $61.27 (p<0.0001)",
        "Teknik Yorum": "Yüksek ücretlendirme churn riskini artırıyor",
        "İş Değeri": "Fiyatlandırma stratejisi gözden geçirilmeli. Premium müşteriler churn ediyor.",
        "Modelleme Etkisi": "MonthlyCharges sayısal değişkenler arasında güçlü prediktör."
    },
    {
        "Bulgu": "TotalCharges ve tenure Korelasyonu",
        "Kanıt": "Korelasyon: 0.8259, TotalCharges VIF: 8.08",
        "Teknik Yorum": "Yüksek multicollinearity. TotalCharges = tenure × MonthlyCharges ilişkisi",
        "İş Değeri": "TotalCharges türetilmiş bir değişken, bağımsız bilgi taşımıyor",
        "Modelleme Etkisi": "TotalCharges modelden çıkarılmalı veya tenure yerine kullanılmalı (leakage riski)."
    },
    {
        "Bulgu": "PaymentMethod - Churn İlişkisi",
        "Kanıt": "Electronic check: %45.29 churn, Automatic methods: ~%16 churn",
        "Teknik Yorum": "Manual payment method yüksek churn ile ilişkili",
        "İş Değeri": "Otomatik ödeme yöntemlerine geçiş teşviki churn'ü azaltabilir",
        "Modelleme Etkisi": "PaymentMethod kategorik encoding ile güçlü bir feature olacak."
    },
    {
        "Bulgu": "OnlineSecurity/TechSupport - Churn İlişkisi",
        "Kanıt": "OnlineSecurity=No: %41.77 churn, TechSupport=No: %41.64 churn",
        "Teknik Yorum": "Ek hizmetler müşteri bağlılığını artırıyor",
        "İş Değeri": "Value-added services churn'ü azaltmanın etkili yolu",
        "Modelleme Etkisi": "Bu değişkenler güçlü negatif churn göstergeleri."
    },
    {
        "Bulgu": "Partner/Dependents - Churn İlişkisi",
        "Kanıt": "Partner=No: %32.96 churn, Dependents=No: %31.28 churn",
        "Teknik Yorum": "Aile yapısı churn'ü etkiliyor",
        "İş Değeri": "Bekar/dependents olmayan müşteriler daha az bağlı",
        "Modelleme Etkisi": "Demografik değişkenler orta düzey prediktörler."
    },
    {
        "Bulgu": "Veri Kalitesi",
        "Kanıt": "Sadece TotalCharges'da 11 eksik değer (%0.16), duplicate yok",
        "Teknik Yorum": "Genel veri kalitesi çok yüksek",
        "İş Değeri": "Temiz veri seti, hızlı modelleme mümkün",
        "Modelleme Etkisi": "Minimal preprocessing gerekli, odak feature engineering ve model selection'da olmalı."
    }
]

findings_df = pd.DataFrame(critical_findings)
findings_df.to_csv('../reports/csv/phase6_critical_findings.csv', index=False, encoding='utf-8-sig')

print("Top 10 Kritik Teknik Bulgu:")
for i, finding in enumerate(critical_findings, 1):
    print(f"\n{i}. {finding['Bulgu']}")
    print(f"   📊 Kanıt: {finding['Kanıt']}")
    print(f"   🔍 Teknik: {finding['Teknik Yorum']}")
    print(f"   💼 İş Değeri: {finding['İş Değeri']}")
    print(f"   🤖 Modelleme: {finding['Modelleme Etkisi']}")

print()
print(f"📄 Kritik bulgular raporu kaydedildi: ../reports/csv/phase6_critical_findings.csv")
print()

print("=" * 70)
print("B. İŞ DEĞERİ YÜKSEK 5 İÇGÖRÜ")
print("=" * 70)
print()

business_insights = [
    {
        "İçgörü": "İlk 18 Ay Kritik Risk Dönemi",
        "Açıklama": "Churn eden müşterilerin ortalama tenure'u 18 ay, kalanların 38 ay. İlk 18 ay müşteri kazanma maliyetini karşılamadan kaybediliyor.",
        "Aksiyon Önerisi": "Onboarding programı, ilk 6-12 ay özel destek, sadakat programı erken başlatılmalı",
        "Beklenen Etki": "İlk 18 aydaki churn %10 azalırsa, LTV önemli ölçüde artacak"
    },
    {
        "İçgörü": "Fiber Optic Müşteri Memnuniyetsizliği",
        "Açıklama": "Fiber optic müşterileri en yüksek churn oranına sahip (%41.89). DSL müşterileri (%18.96) çok daha düşük churn gösteriyor.",
        "Aksiyon Önerisi": "Fiber optic hizmet kalitesi, hız beklentisi, teknik destek ve fiyatlandırma araştırılmalı",
        "Beklenen Etki": "Fiber optic churn %10 puan azalırsa, yıllık ~300 müşteri kaybı önlenebilir"
    },
    {
        "İçgörü": "Uzun Vadeli Sözleşme = Düşük Churn",
        "Açıklama": "Two year sözleşmelerde churn %2.83, month-to-month'da %42.71. 15 kat fark var.",
        "Aksiyon Önerisi": "Uzun vadeli sözleşmeye geçiş teşvikleri (indirim, ek hizmet, özel avantajlar)",
        "Beklenen Etki": "Month-to-month müşterilerin %20'si 1-2 yıllık sözleşmeye geçerse, genel churn %5-7 azalabilir"
    },
    {
        "İçgörü": "Otomatik Ödeme Yöntemi Bağlılık Göstergesi",
        "Açıklama": "Electronic check kullananlar %45.29 churn, otomatik ödeme yapanlar ~%16 churn. Otomatik ödeme bağlılık ve kolaylık sağlıyor.",
        "Aksiyon Önerisi": "Otomatik ödeme kurulumu için incentive, setup kolaylığı, güvenlik vurgusu",
        "Beklenen Etki": "Electronic check müşterilerinin %30'u otomatik ödemeye geçerse, ~150 müşteri kaybı önlenebilir"
    },
    {
        "İçgörü": "Value-Added Services Müşteri Tutma Aracı",
        "Açıklama": "OnlineSecurity, TechSupport, DeviceProtection gibi ek hizmetler churn'ü %20-25 puan azaltıyor.",
        "Aksiyon Önerisi": "Cross-sell kampanyaları, bundle paketler, ilk ay ücretsiz deneme",
        "Beklenen Etki": "Ek hizmet penetrasyonu %10 artarsa, genel churn %2-3 puan azalabilir"
    }
]

insights_df = pd.DataFrame(business_insights)
insights_df.to_csv('../reports/csv/phase6_business_insights.csv', index=False, encoding='utf-8-sig')

print("Top 5 İş Değeri Yüksek İçgörü:")
for i, insight in enumerate(business_insights, 1):
    print(f"\n{i}. {insight['İçgörü']}")
    print(f"   📝 Açıklama: {insight['Açıklama']}")
    print(f"   🎯 Aksiyon: {insight['Aksiyon Önerisi']}")
    print(f"   📈 Beklenen Etki: {insight['Beklenen Etki']}")

print()
print(f"📄 İş değeri içgörüleri kaydedildi: ../reports/csv/phase6_business_insights.csv")
print()

print("=" * 70)
print("C. MODELLEME İÇİN KRİTİK 5 DEĞİŞKEN")
print("=" * 70)
print()

critical_variables = [
    {
        "Değişken": "tenure",
        "Tip": "Sayısal",
        "Önem Seviyesi": "Çok Yüksek",
        "Sebep": "En güçlü prediktör. Churn/No-Churn arasında 2x fark var (18 vs 38 ay)",
        "Preprocessing İhtiyacı": "Scaling gerekli (StandardScaler veya MinMaxScaler)"
    },
    {
        "Değişken": "Contract",
        "Tip": "Kategorik",
        "Önem Seviyesi": "Çok Yüksek",
        "Sebep": "En yüksek Chi-Square değeri (1184). Month-to-month %42.71 churn, Two year %2.83 churn",
        "Preprocessing İhtiyacı": "One-Hot Encoding veya Ordinal Encoding (mantıksal sıra var: month<year<two year)"
    },
    {
        "Değişken": "InternetService",
        "Tip": "Kategorik",
        "Önem Seviyesi": "Çok Yüksek",
        "Sebep": "Fiber optic %41.89 churn, DSL %18.96 churn. Güçlü discriminative power",
        "Preprocessing İhtiyacı": "One-Hot Encoding"
    },
    {
        "Değişken": "MonthlyCharges",
        "Tip": "Sayısal",
        "Önem Seviyesi": "Yüksek",
        "Sebep": "Churn eden müşteriler $13 daha fazla ödüyor ($74.44 vs $61.27)",
        "Preprocessing İhtiyacı": "Scaling gerekli, outlier yok"
    },
    {
        "Değişken": "PaymentMethod",
        "Tip": "Kategorik",
        "Önem Seviyesi": "Yüksek",
        "Sebep": "Electronic check %45.29 churn, automatic methods ~%16 churn. 3x fark",
        "Preprocessing İhtiyacı": "One-Hot Encoding veya Binary Encoding (automatic vs manual)"
    }
]

variables_df = pd.DataFrame(critical_variables)
variables_df.to_csv('../reports/csv/phase6_critical_variables.csv', index=False, encoding='utf-8-sig')

print("Top 5 Kritik Modelleme Değişkeni:")
for i, var in enumerate(critical_variables, 1):
    print(f"\n{i}. {var['Değişken']} ({var['Tip']})")
    print(f"   ⭐ Önem: {var['Önem Seviyesi']}")
    print(f"   📊 Sebep: {var['Sebep']}")
    print(f"   🔧 Preprocessing: {var['Preprocessing İhtiyacı']}")

print()
print(f"📄 Kritik değişkenler raporu kaydedildi: ../reports/csv/phase6_critical_variables.csv")
print()

print("=" * 70)
print("D. DATA PREP EXPERT İÇİN FİNAL ÖNERİLER")
print("=" * 70)
print()

final_recommendations = [
    {
        "Öncelik": "Kritik",
        "Alan": "Feature Engineering",
        "Öneri": "TotalCharges değişkenini modelden çıkar (tenure ve MonthlyCharges ile yüksek korelasyon, leakage riski)",
        "Gerekçe": "Korelasyon 0.8259, VIF 8.08. Bağımsız bilgi taşımıyor."
    },
    {
        "Öncelik": "Kritik",
        "Alan": "Encoding Strategy",
        "Öneri": "Contract için Ordinal Encoding kullan (month-to-month=0, one year=1, two year=2)",
        "Gerekçe": "Mantıksal sıra var ve churn ile doğrusal ilişki var. One-hot yerine ordinal daha efficient."
    },
    {
        "Öncelik": "Yüksek",
        "Alan": "Scaling",
        "Öneri": "tenure, MonthlyCharges için StandardScaler veya MinMaxScaler uygula",
        "Gerekçe": "Farklı ölçeklerde değişkenler var. Tree-based modeller hariç gerekli."
    },
    {
        "Öncelik": "Yüksek",
        "Alan": "Imbalance Handling",
        "Öneri": "Stratified train-test split yeterli. SMOTE gerekli değil.",
        "Gerekçe": "Churn oranı %26.54 - makul dengede. Aggressive sampling model bias yaratabilir."
    },
    {
        "Öncelik": "Orta",
        "Alan": "Missing Values",
        "Öneri": "TotalCharges eksik değerlerini (11 adet) tenure × MonthlyCharges ile doldur",
        "Gerekçe": "Mantıksal ilişki var ve eksik değer sayısı çok düşük (%0.16)"
    },
    {
        "Öncelik": "Orta",
        "Alan": "Feature Creation",
        "Öneri": "tenure_group kategorik değişkeni oluştur (0-12 ay: new, 13-24: medium, 25+: loyal)",
        "Gerekçe": "Non-linear pattern yakalama için threshold-based segmentation faydalı olabilir"
    },
    {
        "Öncelik": "Orta",
        "Alan": "Categorical Grouping",
        "Öneri": "InternetService ile OnlineSecurity/TechSupport interaction feature oluştur",
        "Gerekçe": "Fiber optic + No Security kombinasyonu en yüksek churn riski taşıyor"
    },
    {
        "Öncelik": "Düşük",
        "Alan": "Feature Selection",
        "Öneri": "gender ve PhoneService değişkenleri modelden çıkarılabilir (p-value > 0.05)",
        "Gerekçe": "Churn ile istatistiksel anlamlı ilişki yok. Model simplicity için çıkarma düşünülebilir"
    }
]

recommendations_df = pd.DataFrame(final_recommendations)
recommendations_df.to_csv('../reports/csv/phase6_final_recommendations.csv', index=False, encoding='utf-8-sig')

print("Data Prep Expert için Final Öneriler:")
for i, rec in enumerate(final_recommendations, 1):
    print(f"\n{i}. [{rec['Öncelik']}] {rec['Alan']}")
    print(f"   💡 Öneri: {rec['Öneri']}")
    print(f"   📌 Gerekçe: {rec['Gerekçe']}")

print()
print(f"📄 Final öneriler raporu kaydedildi: ../reports/csv/phase6_final_recommendations.csv")
print()

print("=" * 70)
print("✅ PHASE 6 TAMAMLANDI")
print("=" * 70)
