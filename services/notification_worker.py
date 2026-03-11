from database import get_db
from services.location_service import find_nearest_station
from services.notification_service import send_notification
from services.forecast_service import get_next_7_hours
from health_engine import check_user_risk
from services.aqi_utils import compute_pollutant_aqi, aqi_category
from datetime import datetime


def run_notification_job():

    print("Notification job started")

    with get_db() as db:
        db.execute("""
        SELECT id, kronik_hastalik, firebase_token, latitude, longitude
        FROM kullanicilar
        WHERE firebase_token IS NOT NULL
        """)
        users = db.fetchall()

    for user in users:

        user_data = {
            "id": user[0],
            "kronik_hastalik": user[1],
            "firebase_token": user[2],
            "latitude": user[3],
            "longitude": user[4]
        }

        lat = user_data["latitude"]
        lon = user_data["longitude"]

        station = find_nearest_station(lat, lon)

        data = get_next_7_hours(station["name"])
        predictions = data["hours"]

        for p in predictions:

            # saat string -> int
            hour = int(p["hour"].split(":")[0])

            # datetime oluştur
            prediction_time = datetime.now().replace(
                hour=hour, minute=0, second=0, microsecond=0
            )

            # geçmiş saatleri atla
            if prediction_time <= datetime.now():
                continue

            message = None

            for pollutant, value in p["pollutants"].items():

                # value bazen dict olabilir
                if isinstance(value, dict):
                    value = value["value"]

                aqi = compute_pollutant_aqi(pollutant, value)

                if aqi is None:
                    continue

                category = aqi_category(aqi)

                print(hour, pollutant, value, category)

                prediction = {
                    "hour": hour,
                    "pollutant": pollutant,
                    "category": category
                }

                message = check_user_risk(user_data, prediction)

                if message:
                    send_notification(
                        user_data["firebase_token"],
                        "Hava Kalitesi Uyarısı",
                        message
                    )

                    print(f"Notification sent to {user_data['id']}")
                    break

            if message:
                break