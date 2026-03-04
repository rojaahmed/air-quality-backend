import heapq
import requests
from utils1 import haversine
from database import get_db
from services.aqi_utils import aqi_category
import datetime

GRID_SIZE = 0.00025   # yaklaşık 25–28 metre

# ----------------------------- AQI – IDW -----------------------------
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
    num, den = 0, 0

    for s_lat, s_lon, aqi in stations:
        dist = haversine(lat, lon, s_lat, s_lon) / 1000
        if dist < 0.2:
            return float(aqi)

        w = 1 / (dist ** 2)
        num += float(aqi) * w
        den += w

    return num / den if den else 50


# --------------------- Trafik & Sanayi ---------------------
def traffic_multiplier():
    wd = datetime.datetime.now().weekday()  # 6 = pazar
    hour = datetime.datetime.now().hour

    mult = 1.0
    if wd == 5:
        mult *= 1.4
    if wd == 6:
        mult *= 1.6

    if 7 <= hour <= 10:
        mult *= 1.3
    if 17 <= hour <= 20:
        mult *= 1.35

    return mult

INDUSTRIAL_ZONES = [
    (37.0475, 37.3380),
    (37.0560, 37.3500),
]

def industry_penalty(lat, lon):
    for iz_lat, iz_lon in INDUSTRIAL_ZONES:
        d = haversine(lat, lon, iz_lat, iz_lon)
        if d < 800:
            return 1.35
    return 1.0


# --------------------- A* COST ---------------------
def node_cost(a, b):
    dist = haversine(a[0], a[1], b[0], b[1])
    aqi = idw_aqi(b[0], b[1])
    traf = traffic_multiplier()
    ind = industry_penalty(b[0], b[1])

    return dist * (1 + aqi / 60) * traf * ind


def heuristic(a, b):
    return haversine(a[0], a[1], b[0], b[1])


# ---------------------- A* GRID ROTA ----------------------
def find_clean_route(start, end):

    def neighbors(p):
        lat, lon = p
        d = GRID_SIZE
        return [
            (lat + d, lon),
            (lat - d, lon),
            (lat, lon + d),
            (lat, lon - d),
        ]

    open_set = []
    heapq.heappush(open_set, (0, start))

    came = {}
    g = {start: 0}
    visited = set()

    while open_set:
        _, current = heapq.heappop(open_set)
        if current in visited:
            continue
        visited.add(current)

        if heuristic(current, end) < 30:
            goal = current
            break

        for nb in neighbors(current):
            tentative_g = g[current] + node_cost(current, nb)

            if nb not in g or tentative_g < g[nb]:
                g[nb] = tentative_g
                f = tentative_g + heuristic(nb, end)
                heapq.heappush(open_set, (f, nb))
                came[nb] = current

    # path çıkar
    path = [goal]
    while path[-1] != start:
        path.append(came[path[-1]])
    return path[::-1]