import requests
from utils1 import haversine

OVERPASS_URL = "https://overpass-api.de/api/interpreter"


def get_nearby_health_places(lat, lon):

  
    query = f"""
[out:json];
(
  node["amenity"="hospital"](around:3000,{lat},{lon});
  way["amenity"="hospital"](around:3000,{lat},{lon});
  relation["amenity"="hospital"](around:3000,{lat},{lon});

  node["amenity"="pharmacy"](around:3000,{lat},{lon});
  way["amenity"="pharmacy"](around:3000,{lat},{lon});
  relation["amenity"="pharmacy"](around:3000,{lat},{lon});
);
out center;
"""

    response = requests.get(
        OVERPASS_URL,
        params={"data": query},
        timeout=20
    )

    if response.status_code != 200:
        return []

    data = response.json()

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