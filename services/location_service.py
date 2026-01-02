from database import get_db
import math

def find_nearest_station(lat: float, lon: float):
    with get_db() as db:
        stations = db.execute("""
            SELECT id, isim, enlem, boylam
            FROM istasyonlar
        """).fetchall()

    def distance(lat1, lon1, lat2, lon2):
        return math.sqrt((lat1-lat2)**2 + (lon1-lon2)**2)

    nearest = None
    min_dist = float("inf")

    for s in stations:
        d = distance(lat, lon, s.enlem, s.boylam)
        if d < min_dist:
            min_dist = d
            nearest = s

    return {
        "id": nearest.id,
        "name": nearest.isim
    }
