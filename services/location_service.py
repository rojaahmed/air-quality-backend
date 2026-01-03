from database import get_db
import math

def find_nearest_station(lat: float, lon: float):
    with get_db() as db:
        db.execute("""
            SELECT id, isim, enlem, boylam, Konum
            FROM istasyonlar
        """)
        stations = db.fetchall()

    def distance(lat1, lon1, lat2, lon2):
        return math.sqrt((lat1 - lat2)**2 + (lon1 - lon2)**2)

    nearest = None
    min_dist = float("inf")

    for s in stations:
        d = distance(lat, lon, s[2], s[3])  # enlem, boylam
        if d < min_dist:
            min_dist = d
            nearest = s

    if nearest is None:
        return None

    return {
        "id": nearest[0],
        "name": nearest[1]
    }
