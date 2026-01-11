from database import get_db

def get_aqi_map_points():
    with get_db() as db:
        db.execute("""
            SELECT 
                i.isim,
                i.enlem,
                i.boylam,
                s.tahmin,
                s.kategori
            FROM istasyonlar i
            JOIN saatlik_tahmin_catboost s
              ON s.istasyon_id = i.id
            WHERE s.tarih_saat >= CURRENT_TIMESTAMP
        """)
        rows = db.fetchall()

    result = []
    for r in rows:
        result.append({
            "name": r[0],
            "lat": r[1],
            "lon": r[2],
            "aqi": float(r[3]),
            "category": r[4]
        })

    return result
