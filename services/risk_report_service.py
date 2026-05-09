from database import get_db

# PARAMETRELER
PM10_LIMIT = 50
SO2_LIMIT = 20
CO_LIMIT = 4
O3_LIMIT = 100


def calculate_risk_score(
    pm10_avg,
    so2_avg,
    co_avg,
    o3_avg,
    diseases
):

    score = 0
    messages = []

    # ---------------- PM10 ----------------
    if pm10_avg > PM10_LIMIT:

        score += 25

        messages.append(
            "PM10 seviyesi yüksek"
        )

        if "Astım" in diseases:
            score += 20
            messages.append(
                "Astım hastaları için risk artışı"
            )

        if "KOAH" in diseases:
            score += 20
            messages.append(
                "KOAH hastaları için solunum riski"
            )

        if "65 Yaş Üstü" in diseases:
            score += 10
            messages.append(
                "Yaşlı bireyler dikkat etmeli"
            )

    # ---------------- SO2 ----------------
    if so2_avg > SO2_LIMIT:

        score += 20

        messages.append(
            "SO2 seviyesi yüksek"
        )

        if "Astım" in diseases:
            score += 15
            messages.append(
                "SO2 astımı tetikleyebilir"
            )

        if "Kronik Bronşit" in diseases:
            score += 15
            messages.append(
                "Bronşit için riskli hava"
            )

    # ---------------- CO ----------------
    if co_avg > CO_LIMIT:

        score += 20

        messages.append(
            "CO seviyesi yüksek"
        )

        if "Kalp Hastalığı" in diseases:
            score += 25
            messages.append(
                "Kalp hastaları için ciddi risk"
            )

        if "Hipertansiyon" in diseases:
            score += 15
            messages.append(
                "Hipertansiyon etkilenebilir"
            )

    # ---------------- O3 ----------------
    if o3_avg > O3_LIMIT:

        score += 20

        messages.append(
            "Ozon seviyesi yüksek"
        )

        if "Alerjik Rinit" in diseases:
            score += 15
            messages.append(
                "Alerjik bireylerde şikayet artabilir"
            )

        if "Akciğer Fibrozu" in diseases:
            score += 20
            messages.append(
                "Akciğer hastaları dikkat etmeli"
            )

    # ---------------- EXTRA ----------------
    if "Sigara Kullanımı" in diseases:
        score += 10
        messages.append(
            "Sigara kullanımı hava riskini artırır"
        )

    if "Gebelik" in diseases:
        score += 10
        messages.append(
            "Hamile bireyler dikkat etmeli"
        )

    if "Bağışıklık Sistemi Zayıf" in diseases:
        score += 10
        messages.append(
            "Bağışıklığı düşük bireylerde hassasiyet artabilir"
        )

    # ---------------- RISK LEVEL ----------------
    if score < 30:
        level = "Düşük Risk"

    elif score < 60:
        level = "Orta Risk"

    else:
        level = "Yüksek Risk"

    return {
        "risk_score": score,
        "risk_level": level,
        "messages": messages
    }


def generate_risk_report(
    station_name,
    diseases
):

    with get_db() as db:

        db.execute("""
            SELECT
                p.isim,
                AVG(g.tahmin)
            FROM gunluk_tahmin_catboost g
            JOIN istasyonlar i
                ON i.id = g.istasyon_id
            JOIN parametreler p
                ON p.id = g.parametre_id
            WHERE i.isim = %s
            GROUP BY p.isim
        """, (station_name,))

        rows = db.fetchall()

    averages = {
        "PM10": 0,
        "SO2": 0,
        "CO": 0,
        "O3": 0,
    }

    for r in rows:

        param_name = r[0]
        avg_value = float(r[1])

        averages[param_name] = round(
            avg_value,
            2
        )

    risk = calculate_risk_score(
        averages["PM10"],
        averages["SO2"],
        averages["CO"],
        averages["O3"],
        diseases
    )

    return {

        "station": station_name,

        "averages": averages,

        "risk_score": risk["risk_score"],

        "risk_level": risk["risk_level"],

        "messages": risk["messages"]

    }