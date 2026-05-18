from pmdarima import auto_arima
import numpy as np

# ======================================================
# MODEL CACHE
# ======================================================

MODEL_CACHE = {}

# ======================================================
# ANOMALY DETECTION
# ======================================================

def detect_anomaly(
    values,
    station_id=None,
    parametre_id=None
):

    # ======================================================
    # MINIMUM DATA CONTROL
    # ======================================================

    if len(values) < 24:

        return {
            "status": "not_enough_data"
        }

    try:

        # ======================================================
        # TRAIN / ACTUAL
        # ======================================================

        train = values[:-1]

        actual = float(values[-1])

        # ======================================================
        # CACHE KEY
        # ======================================================

        cache_key = (
            f"{station_id}_{parametre_id}"
        )

        # ======================================================
        # MODEL CACHE CONTROL
        # ======================================================

        if cache_key in MODEL_CACHE:

            model = MODEL_CACHE[cache_key]

        else:

            # ======================================================
            # AUTO ARIMA
            # ======================================================

            model = auto_arima(

                train,

                seasonal=False,

                suppress_warnings=True,

                error_action="ignore",

                trace=False
                stepwise=True

            )

            # CACHE SAVE
            MODEL_CACHE[cache_key] = model

        # ======================================================
        # FORECAST
        # ======================================================

        forecast, conf_int = model.predict(

            n_periods=1,

            return_conf_int=True

        )

        predicted = float(forecast[0])

        # ======================================================
        # CONFIDENCE INTERVAL
        # ======================================================

        lower_bound = float(
            conf_int[0][0]
        )

        upper_bound = float(
            conf_int[0][1]
        )

        # ======================================================
        # DIFFERENCE
        # ======================================================

        difference = abs(
            actual - predicted
        )

        # ======================================================
        # DIFFERENCE PERCENT
        # ======================================================

        difference_percent = (
            difference /
            max(abs(predicted), 1)
        )

        # ======================================================
        # ANOMALY LOGIC
        # ======================================================

        is_anomaly = (

            (
                actual < lower_bound
                or
                actual > upper_bound
            )

            and

            difference_percent > 0.25

        )

        # ======================================================
        # SEVERITY
        # ======================================================

        severity = (

            "HIGH"

            if difference_percent > 1

            else

            "MEDIUM"

            if difference_percent > 0.5

            else

            "LOW"

        )

        # ======================================================
        # RETURN
        # ======================================================

        return {

            "predicted": round(
                predicted,
                2
            ),

            "actual": round(
                actual,
                2
            ),

            "difference": round(
                difference,
                2
            ),

            "difference_percent": round(
                difference_percent * 100,
                2
            ),

            "lower_bound": round(
                lower_bound,
                2
            ),

            "upper_bound": round(
                upper_bound,
                2
            ),

            "severity": severity,

            "is_anomaly": bool(
                is_anomaly
            )

        }

    except Exception as e:

        print(
            "ANOMALY ERROR:",
            str(e)
        )

        return {

            "error": str(e)

        }