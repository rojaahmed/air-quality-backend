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

# aqi_utils.py

# EPA BREAKPOINT TABLOLARI
BREAKPOINTS = {
    "PM10": [
        (0, 54, 0, 50),
        (55, 154, 51, 100),
        (155, 254, 101, 150),
        (255, 354, 151, 200),
        (355, 424, 201, 300),
        (425, 504, 301, 400),
        (505, 604, 401, 500),
    ],
    "O3": [
        (0.000, 0.054, 0, 50),
        (0.055, 0.070, 51, 100),
        (0.071, 0.085, 101, 150),
        (0.086, 0.105, 151, 200),
        (0.106, 0.200, 201, 300),
    ],
    "SO2": [
        (0, 35, 0, 50),
        (36, 75, 51, 100),
        (76, 185, 101, 150),
        (186, 304, 151, 200),
        (305, 604, 201, 300),
        (605, 804, 301, 400),
        (805, 1004, 401, 500),
    ],
    "CO": [
        (0.0, 4.4, 0, 50),
        (4.5, 9.4, 51, 100),
        (9.5, 12.4, 101, 150),
        (12.5, 15.4, 151, 200),
        (15.5, 30.4, 201, 300),
    ]
}


# FORMÜL
def calc_aqi_single(C, breakpoints):
    for C_low, C_high, I_low, I_high in breakpoints:
        if C_low <= C <= C_high:
            return ((I_high - I_low) / (C_high - C_low)) * (C - C_low) + I_low

    return None  # değer aralık dışıysa


# Ana fonksiyon
def compute_pollutant_aqi(pollutant, value):
    if pollutant not in BREAKPOINTS:
        return None

    return calc_aqi_single(value, BREAKPOINTS[pollutant])