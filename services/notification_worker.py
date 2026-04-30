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

            hour = int(p["hour"].split(":")[0])

            prediction_time = datetime.now().replace(
                hour=hour, minute=0, second=0, microsecond=0
            )

            if prediction_time <= datetime.now():
                continue

            best_message = None
            highest_aqi = -1
            best_pollutant = None

            for pollutant, value in p["pollutants"].items():

                print("Checking:", user_data["id"], hour, pollutant)

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

                # EN YÜKSEK AQI'Yİ SEÇ
                if message and aqi > highest_aqi:
                    highest_aqi = aqi
                    best_message = message
                    best_pollutant = pollutant

            # TÜM POLLUTANTLAR BİTTİKTEN SONRA GÖNDER
            if best_message:

                # 🔴 DAHA ÖNCE GÖNDERİLDİ Mİ?
                with get_db() as db:
                    db.execute("""
                    SELECT 1
                    FROM gonderilen_bildirimler
                    WHERE kullanici_id=%s
                    AND saat=%s
                    AND parametre=%s
                    AND tarih=CURRENT_DATE
                    """, (
                        user_data["id"],
                        hour,
                        best_pollutant
                    ))

                    sent = db.fetchone()

                if sent:
                    print("Notification already sent")
                    continue

                # 🔔 BİLDİRİM GÖNDER
                send_notification(
                    user_data["firebase_token"],
                    "Hava Kalitesi Uyarısı",
                    best_message
                )

                print(f"Notification sent to {user_data['id']}")

                # 🟢 GÖNDERİLDİ OLARAK KAYDET
                with get_db() as db:
                    db.execute("""
                    INSERT INTO gonderilen_bildirimler
                    (kullanici_id, saat, parametre, tarih)
                    VALUES (%s,%s,%s,CURRENT_DATE)
                    """, (
                        user_data["id"],
                        hour,
                        best_pollutant
                    ))