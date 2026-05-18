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

from services.anomaly_service import detect_anomaly

NOTIFY_WINDOW_MIN = 0
NOTIFY_WINDOW_MAX = 90

# =====================================================
# ANOMALY COUNTER
# =====================================================

ANOMALY_COUNTER = {}


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

    # =====================================================
    # 🔥 GERÇEK SARIMA / ARIMA TABANLI
    # 🔥 DİNAMİK ANOMALİ ERKEN UYARI SİSTEMİ
    # =====================================================

    with get_db() as db:

        db.execute("""
            SELECT p.id, p.isim
            FROM istasyon_parametreleri ip
            JOIN parametreler p
            ON p.id = ip.parametre_id
            WHERE ip.istasyon_id=%s
        """, (station["id"],))

        station_parameters = db.fetchall()

    print(
        f"İSTASYON PARAMETRELERİ: {station_parameters}"
    )

    # =====================================================
    # HER PARAMETRE İÇİN ANOMALY ANALİZİ
    # =====================================================

    for parametre_id, pollutant_name in station_parameters:

        try:

            # =====================================================
            # GEÇMİŞ VERİLER
            # =====================================================

            with get_db() as db:

                db.execute("""
                    SELECT tahmin
                    FROM saatlik_tahmin_gecmis
                    WHERE istasyon_id=%s
                    AND parametre_id=%s
                    ORDER BY tarih_saat DESC
                    LIMIT 48
                """, (
                    station["id"],
                    parametre_id
                ))

                rows = db.fetchall()

            values = [
                float(r[0])
                for r in rows
                if r[0] is not None
            ]

            values.reverse()

            print(
                f"{pollutant_name} VALUES COUNT:",
                len(values)
            )

            print(
                f"{pollutant_name} VALUES:",
                values[-5:] if values else []
            )

            # =====================================================
            # YETERLİ VERİ KONTROLÜ
            # =====================================================

            if len(values) < 24:

                print(
                    f"{pollutant_name} için yeterli veri yok"
                )

                continue

            # =====================================================
            # ANOMALY DETECTION
            # =====================================================

            anomaly = detect_anomaly(
                values,
                station["id"],
                parametre_id
            )

            print(
                f"ANOMALY RESULT {pollutant_name}:",
                anomaly
            )

            # =====================================================
            # CACHE KEY
            # =====================================================

            key = (
                f"{station['id']}_{parametre_id}"
            )

            # =====================================================
            # ANOMALY COUNTER
            # =====================================================

            if anomaly.get("is_anomaly"):

                ANOMALY_COUNTER[key] = (

                    ANOMALY_COUNTER.get(key, 0) + 1

                )

            else:

                ANOMALY_COUNTER[key] = 0

            print(
                f"ANOMALY COUNTER {key}:",
                ANOMALY_COUNTER[key]
            )

            # =====================================================
            # 2 ARDIŞIK ANOMALİ ŞARTI
            # =====================================================

            if ANOMALY_COUNTER[key] >= 2:

                predicted = anomaly.get("predicted")

                actual = anomaly.get("actual")

                difference = anomaly.get("difference")

                difference_percent = anomaly.get(
                    "difference_percent"
                )

                severity = anomaly.get(
                    "severity"
                )

                send_notification(

                    user_data["firebase_token"],

                    f"🚨 {pollutant_name} Anomali Uyarısı",

                    (
                        f"{pollutant_name} seviyesinde "
                        f"anormal hava değişimi algılandı.\n\n"

                        f"Beklenen: {predicted}\n"

                        f"Gerçek: {actual}\n"

                        f"Fark: {difference}\n"

                        f"Sapma: %{difference_percent}\n"

                        f"Risk: {severity}\n\n"

                        f"Lütfen dış ortamda uzun süre kalmayın."
                    )
                )

                print(
                    f"ANOMALİ BİLDİRİMİ GÖNDERİLDİ: "
                    f"{pollutant_name}"
                )

                # =====================================================
                # COUNTER RESET
                # =====================================================

                ANOMALY_COUNTER[key] = 0

            else:

                print(
                    f"{pollutant_name} için "
                    f"henüz yeterli anomaly yok"
                )

        except Exception as e:

            print(
                f"ANOMALİ HATASI "
                f"{pollutant_name}: {e}"
            )

    # =====================================================
    # 🔥 ESKİ KİŞİSEL UYARI SİSTEMİ
    # 🔥 HİÇ DEĞİŞMEDİ
    # =====================================================

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

        if not (
            timedelta(minutes=NOTIFY_WINDOW_MIN)
            <= time_until <=
            timedelta(minutes=NOTIFY_WINDOW_MAX)
        ):
            continue

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

            # =====================================================
            # ESKİ RİSK SİSTEMİ
            # =====================================================

            message = check_user_risk(
                user_data,
                prediction
            )

            print("MESSAGE:", message)
            print("AQI:", aqi)
            print("CATEGORY:", category)

            # =====================================================
            # HEALTH SCORE
            # =====================================================

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

            # =====================================================
            # EN YÜKSEK AQI
            # =====================================================

            if aqi > highest_aqi:

                if not message:

                    message = (
                        f"{pollutant} seviyeleri izleniyor."
                    )

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