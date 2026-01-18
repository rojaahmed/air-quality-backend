DISEASE_RULES = {

    "Astım": {
        "PM10": {
            "medium": (20, 50),
            "bad": (50, 999),
            "messages": {
                "good": "Astım hastaları için hava uygundur.",
                "medium": "PM10 orta seviyede, dikkatli olun.",
                "bad": "PM10 yüksek, evde kalmanız önerilir."
            }
        },
        "O3": {
            "medium": (120, 180),
            "bad": (180, 999),
            "messages": {
                "good": "Ozon seviyesi güvenlidir.",
                "medium": "Ozon astımı tetikleyebilir.",
                "bad": "Ozon seviyesi tehlikelidir."
            }
        },
        "SO2": {
            "medium": (100, 350),
            "bad": (350, 999),
            "messages": {
                "good": "SO₂ güvenli seviyededir.",
                "medium": "SO₂ solunum yollarını tahriş edebilir.",
                "bad": "SO₂ astım krizini tetikleyebilir."
            }
        },
        "CO": {
            "medium": (5, 10),
            "bad": (10, 999),
            "messages": {
                "good": "CO seviyesi güvenlidir.",
                "medium": "Baş dönmesi yapabilir.",
                "bad": "CO seviyesi tehlikelidir."
            }
        }
    },

    "KOAH": {
        "PM10": {
            "medium": (25, 50),
            "bad": (50, 999),
            "messages": {
                "good": "KOAH hastaları için hava uygundur.",
                "medium": "Uzun süre dışarıda kalmayın.",
                "bad": "Ciddi solunum riski."
            }
        },
        "O3": {
            "medium": (120, 180),
            "bad": (180, 999),
            "messages": {
                "good": "Ozon seviyesi kabul edilebilir.",
                "medium": "Solunum zorlaşabilir.",
                "bad": "KOAH için tehlikelidir."
            }
        },
        "SO2": {
            "medium": (100, 350),
            "bad": (350, 999),
            "messages": {
                "good": "SO₂ normal seviyede.",
                "medium": "Bronşları tahriş edebilir.",
                "bad": "Ağır solunum riski."
            }
        },
        "CO": {
            "medium": (5, 10),
            "bad": (10, 999),
            "messages": {
                "good": "CO seviyesi güvenli.",
                "medium": "Nefes darlığı yapabilir.",
                "bad": "Hayati risk oluşturur."
            }
        }
    },

    "Kalp Hastalığı": {
        "PM10": {
            "medium": (30, 60),
            "bad": (60, 999),
            "messages": {
                "good": "Kalp hastaları için hava uygundur.",
                "medium": "Fiziksel aktiviteleri azaltın.",
                "bad": "Kalp hastaları için ciddi risk."
            }
        },
        "O3": {
            "medium": (120, 180),
            "bad": (180, 999),
            "messages": {
                "good": "Ozon seviyesi güvenlidir.",
                "medium": "Kalp ritmini etkileyebilir.",
                "bad": "Kalp krizi riski artar."
            }
        },
        "SO2": {
            "medium": (100, 350),
            "bad": (350, 999),
            "messages": {
                "good": "SO₂ normal seviyede.",
                "medium": "Kalp yükü artabilir.",
                "bad": "Kalp için tehlikelidir."
            }
        },
        "CO": {
            "medium": (5, 10),
            "bad": (10, 999),
            "messages": {
                "good": "CO seviyesi güvenlidir.",
                "medium": "Baş dönmesi yapabilir.",
                "bad": "CO seviyesi kalp için tehlikelidir."
            }
        }
    },

    "Gebelik": {
        "PM10": {
            "medium": (25, 50),
            "bad": (50, 999),
            "messages": {
                "good": "Gebeler için hava uygundur.",
                "medium": "Uzun süre dışarıda kalmayın.",
                "bad": "Gebelik için risklidir."
            }
        },
        "O3": {
            "medium": (120, 180),
            "bad": (180, 999),
            "messages": {
                "good": "Ozon güvenlidir.",
                "medium": "Baş ağrısı yapabilir.",
                "bad": "Anne ve bebek için risklidir."
            }
        },
        "SO2": {
            "medium": (100, 350),
            "bad": (350, 999),
            "messages": {
                "good": "SO₂ normal seviyede.",
                "medium": "Solunum rahatsızlığı yapabilir.",
                "bad": "Gebelikte tehlikelidir."
            }
        },
        "CO": {
            "medium": (5, 10),
            "bad": (10, 999),
            "messages": {
                "good": "CO seviyesi güvenlidir.",
                "medium": "Baş dönmesi olabilir.",
                "bad": "Bebek için ciddi risk."
            }
        }
    },

    "65 Yaş Üstü": {
        "PM10": {
            "medium": (30, 60),
            "bad": (60, 999),
            "messages": {
                "good": "Yaşlı bireyler için uygundur.",
                "medium": "Dış aktiviteler azaltılmalı.",
                "bad": "Sağlık riski yüksektir."
            }
        },
        "O3": {
            "medium": (120, 180),
            "bad": (180, 999),
            "messages": {
                "good": "Ozon güvenlidir.",
                "medium": "Nefes darlığı yapabilir.",
                "bad": "Acil sağlık riski."
            }
        },
        "SO2": {
            "medium": (100, 350),
            "bad": (350, 999),
            "messages": {
                "good": "SO₂ normal.",
                "medium": "Solunum yolları etkilenebilir.",
                "bad": "Hayati risk oluşturur."
            }
        },
        "CO": {
            "medium": (5, 10),
            "bad": (10, 999),
            "messages": {
                "good": "CO seviyesi güvenlidir.",
                "medium": "Sersemlik yapabilir.",
                "bad": "Zehirlenme riski."
            }
        }
    }
}
