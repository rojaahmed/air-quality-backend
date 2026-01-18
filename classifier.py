def classify_pollutant(value, rule):
    """
    rule = {
      "medium": (x, y),
      "bad": (y, z)
    }
    """
    if "bad" in rule and rule["bad"][0] <= value <= rule["bad"][1]:
        return "bad"
    if "medium" in rule and rule["medium"][0] <= value <= rule["medium"][1]:
        return "medium"
    return "good"
