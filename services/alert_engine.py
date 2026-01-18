# backend/services/alert_engine.py
from collections import defaultdict
from services.disease_rules import DISEASE_RULES

def generate_daily_health_alerts(
    user_name: str,
    disease: str,
    hourly_data: list,
    station_parameters: list = None
):
    alerts = []
    if disease not in DISEASE_RULES:
        return alerts

    rules = DISEASE_RULES[disease]
    max_values = defaultdict(float)

    for hour in hourly_data:
        for param, value in hour["pollutants"].items():
            if station_parameters and param not in station_parameters:
                continue
            if isinstance(value, (int, float)):
                max_values[param] = max(max_values[param], value)

    for param, value in max_values.items():
        if param not in rules:
            continue

        rule = rules[param]
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

    return alerts
