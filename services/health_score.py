def calculate_health_risk(user, category, exposure_count):

    score = 0

    # =====================
    # YAŞ ETKİSİ
    # =====================
    yas = user.get("yas", 0)

    if yas >= 65:
        score += 25

    elif yas >= 50:
        score += 15

    elif yas >= 35:
        score += 5

    # =====================
    # HASTALIK ETKİSİ
    # =====================
    disease = user.get("kronik_hastalik", "Yok")

    if disease == "Astım":
        score += 30

    elif disease == "KOAH":
        score += 40

    elif disease == "Alerjik Rinit":
        score += 15

    elif disease == "Kronik Bronşit":
        score += 30

    elif disease == "Akciğer Fibrozu":
        score += 40

    elif disease == "Kalp Hastalığı":
        score += 35

    elif disease == "Hipertansiyon":
        score += 20

    elif disease == "Diyabet":
        score += 20

    elif disease == "Bağışıklık Sistemi Zayıf":
        score += 35

    elif disease == "Gebelik":
        score += 15

    elif disease == "Sigara Kullanımı":
        score += 20

    elif disease == "65 Yaş Üstü":
        score += 25

    elif disease == "Diğer":
        score += 10

    # =====================
    # HAVA KALİTESİ ETKİSİ
    # =====================
    if category == "iyi":
        score += 0

    elif category == "orta":
        score += 15

    elif category == "hassas":
        score += 25

    elif category == "kirli":
        score += 35

    elif category == "çok kirli":
        score += 45

    elif category == "tehlikeli":
        score += 60

    # =====================
    # GEÇMİŞ MARUZİYET
    # =====================
    if exposure_count >= 10:
        score += 30

    elif exposure_count >= 5:
        score += 20

    elif exposure_count >= 3:
        score += 10

    # =====================
    # MAX SCORE
    # =====================
    return min(score, 100)


def risk_level(score):

    if score >= 70:
        return "Yüksek Risk"

    elif score >= 40:
        return "Orta Risk"

    return "Düşük Risk"