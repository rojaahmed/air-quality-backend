from database import get_db


def get_station_measurements(station_id: int):
    with get_db() as cur:

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

        query = """
            SELECT parametre_id, tahmin
            FROM gunluk_tahmin_catboost
            WHERE istasyon_id = %s AND gun = 1
        """

        cur.execute(query, (station_id,))
        rows = cur.fetchall()

        for row in rows:
            param_id, value = row
            pol_name = pollutant_map.get(param_id)
            if pol_name:
                results[pol_name] = float(value)

        return results