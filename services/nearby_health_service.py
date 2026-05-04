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
out center;
"""

def reverse_geocode(lat, lon):
    try:
        r = requests.get(
            "https://nominatim.openstreetmap.org/reverse",
            params={
                "lat": lat,
                "lon": lon,
                "format": "json",
                "addressdetails": 1,
            },
            headers={"User-Agent": "AirQualityApp/1.0"},
            timeout=5,
        )
        if r.status_code == 200:
            data = r.json()
            addr = data.get("address", {})
            parts = [
                addr.get("road", ""),
                addr.get("house_number", ""),
                addr.get("suburb", ""),
                addr.get("district", ""),
            ]
            return ", ".join(p for p in parts if p).strip(", ") or "Adres bulunamadı"
    except Exception as e:
        print(f"[GEOCODE] Hata: {e}")
    return "Adres bulunamadı"

def fetch_from_overpass(lat, lon):
    query = build_query(lat, lon)
    last_error = None
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
            last_error = "timeout"
        except Exception as e:
            print(f"[OVERPASS] {url} → Hata: {e}")
            last_error = str(e)
    raise RuntimeError(f"Tüm endpointler başarısız: {last_error}")

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

        # Önce OSM tag'lerinden dene
        address = (
            tags.get("addr:street", "") + " " +
            tags.get("addr:housenumber", "")
        ).strip()

        # OSM'de yoksa Nominatim'den çek
        if not address:
            address = reverse_geocode(place_lat, place_lon)

        item = {
            "name": tags.get("name", "İsimsiz"),
            "type": amenity,
            "lat": place_lat,
            "lon": place_lon,
            "distance": round(distance / 1000, 2),
            "address": address,
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