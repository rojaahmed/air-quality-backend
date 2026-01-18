from datetime import datetime
from rules import DISEASE_RULES
from email_service import send_email

def get_status(value, ranges):
    for status, (min_v, max_v) in ranges.items():
        if min_v <= value < max_v:
            return status
    return None


def process_hourly_notifications(user, forecast):
    """
    user: {
      username, email, disease
    }

    forecast: [
      {"hour": "14:00", "PM10": 60, "SO2": 110}
    ]
    """

    current_hour = datetime.now().strftime("%H:00")
    disease = user["disease"]

    if disease not in DISEASE_RULES:
        return

    rules = DISEASE_RULES[disease]
    mail_body = ""

    for item in forecast:
        if item["hour"] != current_hour:
            continue

        for param, value in item.items():
            if param == "hour":
                continue

            if param not in rules:
                continue

            param_rules = rules[param]
            ranges = {
                k: v for k, v in param_rules.items()
                if k in ["temiz", "orta", "kirli"]
            }

            status = get_status(value, ranges)
            message = param_rules["messages"][status]

            mail_body += (
                f"Saat {current_hour}\n"
                f"{param}: {value} → {status.upper()}\n"
                f"{message}\n\n"
            )

    if mail_body:
        send_email(
            user["email"],
            "Saatlik Hava Kalitesi Uyarısı",
            f"Sayın {user['username']},\n\n{mail_body}"
        )
