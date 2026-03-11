from database import get_db
from services.forecast_service import get_7_hour_forecast
from services.location_service import find_nearest_station
from services.notification_service import send_notification
from health_engine import check_user_risk


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

        predictions = get_7_hour_forecast(station["name"])

        for p in predictions:

            message = check_user_risk(user_data, p)

            if message:

                send_notification(
                    user_data["firebase_token"],
                    "Hava Kalitesi Uyarısı",
                    message
                )

                print(f"Notification sent to {user_data['id']}")

                break