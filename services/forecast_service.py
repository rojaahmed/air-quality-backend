from database import get_db
from datetime import datetime, date,timedelta



DEFAULT_STATION = "Gaziantep"


# 7 GÜNLÜK TAHMİN (GÜNLÜK)

def get_7_day_forecast(station_name: str = DEFAULT_STATION):
    with get_db() as db:
        rows = db.execute("""
            SELECT 
                g.tahmin_tarihi,
                p.isim AS parametre,
                AVG(g.tahmin) AS tahmin,
                MAX(g.kategori) AS kategori
            FROM gunluk_tahmin_catboost g
            JOIN istasyonlar i ON i.id = g.istasyon_id
            JOIN parametreler p ON p.id = g.parametre_id
            WHERE i.isim = ?
              AND g.tahmin_tarihi >= CAST(GETDATE() AS DATE)
            GROUP BY g.tahmin_tarihi, p.isim
            ORDER BY g.tahmin_tarihi
        """, (station_name,)).fetchall()

    return _format_forecast(rows, "daily", station_name)



def get_7_hour_forecast(station_name: str = DEFAULT_STATION):
    with get_db() as db:
        rows = db.execute("""
            SELECT 
                s.tarih_saat,
                p.isim AS parametre,
                s.tahmin,
                s.kategori
            FROM saatlik_tahmin_catboost s
            JOIN istasyonlar i ON i.id = s.istasyon_id
            JOIN parametreler p ON p.id = s.parametre_id
            WHERE i.isim = ?
              AND s.tarih_saat >= GETDATE()
            ORDER BY s.tarih_saat
        """, (station_name,)).fetchall()

    return _format_forecast(rows, "hourly", station_name)



def _format_forecast(rows, forecast_type, station_name):
    if not rows:
        return None

    labels = []
    parameters = {}

    for r in rows:
        label = str(r[0])

        if label not in labels:
            labels.append(label)

        param = r.parametre
        if param not in parameters:
            parameters[param] = []

        parameters[param].append({
            "value": round(float(r.tahmin), 2),
            "category": r.kategori
        })

    return {
        "station": station_name,
        "type": forecast_type,
        "labels": labels,
        "parameters": [
            {
                "name": param,
                "values": values
            }
            for param, values in parameters.items()
        ]
    }
def get_next_7_hours(station_name: str = DEFAULT_STATION):
    now = datetime.now()
    end_time = now + timedelta(hours=7)

    with get_db() as db:
        rows = db.execute("""
            SELECT
                s.tarih_saat,
                p.isim AS parametre,
                s.tahmin,
                s.kategori
            FROM saatlik_tahmin_catboost s
            JOIN istasyonlar i ON i.id = s.istasyon_id
            JOIN parametreler p ON p.id = s.parametre_id
            WHERE i.isim = ?
              AND s.tarih_saat >= ?
              AND s.tarih_saat < ?
            ORDER BY s.tarih_saat
        """, (station_name, now, end_time)).fetchall()

    if not rows:
        return {"hours": []}

    hourly = {}

    for r in rows:
        hour = r.tarih_saat.strftime("%H:00")

        if hour not in hourly:
            hourly[hour] = {
                "hour": hour,
                "pollutants": {}
            }

        hourly[hour]["pollutants"][r.parametre] = round(float(r.tahmin), 2)

    return {
        "station": station_name,
        "type": "next_7_hours",
        "hours": list(hourly.values())
    }





from datetime import date
from typing import Optional

def get_selected_day_next_7_hours(
    selected_date: date,
    station_name: str = DEFAULT_STATION
):
    with get_db() as db:
        rows = db.execute("""
        WITH last_run AS (
    SELECT MAX(olusturma_tarihi) AS last_time
    FROM saatlik_tahmin_catboost
    WHERE istasyon_id = (
        SELECT id FROM istasyonlar WHERE isim = ?
    )
      AND CAST(tarih_saat AS DATE) = ?
)
SELECT
    s.tarih_saat,
    p.isim AS parametre,
    s.tahmin,
    s.kategori
FROM saatlik_tahmin_catboost s
JOIN istasyonlar i ON i.id = s.istasyon_id
JOIN parametreler p ON p.id = s.parametre_id
JOIN last_run lr ON s.olusturma_tarihi >= DATEADD(SECOND, -5, lr.last_time)
WHERE i.isim = ?
  AND CAST(s.tarih_saat AS DATE) = ?
ORDER BY s.tarih_saat;


        """, (station_name, selected_date, station_name, selected_date)
).fetchall()

    if not rows:
        return None

    hourly = {}

    for r in rows:
        hour_key = r.tarih_saat.strftime("%H:00")

        if hour_key not in hourly:
            hourly[hour_key] = {
                "hour": hour_key,
                "pollutants": {}
            }

        hourly[hour_key]["pollutants"][r.parametre] = {
            "value": round(float(r.tahmin), 2),
            "category": r.kategori
        }

    return {
        "station": station_name,
        "date": str(selected_date),
        "type": "selected_day_next_7_hours",
        "hours": list(hourly.values())
    }
