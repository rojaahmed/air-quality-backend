DISEASE_RULES = {

    "Astım": {
        "PM10": {
            "good": (0, 20),
            "medium": (20, 50),
            "bad": (50, 999),
            "messages": {
                "good": "Hava kalitesi astım hastaları için uygundur.",
                "medium": "Astım hastaları için PM10 orta seviyede, dikkatli olun.",
                "bad": "Astım hastaları için PM10 yüksek, evde kalmanız veya maske takmanız önerilir."
            }
        },
        "SO2": {
            "medium": (100, 350),
            "bad": (350, 999),
            "messages": {
                "medium": "SO₂ solunum yollarını tahriş edebilir.",
                "bad": "SO₂ seviyesi astım krizini tetikleyebilir."
            }
        },
        "O3": {
            "medium": (120, 180),
            "bad": (180, 999),
            "messages": {
                "medium": "Ozon astımı olumsuz etkileyebilir.",
                "bad": "Ozon seviyesi tehlikeli, dışarı çıkmayınız."
            }
        }
    },

    "KOAH": {
        "PM10": {
            "good": (0, 25),
            "medium": (25, 50),
            "bad": (50, 999),
            "messages": {
                "good": "KOAH hastaları için hava kalitesi iyi.",
                "medium": "KOAH hastaları için PM10 orta düzeyde, uzun süre dışarıda kalmayın.",
                "bad": "KOAH hastaları için ciddi risk, evde kalmanız önerilir."
            }
        },
        "NO2": {
            "medium": (100, 200),
            "bad": (200, 999),
            "messages": {
                "medium": "NO₂ solunum fonksiyonlarını zorlayabilir.",
                "bad": "NO₂ seviyesi KOAH hastaları için tehlikelidir."
            }
        }
    },

    "Alerjik Rinit": {
        "PM10": {
            "medium": (30, 60),
            "bad": (60, 999),
            "messages": {
                "good": "Alerjik rinit için hava koşulları uygundur.",
                "medium": "Alerjik belirtiler artabilir.",
                "bad": "Alerjik rinit şikayetleri ciddi şekilde artabilir."
            }
        }
    },

    "Kronik Bronşit": {
        "PM10": {
            "medium": (25, 50),
            "bad": (50, 999),
            "messages": {
                "good": "Solunum için uygun hava koşulları.",
                "medium": "Öksürük ve nefes darlığı artabilir.",
                "bad": "Kronik bronşit hastaları için risklidir."
            }
        }
    },

    "Akciğer Fibrozu": {
        "PM10": {
            "medium": (20, 40),
            "bad": (40, 999),
            "messages": {
                "good": "Akciğerler için uygun hava.",
                "medium": "Solunum zorlaşabilir.",
                "bad": "Akciğer fibrozu için ciddi risk."
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
        "CO": {
            "medium": (5, 10),
            "bad": (10, 999),
            "messages": {
                "medium": "Baş dönmesi yapabilir.",
                "bad": "CO seviyesi kalp için tehlikelidir."
            }
        }
    },

    "Hipertansiyon": {
        "PM10": {
            "medium": (40, 70),
            "bad": (70, 999),
            "messages": {
                "good": "Tansiyon hastaları için uygun.",
                "medium": "Tansiyon dalgalanmaları görülebilir.",
                "bad": "Hipertansiyon için riskli hava."
            }
        }
    },

    "Diyabet": {
        "PM10": {
            "bad": (80, 999),
            "messages": {
                "good": "Diyabet için risk yok.",
                "bad": "Diyabet hastalarında enfeksiyon riski artabilir."
            }
        }
    },

    "Bağışıklık Sistemi Zayıf": {
        "PM10": {
            "medium": (20, 40),
            "bad": (40, 999),
            "messages": {
                "good": "Genel sağlık için uygun.",
                "medium": "Bağışıklık sistemi zorlanabilir.",
                "bad": "Enfeksiyon riski yüksektir."
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
                "bad": "Gebelikte risklidir, evde kalın."
            }
        }
    },

    "Sigara Kullanımı": {
        "PM10": {
            "medium": (20, 40),
            "bad": (40, 999),
            "messages": {
                "good": "Hava kalitesi yeterlidir.",
                "medium": "Solunum yolları zorlanabilir.",
                "bad": "Sigara kullananlar için ciddi risk."
            }
        }
    },

    "65 Yaş Üstü": {
        "PM10": {
            "medium": (30, 60),
            "bad": (60, 999),
            "messages": {
                "good": "Yaşlı bireyler için hava uygundur.",
                "medium": "Dış aktiviteler sınırlandırılmalı.",
                "bad": "Sağlık riski yüksektir."
            }
        }
    }
}
