from database import get_db


LIMITS = {
    "PM10": 50,
    "O3": 100,
    "SO2": 75,
    "CO": 9
}


def calculate_risk_level(values):

    score = 0

    for pollutant, value in values.items():

        limit = LIMITS.get(pollutant)

        if limit and value > limit:
            score += 1

    if score == 0:
        return "LOW"

    elif score <= 2:
        return "MODERATE"

    return "HIGH"


def generate_safe_ranges(hour_data):

    safe_hours = []

    for hour, values in hour_data.items():

        safe = True

        for pollutant, value in values.items():

            limit = LIMITS.get(pollutant)

            if limit and value > limit:
                safe = False
                break

        if safe:
            safe_hours.append(hour)

    ranges = []

    if len(safe_hours) == 0:
        return ranges

    start = safe_hours[0]
    previous = safe_hours[0]

    for h in safe_hours[1:]:

        prev_hour = int(previous.split(":")[0])
        current_hour = int(h.split(":")[0])

        if current_hour == prev_hour + 1:

            previous = h

        else:

            ranges.append(f"{start}-{previous}")
            start = h
            previous = h

    ranges.append(f"{start}-{previous}")

    return ranges


def generate_ai_health_report(
        station_id,
        disease,
        user_name
):

    with get_db() as db:

        db.execute("""
            SELECT
                p.isim,
                s.tarih_saat,
                s.tahmin
            FROM saatlik_tahmin_catboost s
            JOIN parametreler p
            ON p.id=s.parametre_id
            WHERE s.istasyon_id=%s
            ORDER BY s.tarih_saat
        """, (station_id,))

        rows = db.fetchall()

    hour_data = {}

    latest_values = {}

    for pollutant, tarih, value in rows:

        hour = tarih.strftime("%H:00")

        if hour not in hour_data:
            hour_data[hour] = {}

        hour_data[hour][pollutant] = float(value)

        latest_values[pollutant] = float(value)

    safe_ranges = generate_safe_ranges(hour_data)

    risk_level = calculate_risk_level(latest_values)

    report = []

    report.append(f"Günaydın {user_name} 🌿")

    if disease.lower() != "yok":

        report.append(
            f"{disease} rahatsızlığınız nedeniyle uzun süre dışarıda kalmanız önerilmez."
        )

    if risk_level == "LOW":

        report.append(
            "Bugünkü hava kalitesi genel olarak güvenlidir."
        )

    elif risk_level == "MODERATE":

        report.append(
            "Hassas bireylerin dikkatli olması önerilir."
        )

    else:

        report.append(
            "Bugün açık hava aktiviteleri sınırlandırılmalıdır."
        )

    report.append(
        "Akşam saatlerinde hafif yürüyüş daha güvenlidir."
    )

    return {

        "report": report,

        "risk_level": risk_level,

        "safe_ranges": safe_ranges,

        "pollutants": latest_values

    }