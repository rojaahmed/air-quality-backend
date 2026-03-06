from database import get_db
from collections import defaultdict


def get_aqi_map_points():
    with get_db() as db:
        db.execute("""
            SELECT 
                i.isim,
                i.enlem,
                i.boylam,
                s.tahmin
            FROM istasyonlar i
            JOIN saatlik_tahmin_catboost s
                ON s.istasyon_id = i.id
            WHERE s.tarih_saat >= CURRENT_TIMESTAMP
            ORDER BY s.tarih_saat
        """)
        rows = db.fetchall()

    points = []

    for r in rows:
        points.append({
            "name": r[0],
            "lat": float(r[1]),
            "lon": float(r[2]),
            "aqi": float(r[3])
        })

    return normalize_points(points)


# -------------------------------------
# AQI KATEGORİ
# -------------------------------------

def aqi_category(aqi):
    if aqi <= 50:
        return "Temiz"
    elif aqi <= 100:
        return "Orta"
    else:
        return "Kirli"


# -------------------------------------
# İSTASYON BAŞINA TEK AQI HESABI
# (MAX kullanıyoruz)
# -------------------------------------

def normalize_points(points):
    grouped = defaultdict(list)

    for p in points:
        key = (p["name"], p["lat"], p["lon"])
        grouped[key].append(p["aqi"])

    result = []

    for (name, lat, lon), aqis in grouped.items():

        # AQI = en yüksek kirletici
        station_aqi = max(aqis)

        result.append({
            "name": name,
            "lat": lat,
            "lon": lon,
            "aqi": round(station_aqi, 1),
            "category": aqi_category(station_aqi)
        })

    return result