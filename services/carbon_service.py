def calculate_carbon_footprint(
    car_km,
    electricity,
    flight_hours,
    meat_meals,
    public_transport_km
):

    total = (
        car_km * 0.21 +
        electricity * 0.43 +
        flight_hours * 90 +
        meat_meals * 2.5 -
        public_transport_km * 0.05
    )

    if total < 50:
        category = "Düşük"

        ai_advice = [
            "Harika gidiyorsun 🌱",
            "Toplu taşıma kullanımını sürdür",
            "Enerji tasarrufu yapmaya devam et"
        ]

    elif total < 150:
        category = "Orta"

        ai_advice = [
            "Araç kullanımını azaltabilirsin",
            "Kısa mesafelerde yürüyüş tercih et",
            "Elektrik tüketimini düşürmeye çalış"
        ]

    else:
        category = "Yüksek"

        ai_advice = [
            "Karbon ayak izin yüksek ⚠️",
            "Özel araç yerine toplu taşıma kullan",
            "Uçuş sayısını azaltmayı düşün",
            "Enerji tasarruflu cihazlar kullan"
        ]

    return {
        "carbon_kg": round(total, 2),
        "category": category,
        "ai_advice": ai_advice
    }