from database import SessionLocal
from models import GunlukTahminCatboost

def get_station_measurements(station_id: int):
    db = SessionLocal()

    # parametre_id -> hangi kirletici:
    # 1 = PM10
    # 2 = O3
    # 3 = SO2
    # 4 = CO

    pollutant_map = {
        1: "PM10",
        2: "O3",
        3: "SO2",
        4: "CO",
    }

    results = {
        "PM10": None,
        "O3": None,
        "SO2": None,
        "CO": None,
    }

    rows = (
        db.query(GunlukTahminCatboost)
        .filter(GunlukTahminCatboost.istasyon_id == station_id)
        .filter(GunlukTahminCatboost.gun == 1)  # “bugün” değeri
        .all()
    )

    for row in rows:
        pol_name = pollutant_map.get(row.parametre_id)
        if pol_name:
            results[pol_name] = float(row.tahmin)

    return results