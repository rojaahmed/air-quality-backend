from statsmodels.tsa.statespace.sarimax import SARIMAX
import numpy as np


def detect_anomaly(values):

    if len(values) < 24:
        return {
            "status": "not_enough_data"
        }

    try:

        # TRAIN
        train = values[:-1]

        # GERÇEK DEĞER
        actual = float(values[-1])

        # MODEL
        model = SARIMAX(
            train,
            order=(1,1,1),
            seasonal_order=(1,1,1,24)
        )

        model_fit = model.fit(disp=False)

        # =========================
        # PROFESYONEL FORECAST
        # =========================

        forecast_obj = model_fit.get_forecast(steps=1)

        predicted = float(
            forecast_obj.predicted_mean[0]
        )

        conf_int = forecast_obj.conf_int()

        lower_bound = float(conf_int.iloc[0, 0])
        upper_bound = float(conf_int.iloc[0, 1])

        # INTERVAL DIŞIYSA ANOMALİ
        is_anomaly = (
            actual < lower_bound or
            actual > upper_bound
        )

        difference = abs(actual - predicted)

        return {

            "predicted": round(predicted, 2),

            "actual": round(actual, 2),

            "difference": round(difference, 2),

            "lower_bound": round(lower_bound, 2),

            "upper_bound": round(upper_bound, 2),

            "is_anomaly": bool(is_anomaly)
        }

    except Exception as e:

        return {
            "error": str(e)
        }