from collections import defaultdict
from services.disease_rules import DISEASE_RULES

def generate_daily_health_alerts(
    user_name: str,
    disease: str,
    hourly_data: list,
    station_parameters: list = None
):
    alerts = []

    # ❗ Hastalık yoksa bile boş dönme, "Diğer" kullan
    rules = DISEASE_RULES.get(disease, DISEASE_RULES.get("Diğer"))
    if not rules:
        return alerts

    max_values = defaultdict(float)

    # 🔹 Gün içindeki maksimum değerleri al
    for hour in hourly_data:
        for param, value in hour.get("pollutants", {}).items():
            if station_parameters and param not in station_parameters:
                continue
            if isinstance(value, (int, float)):
                max_values[param] = max(max_values[param], value)

    # 🔹 Parametre bazlı uyarılar
    for param, rule in rules.items():
        value = max_values.get(param)

        # Parametre istasyonda yoksa atla
        if value is None:
            continue

        level = "good"

        if "bad" in rule and rule["bad"][0] <= value <= rule["bad"][1]:
            level = "bad"
        elif "medium" in rule and rule["medium"][0] <= value <= rule["medium"][1]:
            level = "medium"

        message = rule["messages"].get(level)

        if message:
            alerts.append({
                "severity": level,
                "message": f"Sayın {user_name}, bugün {param} değeri {value}. {message}"
            })

    # 🔥 EN KRİTİK GARANTİ
    if not alerts:
        alerts.append({
            "severity": "good",
            "message": f"Sayın {user_name}, bugün hava kalitesi {disease} hastaları için genel olarak uygundur."
        })

    return alerts
