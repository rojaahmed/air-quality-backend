from risk_engine import disease_sensitive, is_risky


def check_user_risk(user, prediction):

    disease = user["kronik_hastalik"]
    pollutant = prediction["pollutant"]

    category = prediction["category"].lower()
    hour = prediction["hour"]

    if not disease:
        return None

    if not disease_sensitive(disease, pollutant):
        return None

    if not is_risky(category):
        return None

    message = f"""
⚠️ Hava Kalitesi Uyarısı

{hour} saatinde bulunduğunuz bölgede
{pollutant} seviyesi {category} seviyesine çıkacak.

{disease} hastaları için risk oluşturabilir.

Maske kullanmanız ve dışarıda uzun süre kalmamanız önerilir.
"""

    return message