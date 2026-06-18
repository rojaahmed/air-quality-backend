# services/manual_test_service.py

# ==========================================================
# WHO LIMITS
# ==========================================================

WHO_LIMITS = {
    "PM10": 45,
    "SO2": 40,
    "CO": 10,
    "O3": 100
}

# ==========================================================
# EPA AQI BREAKPOINTS
# ==========================================================

PM10_BREAKPOINTS = [
    (0, 54, 0, 50),
    (55, 154, 51, 100),
    (155, 254, 101, 150),
    (255, 354, 151, 200),
    (355, 424, 201, 300),
]

SO2_BREAKPOINTS = [
    (0, 35, 0, 50),
    (36, 75, 51, 100),
    (76, 185, 101, 150),
    (186, 304, 151, 200),
    (305, 604, 201, 300),
]

CO_BREAKPOINTS = [
    (0, 4.4, 0, 50),
    (4.5, 9.4, 51, 100),
    (9.5, 12.4, 101, 150),
    (12.5, 15.4, 151, 200),
    (15.5, 30.4, 201, 300),
]

O3_BREAKPOINTS = [
    (0, 54, 0, 50),
    (55, 70, 51, 100),
    (71, 85, 101, 150),
    (86, 105, 151, 200),
    (106, 200, 201, 300),
]

# ==========================================================
# HASTALIK AĞIRLIKLARI
# ==========================================================

ASTIM = {
    "PM10": 3,
    "SO2": 3,
    "CO": 1,
    "O3": 2
}

KOAH = {
    "PM10": 3,
    "SO2": 2,
    "CO": 2,
    "O3": 2
}

KALP = {
    "PM10": 2,
    "SO2": 1,
    "CO": 3,
    "O3": 1
}

HIPERTANSIYON = {
    "PM10": 1,
    "SO2": 1,
    "CO": 3,
    "O3": 1
}

DIYABET = {
    "PM10": 2,
    "SO2": 1,
    "CO": 1,
    "O3": 1
}

FIBROZ = {
    "PM10": 3,
    "SO2": 3,
    "CO": 1,
    "O3": 2
}

RINIT = {
    "PM10": 3,
    "SO2": 1,
    "CO": 0,
    "O3": 1
}

GEBELIK = {
    "PM10": 2,
    "SO2": 1,
    "CO": 2,
    "O3": 1
}

SIGARA = {
    "PM10": 2,
    "SO2": 2,
    "CO": 3,
    "O3": 1
}

YAS65 = {
    "PM10": 2,
    "SO2": 2,
    "CO": 2,
    "O3": 1
}

# ==========================================================
# HASTALIK SÖZLÜĞÜ
# ==========================================================

DISEASE_WEIGHTS = {

    "Astım": ASTIM,
    "KOAH": KOAH,
    "Alerjik Rinit": RINIT,
    "Kronik Bronşit": KOAH,
    "Akciğer Fibrozu": FIBROZ,
    "Kalp Hastalığı": KALP,
    "Hipertansiyon": HIPERTANSIYON,
    "Diyabet": DIYABET,
    "Bağışıklık Sistemi Zayıf": ASTIM,
    "Gebelik": GEBELIK,
    "Sigara Kullanımı": SIGARA,
    "65 Yaş Üstü": YAS65,

    "Yok": {
        "PM10": 1,
        "SO2": 1,
        "CO": 1,
        "O3": 1
    },
    "Diğer": {
    "PM10": 1,
    "SO2": 1,
    "CO": 1,
    "O3": 1
},
}

# ==========================================================
# HASTALIĞA ÖZEL ÖNERİLER
# ==========================================================

DISEASE_RECOMMENDATIONS = {

    "Astım": [
        "Maske kullanın",
        "İnhalerinizi yanınızda taşıyın",
        "Açık hava sporlarından kaçının"
    ],

    "KOAH": [
        "Uzun süre dışarıda kalmayın",
        "Nefes egzersizleri yapın",
        "Doktor ilaçlarını aksatmayın"
    ],

    "Kalp Hastalığı": [
        "Yoğun fiziksel aktiviteden kaçının",
        "Bol su tüketin",
        "Stresten uzak durun"
    ],

    "Gebelik": [
        "Kalabalık bölgelerden kaçının",
        "Maske kullanın",
        "Kapalı ortam hava temizleyicisi tercih edin"
    ],
    "Hipertansiyon": [
    "Tuz tüketimini azaltın",
    "Bol su tüketin",
    "Aşırı efordan kaçının"
],
"Diyabet": [
    "Kan şekerinizi düzenli takip edin",
    "Bol sıvı tüketin",
    "Uzun süre kirli havada kalmayın"
],
"Alerjik Rinit": [
    "Maske kullanın",
    "Polenli bölgelerden uzak durun",
    "Eve gelince yüzünüzü yıkayın"
],
"Akciğer Fibrozu": [
    "Nefes egzersizleri yapın",
    "Kirli havada uzun süre kalmayın",
    "Doktor kontrollerinizi aksatmayın"
],
"Sigara Kullanımı": [
    "Sigara tüketimini azaltın",
    "Maske kullanın",
    "Açık havada egzersizden kaçının"
],
"65 Yaş Üstü": [
    "Uzun süre dışarıda kalmayın",
    "Bol su tüketin",
    "Maske kullanın"
]

}

# ==========================================================
# AQI HESABI
# ==========================================================

def calculate_aqi(C, breakpoints):

    for Clow, Chigh, Ilow, Ihigh in breakpoints:

        if Clow <= C <= Chigh:

            return round(
                ((Ihigh - Ilow) / (Chigh - Clow))
                * (C - Clow)
                + Ilow
            )

    return 500


# ==========================================================
# ANA FONKSİYON
# ==========================================================

def analyze_manual_test(
        pm10,
        so2,
        co,
        o3,
        exposure_hours,
        disease
):

    # ---------------- AQI ----------------

    pm10_aqi = calculate_aqi(pm10, PM10_BREAKPOINTS)
    so2_aqi = calculate_aqi(so2, SO2_BREAKPOINTS)
    co_aqi = calculate_aqi(co, CO_BREAKPOINTS)
    o3_aqi = calculate_aqi(o3, O3_BREAKPOINTS)

    aqi = max(
        pm10_aqi,
        so2_aqi,
        co_aqi,
        o3_aqi
    )

    # ---------------- AQI CATEGORY ----------------

    if aqi <= 50:
        category = "İyi"

    elif aqi <= 100:
        category = "Orta"

    elif aqi <= 150:
        category = "Hassas Gruplar"

    elif aqi <= 200:
        category = "Sağlıksız"

    else:
        category = "Çok Sağlıksız"

    # ---------------- WEIGHTS ----------------

    weights = DISEASE_WEIGHTS.get(
        disease,
        DISEASE_WEIGHTS["Yok"]
    )

    # ---------------- EXPOSURE FACTOR ----------------

    if exposure_hours < 6:
        exposure_factor = 1

    elif exposure_hours < 12:
        exposure_factor = 1.2

    elif exposure_hours < 24:
        exposure_factor = 1.5

    else:
        exposure_factor = 2

    # ---------------- RISK SCORE ----------------

    risk_score = (
    pm10_aqi * weights["PM10"]
    + so2_aqi * weights["SO2"]
    + co_aqi * weights["CO"]
    + o3_aqi * weights["O3"]
)

    risk_score *= exposure_factor

    risk_percent = min(
        100,
        round(risk_score / 10)
    )

    # ---------------- ALARM LEVEL ----------------

    if risk_percent < 30:
        risk_level = "Hafif"

    elif risk_percent < 70:
        risk_level = "Orta"

    else:
        risk_level = "Ağır"

    # ---------------- DOMINANT POLLUTANT ----------------

    aqi_values = {
     "PM10": pm10_aqi,
     "SO2": so2_aqi,
     "CO": co_aqi,
     "O3": o3_aqi
    }

    dominant_pollutant = max(
      aqi_values,
      key=aqi_values.get
    )

    # ---------------- WARNINGS ----------------

    warnings = []

    if disease == "Astım":

        if pm10 > WHO_LIMITS["PM10"]:
            warnings.append(
                "PM10 seviyesi astım hastaları için ciddi risk oluşturuyor."
            )

        if so2 > WHO_LIMITS["SO2"]:
            warnings.append(
                "SO2 bronş daralmasına neden olabilir."
            )

        if o3 > WHO_LIMITS["O3"]:
            warnings.append(
                "Ozon maruziyeti nefes darlığını artırabilir."
            )

    elif disease == "KOAH":

        if pm10 > WHO_LIMITS["PM10"]:
            warnings.append(
                "PM10 KOAH hastalarında nefes darlığını artırabilir."
            )

        if so2 > WHO_LIMITS["SO2"]:
            warnings.append(
                "SO2 akciğer fonksiyonlarını olumsuz etkileyebilir."
            )

    elif disease == "Kalp Hastalığı":

        if co > WHO_LIMITS["CO"]:
            warnings.append(
                "CO seviyesi kalp hastaları için risk oluşturuyor."
            )

    if len(warnings) == 0:
      warnings.append(
        "WHO limitleri içerisinde ciddi bir sağlık riski tespit edilmedi."
    )
    # ---------------- RECOMMENDATIONS ----------------

    recommendations = DISEASE_RECOMMENDATIONS.get(
        disease,
        [
            "Maske kullanın",
            "Uzun süre dışarıda kalmayın",
            "Bol su tüketin"
        ]
    )

    # ---------------- RETURN ----------------

    return {

        "aqi": aqi,

        "category": category,

        "risk_percent": risk_percent,

        "risk_level": risk_level,

        "dominant_pollutant": dominant_pollutant,
        "pm10": pm10,
        "so2": so2,
        "co": co,
        "o3": o3,

        "pm10_aqi": pm10_aqi,
        "so2_aqi": so2_aqi,
        "co_aqi": co_aqi,
        "o3_aqi": o3_aqi,

        "warnings": warnings,

        "recommendations": recommendations
    }