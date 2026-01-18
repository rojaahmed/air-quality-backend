from fastapi import APIRouter
from pydantic import BaseModel
from services.alert_engine import generate_daily_health_alerts

router = APIRouter()

class HealthAlertRequest(BaseModel):
    user_name: str
    disease: str
    hourly_data: list


@router.post("/health-alerts")
def health_alerts(req: HealthAlertRequest):
    return generate_daily_health_alerts(
        req.user_name,
        req.disease,
        req.hourly_data
    )
