def aqi_category(aqi):
    if aqi <= 50:
        return "Temiz"
    elif aqi <= 100:
        return "Orta"
    elif aqi <= 150:
        return "Hassas"
    elif aqi <= 200:
        return "Kötü"
    else:
        return "Kirli"
