# api/alerts.py

from fastapi import APIRouter
from services.alert_engine import generate_health_alerts

router = APIRouter()

@router.post("/health-alerts")
def get_health_alerts(payload: dict):
    return generate_health_alerts(
        user_name=payload["user_name"],
        disease=payload["disease"],
        station_parameters=payload["station_parameters"],
        hourly_data=payload["hourly_data"]
    )
