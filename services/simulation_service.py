def simulate_air_quality(
        activity,
        age,
        disease,
        aqi):

    score = 0

    score += aqi

    if age >= 60:
        score += 30

    if disease != "Yok":
        score += 40

    if activity == "Morning Run":
        score += 25

    elif activity == "Cycling":
        score += 15

    elif activity == "Walking":
        score += 10

    # risk seviyesi

    if score < 80:

        risk = "Low"

        message = (
            "Outdoor activity is safe."
        )

    elif score < 140:

        risk = "Medium"

        message = (
            "Sensitive groups should be careful."
        )

    elif score < 200:

        risk = "High"

        message = (
            "Outdoor activity is not recommended."
        )

    else:

        risk = "Critical"

        message = (
            "Stay indoors."
        )

    return {

        "risk_level": risk,
        "score": score,
        "message": message

    }