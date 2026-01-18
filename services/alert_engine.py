# services/alert_engine.py

from services.disease_rules import DISEASE_RULES

def generate_health_alerts(
    user_name: str,
    disease: str,
    station_parameters: list,
    hourly_data: list
):
    alerts = []

    if disease == "Yok" or disease not in DISEASE_RULES:
        return alerts

    rules = DISEASE_RULES[disease]

    for hour_info in hourly_data:
        hour = hour_info["hour"]

        for param in station_parameters:
            if param not in rules:
                continue

            value = hour_info.get(param)
            if value is None:
                continue

            param_rules = rules[param]

            for level in ["bad", "medium", "good"]:
                if level in param_rules:
                    min_v, max_v = param_rules[level]
                    if min_v <= value <= max_v:
                        msg = param_rules["messages"].get(level)
                        if msg:
                            alerts.append({
                                "hour": hour,
                                "parameter": param,
                                "severity": level,
                                "value": value,
                                "message": f"Sayın {user_name}, "
                                           f"{hour} saatlerinde {param} değeri {value}. {msg}"
                            })
                        break

    return alerts
