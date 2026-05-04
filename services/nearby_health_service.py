import requests
from utils1 import haversine

OVERPASS_ENDPOINTS = [
    "https://overpass-api.de/api/interpreter",
    "https://overpass.kumi.systems/api/interpreter",
    "https://maps.mail.ru/osm/tools/overpass/api/interpreter",
]

def build_query(lat, lon):
    return f"""
[out:json][timeout:30];
(
  nwr["amenity"="hospital"](around:10000,{lat},{lon});
  nwr["amenity"="pharmacy"](around:10000,{lat},{lon});
);
out center tags;
"""

def format_address(tags):
    """OSM tag'lerinden adres oluştur, yoksa boş döndür."""
    street = tags.get("addr:street", "")
    number = tags.get("addr:housenumber", "")
    district = tags.get("addr:district", "") or tags.get("addr:suburb", "")
    city = tags.get("addr:city", "") or tags.get("addr:province", "")

    parts = []
    if street:
        parts.append(f"{street} {number}".strip())
    if district:
        parts.append(district)
    if city:
        parts.append(city)

    return ", ".join(parts) if parts else ""

def fetch_from_overpass(lat, lon):
    query = build_query(lat, lon)
    for url in OVERPASS_ENDPOINTS:
        try:
            response = requests.get(
                url,
                params={"data": query},
                timeout=35,
                headers={"User-Agent": "AirQualityApp/1.0"},
            )
            if response.status_code == 200:
                return response.json()
            print(f"[OVERPASS] {url} → {response.status_code}")
        except requests.exceptions.Timeout:
            print(f"[OVERPASS] {url} → Timeout")
        except Exception as e:
            print(f"[OVERPASS] {url} → Hata: {e}")
    raise RuntimeError("Tüm Overpass endpointleri başarısız")

def parse_elements(data, lat, lon):
    hospitals = []
    pharmacies = []

    for element in data.get("elements", []):
        if "lat" in element and "lon" in element:
            place_lat = element["lat"]
            place_lon = element["lon"]
        elif "center" in element:
            place_lat = element["center"]["lat"]
            place_lon = element["center"]["lon"]
        else:
            continue

        tags = element.get("tags", {})
        amenity = tags.get("amenity")

        if amenity not in ("hospital", "pharmacy"):
            continue

        distance = haversine(lat, lon, place_lat, place_lon)
        address = format_address(tags)

        item = {
            "name": tags.get("name", "İsimsiz"),
            "type": amenity,
            "lat": place_lat,
            "lon": place_lon,
            "distance": round(distance / 1000, 2),
            # Adres yoksa koordinatı göster — en azından kullanıcı bir şey görür
            "address": address if address else f"{round(place_lat,4)}, {round(place_lon,4)}",
        }

        if amenity == "hospital":
            hospitals.append(item)
        else:
            pharmacies.append(item)

    hospitals.sort(key=lambda x: x["distance"])
    pharmacies.sort(key=lambda x: x["distance"])

    results = hospitals[:10] + pharmacies[:10]
    results.sort(key=lambda x: x["distance"])
    return results

def get_nearby_health_places(lat, lon):
    try:
        data = fetch_from_overpass(lat, lon)
        return parse_elements(data, lat, lon)
    except Exception as e:
        print(f"[NEARBY HEALTH] Kritik hata: {e}")
        return []