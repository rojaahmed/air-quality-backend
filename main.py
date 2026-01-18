from fastapi import FastAPI, HTTPException
from models import KullaniciCreate, LoginRequest
from crud import create_user
from user_service import login_user
from pydantic import BaseModel, EmailStr
import crud
from services.forecast_service import (
    get_7_day_forecast,
    get_7_hour_forecast,
    get_selected_day_next_7_hours,
)
from datetime import date
from services.location_service import find_nearest_station
from fastapi.middleware.cors import CORSMiddleware
from services.clean_route_service import idw_aqi
from services.clean_route_service import find_clean_route
from pydantic import BaseModel
from services.aqi_map_service import get_aqi_map_points
from services.clean_route_service import generate_address_points
from api.alerts import router as alerts_router

app = FastAPI()
app.include_router(alerts_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # sunum için serbest
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/kullanici/")
def add_user(k: KullaniciCreate):
    try:
        user_id = create_user(k.dict())
        return {
            "durum": "Basarili",
            "user_id": user_id
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/login/")
def login(data: LoginRequest):
    return login_user(data)

class ForgetPasswordRequest(BaseModel):
    email: EmailStr

class VerifyCodeRequest(BaseModel):
    email: EmailStr
    code: str

class ResetPasswordRequest(BaseModel):
    email: EmailStr
    new_password: str

@app.post("/forget-password/")
def forget_password(req: ForgetPasswordRequest):
    code = crud.set_reset_code(req.email)
    if not code:
        raise HTTPException(status_code=404, detail="Kullanıcı bulunamadı")
    # Demo için code döndürdük, prod’da mail gönder
    return {"message": "Kod gönderildi", "code": code}

@app.post("/verify-code/")
def verify_code(req: VerifyCodeRequest):
    if crud.verify_reset_code(req.email, req.code):
        return {"message": "Kod doğru"}
    raise HTTPException(status_code=400, detail="Kod yanlış")

@app.post("/reset-password/")
def reset_password(req: ResetPasswordRequest):
    success = crud.reset_password(req.email, req.new_password)
    if not success:
        raise HTTPException(status_code=404, detail="Kullanıcı bulunamadı")
    return {"message": "Şifre başarıyla değiştirildi"}

@app.get("/forecast/daily")
def daily_forecast(station: str = "Gaziantep"):
    data = get_7_day_forecast(station)
    if not data:
        raise HTTPException(status_code=404, detail="Günlük tahmin yok")
    return data


@app.get("/forecast/hourly")
def hourly_forecast(station: str = "Gaziantep"):
    data = get_7_hour_forecast(station)
    if not data:
        raise HTTPException(status_code=404, detail="Saatlik tahmin yok")
    return data

@app.get("/forecast/selected-day-next-7-hours")
def selected_day_next_7_hours(
    selected_date: date,
    station: str = "Gaziantep"
):
    data = get_selected_day_next_7_hours(
        selected_date=selected_date,
        station_name=station
    )

    if not data:
        raise HTTPException(
            status_code=404,
            detail="Seçilen gün için saatlik tahmin yok"
        )

    return data

@app.get("/station/nearest")
def nearest_station(lat: float, lon: float):
    return find_nearest_station(lat, lon)

@app.get("/aqi-at-point")
def aqi_at_point(lat: float, lon: float):
    return {
        "aqi": idw_aqi(lat, lon)
    }

class CleanRouteRequest(BaseModel):
    start_lat: float
    start_lon: float
    end_lat: float
    end_lon: float

@app.post("/clean-route")
def clean_route(req: CleanRouteRequest):
    route = find_clean_route(
        (req.start_lat, req.start_lon),
        (req.end_lat, req.end_lon)
    )
    return {"route": route}

@app.get("/aqi-map")
def aqi_map():
    return get_aqi_map_points()

@app.get("/gaziantep/addresses")
def gaziantep_addresses():
    all_points = []

    for station in stations:
        all_points.extend(generate_address_points(station))

    return all_points