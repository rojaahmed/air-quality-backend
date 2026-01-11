import requests
from database import get_db
from utils1 import haversine

# --------------------------------
# AQI – IDW
# --------------------------------
def get_stations():
    with get_db() as db:
        db.execute("""
            SELECT i.enlem, i.boylam, s.tahmin
            FROM istasyonlar i
            JOIN saatlik_tahmin_catboost s
              ON s.istasyon_id = i.id
            WHERE s.tarih_saat >= CURRENT_TIMESTAMP
        """)
        return db.fetchall()

def idw_aqi(lat, lon):
    stations = get_stations()
    num, den = 0.0, 0.0

    for s_lat, s_lon, aqi in stations:
        aqi = float(aqi)

        d = haversine(lat, lon, s_lat, s_lon) / 1000
        if d < 0.5:
            return aqi

        w = 1 / (d ** 2)
        num += aqi * w
        den += w

    return num / den if den else 50

# --------------------------------
# OSRM ROUTE
# --------------------------------
def get_osrm_route(start, end):
    url = (
        f"https://router.project-osrm.org/route/v1/driving/"
        f"{start[1]},{start[0]};{end[1]},{end[0]}"
        f"?overview=full&geometries=geojson"
    )
    r = requests.get(url, timeout=10)
    data = r.json()
    coords = data["routes"][0]["geometry"]["coordinates"]
    return [(lat, lon) for lon, lat in coords]

# --------------------------------
# ROUTE SAMPLING
# --------------------------------
def sample_route(route, step_m=80):
    sampled = [route[0]]
    acc = 0

    for i in range(1, len(route)):
        d = haversine(
            route[i-1][0], route[i-1][1],
            route[i][0], route[i][1]
        )
        acc += d
        if acc >= step_m:
            sampled.append(route[i])
            acc = 0

    sampled.append(route[-1])
    return sampled

def corridor(point, offset=0.0005):
    lat, lon = point
    return [
        (lat, lon),
        (lat + offset, lon),
        (lat - offset, lon),
        (lat, lon + offset),
        (lat, lon - offset),
    ]

# --------------------------------
# CLEAN ROUTE
# --------------------------------
def find_clean_route(start, end):
    base_route = get_osrm_route(start, end)
    sampled = sample_route(base_route)

    clean_route = []
    for p in sampled:
        options = corridor(p)
        best = min(options, key=lambda x: idw_aqi(x[0], x[1]))
        clean_route.append(best)

    return clean_route
