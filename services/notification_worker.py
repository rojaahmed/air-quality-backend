from database import get_db
from services.location_service import find_nearest_station
from services.notification_service import send_notification
from services.forecast_service import get_next_7_hours
from health_engine import check_user_risk
from services.aqi_utils import compute_pollutant_aqi, aqi_category
from datetime import datetime, timedelta

from services.health_score import (
    calculate_health_risk,
    risk_level
)

NOTIFY_WINDOW_MIN = 0
NOTIFY_WINDOW_MAX = 90


def run_notification_job():

    print("Notification job started")

    with get_db() as db:

        db.execute("""
            SELECT id, kronik_hastalik, yas,
                   firebase_token, latitude, longitude
            FROM kullanicilar
            WHERE firebase_token IS NOT NULL
        """)

        users = db.fetchall()

    for user in users:

        try:
            _process_user(user)

        except Exception as e:
            print(f"Kullanıcı {user[0]} için hata: {e}")


def _process_user(user):

    user_data = {
        "id": user[0],
        "kronik_hastalik": user[1],
        "yas": user[2],
        "firebase_token": user[3],
        "latitude": user[4],
        "longitude": user[5]
    }

    station = find_nearest_station(
        user_data["latitude"],
        user_data["longitude"]
    )

    data = get_next_7_hours(station["name"])

    for p in data["hours"]:

        now = datetime.now()

        hour = int(
            p["hour"].split(":")[0]
        )

        prediction_dt = now.replace(
            hour=hour,
            minute=0,
            second=0,
            microsecond=0
        )

        if prediction_dt <= now:
            prediction_dt += timedelta(days=1)

        time_until = prediction_dt - now

        #if not (
          #  timedelta(minutes=NOTIFY_WINDOW_MIN)
          #  <= time_until <=
          #  timedelta(minutes=NOTIFY_WINDOW_MAX)
        #):
        #    continue

        best_message = None
        highest_aqi = -1
        best_pollutant = None

        for pollutant, value in p["pollutants"].items():

            if isinstance(value, dict):
                value = value["value"]

            aqi = compute_pollutant_aqi(
                pollutant,
                value
            )

            if aqi is None:
                continue

            category = aqi_category(aqi)

            prediction = {
                "hour": hour,
                "pollutant": pollutant,
                "category": category
            }

            # 🔥 ESKİ SİSTEM
            message = check_user_risk(
                user_data,
                prediction
            )
            print("MESSAGE:", message)
            print("AQI:", aqi)
            print("CATEGORY:", category)
           
            # 🔥 YENİ RİSK SİSTEMİ
            with get_db() as db:

                db.execute("""
                    SELECT COUNT(*)
                    FROM gonderilen_bildirimler
                    WHERE kullanici_id=%s
                    AND tarih >= CURRENT_DATE - INTERVAL '3 day'
                """, (user_data["id"],))

                exposure_count = db.fetchone()[0]

            score = calculate_health_risk(
                user_data,
                category,
                exposure_count
            )

            level = risk_level(score)

            # 🔥 ESKİ SİSTEM DEVAM EDİYOR
            if message and aqi > highest_aqi:

                highest_aqi = aqi

                best_message = (
    f"{message}\n\n"
    f"Risk Skoru: {score}/100\n"
    f"Risk Durumu: {level}\n"
    f"Son 3 Gün Maruziyet: {exposure_count}"
)

                best_pollutant = pollutant

        if not best_message:
            continue

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

            if db.fetchone():

                print(
                    f"Zaten gönderildi: kullanıcı={user_data['id']} saat={hour}"
                )

                continue
            print(best_message)
            send_notification(
                user_data["firebase_token"],
                f"Hava Kalitesi Uyarısı {hour}",
                best_message
            )


            print(
                f"Bildirim gönderildi: kullanıcı={user_data['id']} saat={hour}"
            )

            db.execute("""
                INSERT INTO gonderilen_bildirimler
                (kullanici_id, saat, parametre, tarih)
                VALUES (%s, %s, %s, CURRENT_DATE)
            """, (
                user_data["id"],
                hour,
                best_pollutant
            ))