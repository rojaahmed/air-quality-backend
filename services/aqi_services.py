from .aqi_utils import compute_pollutant_aqi, aqi_category

def compute_station_aqi(data):
    results = {}

    for pollutant, value in data.items():
        if value is None:   # veri yoksa hesaplama yapma
            results[pollutant] = None
            continue

        aqi = compute_pollutant_aqi(pollutant, value)
        results[pollutant] = aqi

    # None olmayanları seç
    valid_aqi = [v for v in results.values() if v is not None]

    if not valid_aqi:
        return {
            "pollutants": results,
            "station_aqi": None,
            "category": "Veri Yok"
        }

    station_aqi = max(valid_aqi)

    return {
        "pollutants": results,
        "station_aqi": station_aqi,
        "category": aqi_category(station_aqi)
    }