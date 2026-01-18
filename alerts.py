from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any
from services.alert_engine import generate_health_alerts

router = APIRouter()

class HealthAlertRequest(BaseModel):
    user_name: str
    disease: str
    station_parameters: List[str]
    hourly_data: List[Dict[str, Any]]

@router.post("/health-alerts")
def get_health_alerts(req: HealthAlertRequest):
    try:
        return generate_health_alerts(
            user_name=req.user_name,
            disease=req.disease,
            station_parameters=req.station_parameters,
            hourly_data=req.hourly_data
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
