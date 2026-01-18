DISEASE_RULES = {

    "Astım": {
        "PM10": {
            "temiz": (0, 20),
            "orta": (20, 50),
            "kirli": (50, 999),
            "messages": {
                "temiz": "Hava kalitesi astım hastaları için uygundur.",
                "orta": "Astım hastaları için PM10 orta seviyede, dikkatli olun.",
                "kirli": "Astım hastaları için PM10 yüksek, maske takmanız önerilir."
            }
        },
        "SO2": {
            "orta": (100, 350),
            "kirli": (350, 999),
            "messages": {
                "orta": "SO₂ solunum yollarını tahriş edebilir.",
                "kirli": "SO₂ seviyesi astım krizini tetikleyebilir."
            }
        },
        "O3": {
            "orta": (120, 180),
            "kirli": (180, 999),
            "messages": {
                "orta": "Ozon astımı olumsuz etkileyebilir.",
                "kirli": "Ozon seviyesi tehlikelidir."
            }
        }
    },

    "KOAH": {
        "PM10": {
            "temiz": (0, 25),
            "orta": (25, 50),
            "kirli": (50, 999),
            "messages": {
                "temiz": "KOAH hastaları için hava temiz.",
                "orta": "PM10 orta düzeyde, dikkatli olun.",
                "kirli": "KOAH hastaları için ciddi risk vardır."
            }
        }
    },

    "Alerjik Rinit": {
        "PM10": {
            "temiz": (0, 30),
            "orta": (30, 60),
            "kirli": (60, 999),
            "messages": {
                "temiz": "Alerjik rinit için hava uygundur.",
                "orta": "Alerjik belirtiler artabilir.",
                "kirli": "Alerjik rinit şikayetleri ciddi şekilde artabilir."
            }
        }
    },

    "Kronik Bronşit": {
        "PM10": {
            "temiz": (0, 25),
            "orta": (25, 50),
            "kirli": (50, 999),
            "messages": {
                "temiz": "Solunum için uygun hava koşulları.",
                "orta": "Öksürük ve nefes darlığı artabilir.",
                "kirli": "Kronik bronşit hastaları için risklidir."
            }
        }
    },

    "Akciğer Fibrozu": {
        "PM10": {
            "temiz": (0, 20),
            "orta": (20, 40),
            "kirli": (40, 999),
            "messages": {
                "temiz": "Akciğerler için uygun hava.",
                "orta": "Solunum zorlaşabilir.",
                "kirli": "Akciğer fibrozu için ciddi risk."
            }
        }
    },

    "Kalp Hastalığı": {
        "PM10": {
            "temiz": (0, 30),
            "orta": (30, 60),
            "kirli": (60, 999),
            "messages": {
                "temiz": "Kalp hastaları için hava uygundur.",
                "orta": "Fiziksel aktiviteleri azaltın.",
                "kirli": "Kalp hastaları için ciddi risk."
            }
        }
    },

    "Hipertansiyon": {
        "PM10": {
            "temiz": (0, 40),
            "orta": (40, 70),
            "kirli": (70, 999),
            "messages": {
                "temiz": "Tansiyon hastaları için uygun.",
                "orta": "Tansiyon dalgalanmaları görülebilir.",
                "kirli": "Hipertansiyon için riskli hava."
            }
        }
    },

    "Diyabet": {
        "PM10": {
            "temiz": (0, 50),
            "orta": (50, 80),
            "kirli": (80, 999),
            "messages": {
                "temiz": "Diyabet için risk yok.",
                "orta": "Dikkatli olunması önerilir.",
                "kirli": "Diyabet hastalarında enfeksiyon riski artabilir."
            }
        }
    },

    "65 Yaş Üstü": {
        "PM10": {
            "temiz": (0, 30),
            "orta": (30, 60),
            "kirli": (60, 999),
            "messages": {
                "temiz": "Yaşlı bireyler için hava uygundur.",
                "orta": "Dış aktiviteler sınırlandırılmalı.",
                "kirli": "Sağlık riski yüksektir."
            }
        }
    }
}
