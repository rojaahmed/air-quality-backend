from database import get_db
from services.forecast_service import get_7_hour_forecast
from services.location_service import find_nearest_station
from risk_engine import check_user_risk
from notification_service import send_notification


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

        lat = user["latitude"]
        lon = user["longitude"]

        station = find_nearest_station(lat, lon)

        predictions = get_7_hour_forecast(station["name"])

        for p in predictions:

            message = check_user_risk(user, p)

            if message:

                send_notification(
                    user["firebase_token"],
                    "Hava Kalitesi Uyarısı",
                    message
                )

                print(f"Notification sent to {user['id']}")