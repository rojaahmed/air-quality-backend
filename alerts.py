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

    station_parameters = (
        list(hours[0]["pollutants"].keys())
        if hours and "pollutants" in hours[0]
        else None
    )

    disease = req.disease.strip()

    return generate_daily_health_alerts(
        user_name=req.user_name,
        disease=disease,
        hourly_data=hours,
        station_parameters=station_parameters
    )
