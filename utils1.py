import math

# -------------------------
# HAVERSINE (METRE)
# -------------------------
def haversine(lat1, lon1, lat2, lon2):
    """
    İki nokta arası mesafeyi METRE cinsinden hesaplar
    """
    R = 6371000  # Dünya yarıçapı (metre)

    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)

    a = (
        math.sin(dphi / 2) ** 2
        + math.cos(phi1)
        * math.cos(phi2)
        * math.sin(dlambda / 2) ** 2
    )

    return 2 * R * math.atan2(math.sqrt(a), math.sqrt(1 - a))
