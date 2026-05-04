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

def fetch_from_overpass(lat, lon):
    query = build_query(lat, lon)
    last_error = None

    for url in OVERPASS_ENDPOINTS:
        try:
            response = requests.get(
                url,
                params={"data": query},
                timeout=35,  # Overpass timeout'undan büyük olmalı
                headers={"User-Agent": "AirQualityApp/1.0"},
            )

            if response.status_code == 200:
                return response.json()

            print(f"[OVERPASS] {url} → {response.status_code}")

        except requests.exceptions.Timeout:
            print(f"[OVERPASS] {url} → Timeout")
            last_error = "timeout"

        except requests.exceptions.ConnectionError as e:
            print(f"[OVERPASS] {url} → ConnectionError: {e}")
            last_error = str(e)

        except Exception as e:
            print(f"[OVERPASS] {url} → Hata: {e}")
            last_error = str(e)

    raise RuntimeError(f"Tüm Overpass endpointleri başarısız. Son hata: {last_error}")


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

        address = (
            tags.get("addr:street", "") + " " + tags.get("addr:housenumber", "")
        ).strip()

        item = {
            "name": tags.get("name", "İsimsiz"),
            "type": amenity,
            "lat": place_lat,
            "lon": place_lon,
            "distance": round(distance / 1000, 2),
            "address": address if address else "Adres bilgisi yok",
        }

        if amenity == "hospital":
            hospitals.append(item)
        elif amenity == "pharmacy":
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
        return []  # boş liste döndür, 500 verme