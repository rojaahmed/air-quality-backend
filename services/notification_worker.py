from database import get_db
from services.location_service import find_nearest_station
from services.notification_service import send_notification
from services.forecast_service import get_next_7_hours
from services.aqi_utils import compute_pollutant_aqi, aqi_category
from health_engine import disease_sensitive, is_risky
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

        print("User:", user_data["id"], "Station:", station["name"])

        data = get_next_7_hours(station["name"])
        predictions = data["hours"]

        for p in predictions:

            hour = int(p["hour"].split(":")[0])

            prediction_time = datetime.now().replace(
                hour=hour, minute=0, second=0, microsecond=0
            )

            if prediction_time <= datetime.now():
                continue

            print("Checking hour:", hour)

            risky_pollutants = []

            for pollutant, value in p["pollutants"].items():

                print("Checking pollutant:", pollutant)

                if isinstance(value, dict):
                    value = value["value"]

                aqi = compute_pollutant_aqi(pollutant, value)

                if aqi is None:
                    continue

                category = aqi_category(aqi)

                print("AQI:", pollutant, value, category)

                if disease_sensitive(user_data["kronik_hastalik"], pollutant) and is_risky(category):

                    risky_pollutants.append((pollutant, category))

            # Eğer riskli parametre varsa
            if risky_pollutants:

                # Daha önce gönderilmiş mi kontrol et
                with get_db() as db:
                    db.execute("""
                    SELECT 1
                    FROM gonderilen_bildirimler
                    WHERE kullanici_id=%s
                    AND saat=%s
                    AND tarih=CURRENT_DATE
                    """, (user_data["id"], hour))

                    sent = db.fetchone()

                if sent:
                    print("Notification already sent")
                    continue

                text = ""

                for pol, cat in risky_pollutants:
                    text += f"{pol} seviyesi {cat}\n"

                message = f"""
⚠️ Hava Kalitesi Uyarısı

{hour:02d}:00 saatinde bulunduğunuz bölgede

{text}

Sağlığınız için dikkatli olunması önerilir.
"""

                send_notification(
                    user_data["firebase_token"],
                    "Hava Kalitesi Uyarısı",
                    message
                )

                print(f"Notification sent to {user_data['id']}")

                # Gönderildi olarak kaydet
                with get_db() as db:
                    db.execute("""
                    INSERT INTO gonderilen_bildirimler
                    (kullanici_id, saat, tarih)
                    VALUES (%s,%s,CURRENT_DATE)
                    """, (user_data["id"], hour))