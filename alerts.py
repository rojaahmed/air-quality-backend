# backend/routes/alerts.py
from fastapi import APIRouter
from pydantic import BaseModel
from services.alert_engine import generate_daily_health_alerts
from services.forecast_service import get_next_7_hours

router = APIRouter()

class HealthAlertRequest(BaseModel):
    user_name: str
    disease: str
    station_name: str

@router.post("/health-alerts")
def health_alerts(req: HealthAlertRequest):

    forecast = get_next_7_hours(req.station_name)

    hours = forecast.get("hours", [])

    if not hours:
        return []

    station_parameters = set()

    for hour in hours:
     station_parameters.update(hour.get("pollutants", {}).keys())

     station_parameters = list(station_parameters)


    return generate_daily_health_alerts(
        user_name=req.user_name,
        disease=req.disease,
        hourly_data=hours,
        station_parameters=station_parameters
    )

