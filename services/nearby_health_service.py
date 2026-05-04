import requests
from utils1 import haversine

OVERPASS_URL = "https://overpass.kumi.systems/api/interpreter"


def get_nearby_health_places(lat, lon):

    try:

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

        pharmacies = []
        hospitals = []

        for element in data["elements"]:

            if "lat" in element:
                place_lat = element["lat"]
                place_lon = element["lon"]

            elif "center" in element:
                place_lat = element["center"]["lat"]
                place_lon = element["center"]["lon"]

            else:
                continue

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

            item = {
                "name": tags.get("name", "İsimsiz"),
                "type": tags.get("amenity"),
                "lat": place_lat,
                "lon": place_lon,
                "distance": round(distance / 1000, 2),
                "address": address
            }

            if item["type"] == "hospital":
                hospitals.append(item)

            elif item["type"] == "pharmacy":
                pharmacies.append(item)

        hospitals.sort(key=lambda x: x["distance"])
        pharmacies.sort(key=lambda x: x["distance"])

        results = hospitals[:10] + pharmacies[:10]

        results.sort(key=lambda x: x["distance"])

        return results

    except Exception as e:

        print("HEALTH SERVICE ERROR:", e)

        return []