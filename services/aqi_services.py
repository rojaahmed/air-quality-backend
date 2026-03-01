from .aqi_utils import compute_pollutant_aqi, aqi_category

def compute_station_aqi(data):
    results = {}

    for pollutant, value in data.items():
        aqi = compute_pollutant_aqi(pollutant, value)
        results[pollutant] = aqi

    station_aqi = max(results.values())

    return {
        "pollutants": results,
        "station_aqi": station_aqi,
        "category": aqi_category(station_aqi)
    }