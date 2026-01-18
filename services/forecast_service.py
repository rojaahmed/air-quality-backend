from database import get_db
from datetime import datetime, date, timedelta

DEFAULT_STATION = "Gaziantep"
STATION_MAP = {
    "gaziantep": "Gaziantep",
    "atapark": "Atapark",
    "fevzicakmak": "Fevzi Çakmak",
    "beydilli": "Beydilli",
    "nizip": "Nizip",
    "gaskid6": "Gaski D6"
}

# -------------------------
# 7 GÜNLÜK TAHMİN (GÜNLÜK)
# -------------------------
def get_7_day_forecast(station_name: str = DEFAULT_STATION):
    with get_db() as db:
        db.execute("""
            SELECT
                g.tahmin_tarihi,
                p.isim AS parametre,
                g.tahmin,
                g.kategori,
                g.mae,
                g.mse,
                g.r2
            FROM gunluk_tahmin_catboost g
            JOIN istasyonlar i ON i.id = g.istasyon_id
            JOIN parametreler p ON p.id = g.parametre_id
            WHERE i.isim = %s
              AND g.tahmin_tarihi >= CURRENT_DATE
            ORDER BY g.tahmin_tarihi, g.gun
        """, (station_name,))
        rows = db.fetchall()

    return _format_forecast(rows, "daily", station_name)



# -------------------------
# 7 SAATLİK TAHMİN
# -------------------------
def get_7_hour_forecast(station_name: str = DEFAULT_STATION):
    with get_db() as db:
        db.execute("""
            SELECT 
                s.tarih_saat,  -- 0
                p.isim,        -- 1
                s.tahmin,      -- 2
                s.kategori     -- 3
            FROM saatlik_tahmin_catboost s
            JOIN istasyonlar i ON i.id = s.istasyon_id
            JOIN parametreler p ON p.id = s.parametre_id
            WHERE i.isim = %s
              AND s.tarih_saat >= CURRENT_TIMESTAMP
            ORDER BY s.tarih_saat
        """, (station_name,))
        rows = db.fetchall()

    return _format_forecast(rows, "hourly", station_name)


# -------------------------
# ORTAK FORMATLAYICI
# -------------------------
def _format_forecast(rows, forecast_type, station_name):
    if not rows:
        return None

    labels = []
    parameters = {}

    for r in rows:
        label = str(r[0])  # tarih / saat

        if label not in labels:
            labels.append(label)

        param = r[1]  # parametre adı

        if param not in parameters:
            parameters[param] = []

        parameters[param].append({
            "value": round(float(r[2]), 2),
            "category": r[3]
        })

    return {
        "station": station_name,
        "type": forecast_type,
        "labels": labels,
        "parameters": [
            {"name": p, "values": v}
            for p, v in parameters.items()
        ]
    }


# -------------------------
# SONRAKİ 7 SAAT
# -------------------------
def get_next_7_hours(station_name: str = DEFAULT_STATION):
    now = datetime.now()
    end_time = now + timedelta(hours=7)

    with get_db() as db:
        db.execute("""
            SELECT
                s.tarih_saat,  -- 0
                p.isim,        -- 1
                s.tahmin,      -- 2
                s.kategori     -- 3
            FROM saatlik_tahmin_catboost s
            JOIN istasyonlar i ON i.id = s.istasyon_id
            JOIN parametreler p ON p.id = s.parametre_id
            WHERE i.isim = %s
              AND s.tarih_saat >= %s
              AND s.tarih_saat < %s
            ORDER BY s.tarih_saat
        """, (station_name, now, end_time))
        rows = db.fetchall()

    if not rows:
        return {"hours": []}

    hourly = {}

    for r in rows:
        hour = r[0].strftime("%H:00")

        if hour not in hourly:
            hourly[hour] = {"hour": hour, "pollutants": {}}

        hourly[hour]["pollutants"][r[1]] = round(float(r[2]), 2)

    return {
        "station": station_name,
        "type": "next_7_hours",
        "hours": list(hourly.values())
    }


# -------------------------
# SEÇİLİ GÜN – SONRAKİ 7 SAAT
# -------------------------
def get_selected_day_next_7_hours(selected_date: date, station_name: str = DEFAULT_STATION):
    with get_db() as db:
        db.execute("""
            WITH last_run AS (
                SELECT MAX(olusturma_tarihi)
                FROM saatlik_tahmin_catboost
                WHERE istasyon_id = (
                    SELECT id FROM istasyonlar WHERE isim = %s
                )
                  AND CAST(tarih_saat AS DATE) = %s
            )
            SELECT
                s.tarih_saat,  -- 0
                p.isim,        -- 1
                s.tahmin,      -- 2
                s.kategori     -- 3
            FROM saatlik_tahmin_catboost s
            JOIN istasyonlar i ON i.id = s.istasyon_id
            JOIN parametreler p ON p.id = s.parametre_id
            WHERE i.isim = %s
              AND CAST(s.tarih_saat AS DATE) = %s
            ORDER BY s.tarih_saat
        """, (station_name, selected_date, station_name, selected_date))
        rows = db.fetchall()

    if not rows:
        return None

    hourly = {}

    for r in rows:
        hour = r[0].strftime("%H:00")

        if hour not in hourly:
            hourly[hour] = {"hour": hour, "pollutants": {}}

        hourly[hour]["pollutants"][r[1]] = {
            "value": round(float(r[2]), 2),
            "category": r[3]
        }

    return {
        "station": station_name,
        "date": str(selected_date),
        "type": "selected_day_next_7_hours",
        "hours": list(hourly.values())
    }

