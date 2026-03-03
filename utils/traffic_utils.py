import datetime

def traffic_multiplier():
    weekday = datetime.datetime.now().weekday()

    if weekday == 5:   # Cumartesi
        return 1.4
    if weekday == 6:   # Pazar
        return 1.7
    return 1.0