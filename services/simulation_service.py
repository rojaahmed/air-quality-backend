def simulate_air_quality(activity, age, disease, aqi):

    score = 0

    # AQI etkisi
    score += aqi

    # Yaş etkisi
    if age >= 65:
        score += 30
    elif age >= 50:
        score += 15

    # Hastalık etkileri
    disease_scores = {

        "Yok": 0,

        # Solunum sistemi
        "Astım": 45,
        "KOAH": 55,
        "Kronik Bronşit": 50,
        "Akciğer Fibrozu": 60,
        "Alerjik Rinit": 20,

        # Kalp ve dolaşım
        "Kalp Hastalığı": 40,
        "Hipertansiyon": 25,

        # Diğer
        "Diyabet": 20,
        "Bağışıklık Sistemi Zayıf": 35,
        "Gebelik": 20,
        "Sigara Kullanımı": 25,
        "65 Yaş Üstü": 30,
        "Diğer": 20,
    }

    # Kullanıcının hastalığına göre puan ekle
    score += disease_scores.get(disease, 20)

    # Aktivite etkileri
    activity_scores = {

        "Sabah Koşusu": 30,
        "Koşu": 30,
        "Futbol": 28,
        "Basketbol": 25,
        "Voleybol": 20,
        "Açık Havada Spor": 25,
        "Bisiklet Sürme": 18,
        "Doğa Yürüyüşü": 15,
        "Kamp": 12,
        "Bahçe İşleri": 12,
        "Açık Havada Çalışma": 15,
        "Yürüyüş": 8,
        "Piknik": 5,
        "Alışveriş": 5,
        "Çocuk Parkına Gitme": 8,
        "Evcil Hayvan Gezdirme": 8,
        "Balık Tutma": 5,
        "Motosiklet Sürme": 10,
        "Gezinti": 5,
        "Dinlenme": 0,
    }

    # Aktiviteye göre puan ekle
    score += activity_scores.get(activity, 10)

    # Risk seviyeleri
    if score < 80:
        risk = "Düşük"
        message = "Açık hava aktivitesi güvenlidir."

    elif score < 140:
        risk = "Orta"
        message = "Hassas gruplar dikkatli olmalıdır."

    elif score < 200:
        risk = "Yüksek"
        message = "Açık hava aktivitesi önerilmez."

    else:
        risk = "Kritik"
        message = "Mümkünse kapalı ortamda kalın."

    return {
        "risk_level": risk,
        "score": score,
        "message": message
    }