from database import get_db
from utils.geo_utils import haversine

def get_stations():
    with get_db() as db:
        db.execute("""
            SELECT i.enlem, i.boylam, s.tahmin
            FROM saatlik_tahmin_catboost s
            JOIN istasyonlar i ON i.id = s.istasyon_id
        """)
        return db.fetchall()


def idw_aqi(lat, lon):
    stations = get_stations()
    num = 0
    den = 0

    for s_lat, s_lon, aqi in stations:
        d = haversine(lat, lon, s_lat, s_lon)

        # 500 metre yakınsa direkt o istasyonun AQI değerini döndür
        if d < 0.5:  # kilometre cinsinden (haversine km döndürür)
            return aqi

        # Ağırlık: 1 / d²
        w = 1 / (d ** 2)
        num += aqi * w
        den += w

    return num / den if den else 50  # Hiç istasyon yoksa default 50