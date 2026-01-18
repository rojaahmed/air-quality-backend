from services.disease_rules import DISEASE_RULES
from classifier import classify_pollutant

def generate_daily_health_alerts(user_name, disease, hourly_data, station_parameters):
    alerts = []

    if disease not in DISEASE_RULES:
        return alerts

    disease_rules = DISEASE_RULES[disease]

    for param in station_parameters:
        values = []

        for hour in hourly_data:
            if param in hour["pollutants"]:
                values.append(hour["pollutants"][param])

        if not values or param not in disease_rules:
            continue

        max_value = max(values)
        rule = disease_rules[param]

        severity = classify_pollutant(max_value, rule)
        message = rule["messages"].get(severity)

        if message:
            alerts.append({
                "parameter": param,
                "severity": severity,
                "message": f"Sayın {user_name}, bugün {param} değeri {max_value}. {message}"
            })

    return alerts
