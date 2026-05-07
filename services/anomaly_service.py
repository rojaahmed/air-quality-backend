from statsmodels.tsa.statespace.sarimax import SARIMAX
import numpy as np


def detect_anomaly(values):

    if len(values) < 24:
        return {
            "status": "not_enough_data"
        }

    try:

        model = SARIMAX(
            values,
            order=(1,1,1),
            seasonal_order=(1,1,1,24)
        )

        model_fit = model.fit(disp=False)

        forecast = model_fit.forecast(steps=1)

        predicted = float(forecast[0])

        actual = float(values[-1])

        difference = abs(actual - predicted)

        threshold = np.std(values) * 2

        is_anomaly = difference > threshold

        return {
            "predicted": round(predicted, 2),
            "actual": round(actual, 2),
            "difference": round(difference, 2),
            "threshold": round(threshold, 2),
            "is_anomaly": bool(is_anomaly)
        }

    except Exception as e:

        return {
            "error": str(e)
        }