import requests
from utils1 import haversine

OVERPASS_URL = "https://overpass.kumi.systems/api/interpreter"

def get_nearby_health_places(lat, lon):

    query = f"""
[out:json][timeout:25];
(
  nwr["amenity"="hospital"](around:10000,{lat},{lon});
  nwr["amenity"="pharmacy"](around:10000,{lat},{lon});
);
out center;
"""

    response = requests.get(
        OVERPASS_URL,
        params={"data": query},
        timeout=20
    )
    print(response.text)

    if response.status_code != 200:
        return []

    data = response.json()

    if "elements" not in data:
        return []

    print(data)

    results = []

    for element in data["elements"]:

        if "lat" in element:
            place_lat = element["lat"]
            place_lon = element["lon"]
        else:
            place_lat = element["center"]["lat"]
            place_lon = element["center"]["lon"]

        tags = element.get("tags", {})

        distance = haversine(
            lat,
            lon,
            place_lat,
            place_lon
        )

        address = (
            tags.get("addr:street", "") +
            " " +
            tags.get("addr:housenumber", "")
        ).strip()

        results.append({
            "name": tags.get("name", "İsimsiz"),
            "type": tags.get("amenity"),
            "lat": place_lat,
            "lon": place_lon,
            "distance": round(distance / 1000, 2),
            "address": address
        })

    results.sort(key=lambda x: x["distance"])

    return results