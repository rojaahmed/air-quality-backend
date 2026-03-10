from health_rules import disease_pollutants


def is_risky(category):

    risky_levels = ["orta", "kirli", "çok kirli"]

    return category in risky_levels


def disease_sensitive(disease, pollutant):

    if disease not in disease_pollutants:
        return False

    return pollutant in disease_pollutants[disease]