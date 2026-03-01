# aqi_service.py


from .aqi_utils import compute_pollutant_aqi, aqi_category

def compute_station_aqi(data):
    """
    data = {
       "PM10": 80,
       "O3": 0.060,
       "SO2": 40,
       "CO": 5.0
    }
    """

    results = {}

    for pollutant, value in data.items():
        aqi = compute_pollutant_aqi(pollutant, value)
        results[pollutant] = aqi

    # En kötü olan istasyon AQI skorudur
    station_aqi = max(results.values())

    return {
        "pollutants": results,
        "station_aqi": station_aqi,
      "category": aqi_category(station_aqi)
    }


def get_aqi_category(aqi):
    if aqi <= 50:
        return "Good"
    elif aqi <= 100:
        return "Moderate"
    elif aqi <= 150:
        return "Unhealthy for Sensitive Groups"
    elif aqi <= 200:
        return "Unhealthy"
    elif aqi <= 300:
        return "Very Unhealthy"
    else:
        return "Hazardous"