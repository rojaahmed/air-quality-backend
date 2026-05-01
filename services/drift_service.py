import json
import statistics


def analyze_single_model(data):

    maes = []
    r2_scores = []

    for station in data:

        predictions = station.get("tahminler", [])

        for pred in predictions:

            mae = pred.get("mae")
            r2 = pred.get("r2")

            if mae is not None:
                maes.append(mae)

            if r2 is not None:
                r2_scores.append(r2)

    if not maes:

        return {
            "status": "no_data"
        }

    avg_mae = round(statistics.mean(maes), 2)
    avg_r2 = round(statistics.mean(r2_scores), 3)

    drift_status = "Stable"

    ai_warning = (
        "Model performansı stabil çalışmaktadır."
    )

    if avg_mae > 15 or avg_r2 < 0.70:

        drift_status = "High Drift"

        ai_warning = (
            "Model performansında ciddi düşüş "
            "tespit edildi."
        )

    elif avg_mae > 8 or avg_r2 < 0.85:

        drift_status = "Medium Drift"

        ai_warning = (
            "Model performansında orta seviyede "
            "sapma gözlemlendi."
        )

    return {

        "avg_mae": avg_mae,

        "avg_r2": avg_r2,

        "drift_status": drift_status,

        "ai_warning": ai_warning,

        "prediction_count": len(maes)
    }


def analyze_model_drift():

    with open(
        "data/gunluk_tahmin_catboost.json",
        "r",
        encoding="utf-8"
    ) as f:

        daily_data = json.load(f)

    with open(
        "data/saatlik_tahmin_catboost.json",
        "r",
        encoding="utf-8"
    ) as f:

        hourly_data = json.load(f)

    daily_result = analyze_single_model(
        daily_data
    )

    hourly_result = analyze_single_model(
        hourly_data
    )

    overall_status = "Stable"

    if (
        daily_result["drift_status"] == "High Drift"
        or
        hourly_result["drift_status"] == "High Drift"
    ):

        overall_status = "High Drift"

    elif (
        daily_result["drift_status"] == "Medium Drift"
        or
        hourly_result["drift_status"] == "Medium Drift"
    ):

        overall_status = "Medium Drift"

    overall_ai_message = (
        "Tüm modeller stabil çalışmaktadır."
    )

    if overall_status == "High Drift":

        overall_ai_message = (
            "AI sisteminde ciddi performans "
            "düşüşü tespit edildi."
        )

    elif overall_status == "Medium Drift":

        overall_ai_message = (
            "Bazı modellerde performans "
            "sapması gözlemlendi."
        )

    return {

        "overall_status": overall_status,

        "overall_ai_message":
            overall_ai_message,

        "daily_model":
            daily_result,

        "hourly_model":
            hourly_result
    }