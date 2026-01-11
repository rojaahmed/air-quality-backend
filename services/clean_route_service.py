import heapq
from database import get_db
from utils1 import haversine

# -------------------------
# İSTASYONLARI VERİTABANINDAN ÇEK
# -------------------------
def get_stations():
    """
    Tüm istasyonların:
    (enlem, boylam, aqi_tahmin)
    bilgilerini döndürür
    """
    with get_db() as db:
        db.execute("""
            SELECT 
                i.enlem,
                i.boylam,
                s.tahmin
            FROM istasyonlar i
            JOIN saatlik_tahmin_catboost s
              ON s.istasyon_id = i.id
            WHERE s.tarih_saat >= CURRENT_TIMESTAMP
        """)
        return db.fetchall()


# -------------------------
# IDW (Inverse Distance Weighting) ile AQI
# -------------------------
def idw_aqi(lat, lon):
    """
    Verilen noktadaki AQI değerini
    istasyonlara göre tahmin eder
    """
    stations = get_stations()

    numerator = 0.0
    denominator = 0.0

    for s_lat, s_lon, aqi in stations:
        distance_km = haversine(lat, lon, s_lat, s_lon) / 1000

        # Çok yakın istasyon varsa direkt onu al
        if distance_km < 0.5:
            return aqi

        weight = 1 / (distance_km ** 2)
        numerator += aqi * weight
        denominator += weight

    return numerator / denominator if denominator != 0 else 50


# -------------------------
# KOMŞU NOKTALARI ÜRET
# -------------------------
def get_neighbors(node, step=0.002):
    """
    Grid tabanlı komşuluk (8 yön)
    """
    lat, lon = node
    neighbors = []

    for dlat in [-step, 0, step]:
        for dlon in [-step, 0, step]:
            if dlat != 0 or dlon != 0:
                neighbors.append((lat + dlat, lon + dlon))

    return neighbors


# -------------------------
# A* ALGORİTMASI (AQI AĞIRLIKLI)
# -------------------------
def a_star(start, goal):
    """
    En temiz rotayı döndürür
    cost = mesafe × (1 + AQI / 100)
    """
    open_set = []
    heapq.heappush(open_set, (0, start))

    came_from = {}
    g_score = {start: 0}

    while open_set:
        _, current = heapq.heappop(open_set)

        # Hedefe yaklaştıysak bitir
        if haversine(
            current[0], current[1],
            goal[0], goal[1]
        ) < 200:
            return reconstruct_path(came_from, current)

        for neighbor in get_neighbors(current):
            distance = haversine(
                current[0], current[1],
                neighbor[0], neighbor[1]
            )

            aqi = idw_aqi(neighbor[0], neighbor[1])
            cost = distance * (1 + aqi / 100)

            tentative_g = g_score[current] + cost

            if neighbor not in g_score or tentative_g < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g

                f_score = tentative_g + haversine(
                    neighbor[0], neighbor[1],
                    goal[0], goal[1]
                )

                heapq.heappush(open_set, (f_score, neighbor))

    return []


# -------------------------
# ROTA GERİ OLUŞTURMA
# -------------------------
def reconstruct_path(came_from, current):
    path = [current]

    while current in came_from:
        current = came_from[current]
        path.append(current)

    return path[::-1]
