import heapq
import requests
from utils1 import haversine
from database import get_db
from services.aqi_utils import aqi_category
import datetime
import osmnx as ox
import networkx as nx
import pickle
from functools import lru_cache


GRID_SIZE = 0.00025   # yaklaşık 25–28 metre

with open("roads.pkl","rb") as f:
    G = pickle.load(f)


def node_to_coord(node):
    return (G.nodes[node]["y"], G.nodes[node]["x"])


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


# ⚡ sadece bir kere çekiyoruz
STATIONS = get_stations()


# ⚡ CACHE EKLEDİK (çok hızlandırır)
@lru_cache(maxsize=50000)
def idw_aqi(lat, lon):

    num, den = 0, 0

    for s_lat, s_lon, aqi in STATIONS:

        dist = haversine(lat, lon, s_lat, s_lon) / 1000

        if dist < 0.2:
            return float(aqi)

        w = 1 / (dist ** 2)

        num += float(aqi) * w
        den += w

    return num / den if den else 50


# --------------------- Trafik & Sanayi ---------------------
def traffic_multiplier():

    wd = datetime.datetime.now().weekday()
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


# --------------------- HEURISTIC ---------------------
def heuristic(a, b):

    return haversine(a[0], a[1], b[0], b[1])


# ---------------------- A* ROAD ROTA ----------------------
def find_clean_route(start, end):

    # ⚡ TRAFİK BİR KERE HESAPLANIYOR
    traf = traffic_multiplier()

    # en yakın yol node'ları
    start_node = ox.distance.nearest_nodes(G, start[1], start[0])
    end_node = ox.distance.nearest_nodes(G, end[1], end[0])

    def cost(u, v, d):

        a = node_to_coord(u)
        b = node_to_coord(v)

        # gerçek yol uzunluğu
        dist = d.get("length", haversine(a[0], a[1], b[0], b[1]))

        # ⚡ cache daha iyi çalışsın diye yuvarlama
        lat = round(b[0], 4)
        lon = round(b[1], 4)

        aqi = idw_aqi(lat, lon)
        ind = industry_penalty(lat, lon)

        return dist * (1 + aqi / 60) * traf * ind


    route = nx.astar_path(
        G,
        start_node,
        end_node,
        heuristic=lambda u, v: heuristic(node_to_coord(u), node_to_coord(v)),
        weight=cost
    )

    # node → koordinat
    path = [node_to_coord(n) for n in route]

    return path