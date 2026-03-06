from database import get_db
from collections import defaultdict
from services.clean_route_service import idw_aqi


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
# İSTASYON AQI (database)
# -------------------------------------

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
# İSTASYON BAŞINA TEK AQI
# -------------------------------------

def normalize_points(points):
    grouped = defaultdict(list)

    for p in points:
        key = (p["name"], p["lat"], p["lon"])
        grouped[key].append(p["aqi"])

    result = []

    for (name, lat, lon), aqis in grouped.items():

        station_aqi = max(aqis)

        result.append({
            "name": name,
            "lat": lat,
            "lon": lon,
            "aqi": round(station_aqi, 1),
            "category": aqi_category(station_aqi)
        })

    return result


# -------------------------------------
# IDW GRID (kullanıcı çevresi AQI)
# -------------------------------------

def generate_nearby_points(user_lat, user_lon):

    points = []

    step = 0.01   # ~1 km
    size = 2      # 5x5 grid → 25 nokta

    for i in range(-size, size + 1):
        for j in range(-size, size + 1):

            lat = user_lat + i * step
            lon = user_lon + j * step

            aqi = idw_aqi(lat, lon)

            points.append({
                "name": f"Point {len(points)+1}",
                "lat": lat,
                "lon": lon,
                "aqi": round(aqi, 1),
                "category": aqi_category(aqi)
            })

    return points