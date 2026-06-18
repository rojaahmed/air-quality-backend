from fastapi import WebSocket
import asyncio
import json
from fastapi import FastAPI, HTTPException
from database import get_db
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
from alerts import router as alerts_router
from services.crud import get_station_measurements
from services.aqi_services import compute_station_aqi
from services import emergency_service
from scheduler import start_scheduler
from services.notification_worker import run_notification_job
from services.trend_service import get_station_trend
from services.drift_service import analyze_model_drift
from services.nearby_health_service import get_nearby_health_places
from services.carbon_service import calculate_carbon_footprint
from services.anomaly_service import detect_anomaly
from services.risk_report_service import generate_risk_report
from services.simulation_service import simulate_air_quality
from services.ai_health_report_service import generate_ai_health_report
from services.manual_test_service import analyze_manual_test
app = FastAPI()
@app.on_event("startup")
def start_jobs():
    start_scheduler()
app.include_router(alerts_router)
app.include_router(emergency_service.router)
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

@app.get("/clean-route")
def clean_route(
    start_lat: float,
    start_lon: float,
    end_lat: float,
    end_lon: float
):
    route = find_clean_route(
        (start_lat, start_lon),
        (end_lat, end_lon)
    )
    return {"route": route}

@app.get("/aqi-map")
def aqi_map():
    return get_aqi_map_points()




@app.get("/aqi/{station_id}")
def get_aqi_for_station(station_id: int):
    data = get_station_measurements(station_id)

    aqi_result = compute_station_aqi(data)

    return {
        "station_id": station_id,
        "aqi": aqi_result["station_aqi"],
        "category": aqi_result["category"],
        "pollutants": aqi_result["pollutants"]
    }

class UpdateDeviceRequest(BaseModel):
    user_id: int
    firebase_token: str
    latitude: float
    longitude: float


@app.post("/update-device")
def update_device(data: UpdateDeviceRequest):

    with get_db() as db:

        db.execute("""
            SELECT id FROM kullanicilar
            WHERE id=%s
        """,(data.user_id,))

        user = db.fetchone()

        if not user:
            raise HTTPException(status_code=404, detail="Kullanıcı bulunamadı")

        db.execute("""
            UPDATE kullanicilar
            SET firebase_token=%s,
                latitude=%s,
                longitude=%s
            WHERE id=%s
        """,(
            data.firebase_token,
            data.latitude,
            data.longitude,
            data.user_id
        ))

    return {"status": "ok"}




@app.get("/test-notification")
def test_notification():

    with get_db() as db:
        db.execute("DELETE FROM gonderilen_bildirimler")

    run_notification_job()

    return {"status": "notification job executed"}

@app.get("/trend-analysis-long")
def trend_analysis_long(
    station_id: int,
    parametre_id: int
):

    with get_db() as db:

        db.execute("""
            SELECT tahmin
            FROM gunluk_tahmin_gecmis
            WHERE istasyon_id=%s
            AND parametre_id=%s
            ORDER BY tahmin_tarihi DESC
            LIMIT 30
        """, (station_id, parametre_id))

        rows = db.fetchall()

    values = [float(r[0]) for r in rows if r[0] is not None]

    if not values:
        return {
            "status": "empty",
            "message": "Uzun dönem veri yok",
            "values": []
        }

    values.reverse()

    avg = sum(values) / len(values)
    direction = "rising" if values[-1] > values[0] else "falling"

    return {
        "station_id": station_id,
        "parametre_id": parametre_id,
        "type": "long_term",
        "average": avg,
        "direction": direction,
        "values": values
    }

@app.get("/trend-analysis-by-location-all")
def trend_analysis_by_location_all(
    lat: float,
    lon: float,
    trend_type: str = "daily"
):

    if trend_type not in ["daily", "hourly"]:
        raise HTTPException(
            status_code=400,
            detail="trend_type daily veya hourly olmalı"
        )

    station = find_nearest_station(lat, lon)

    if not station:
        raise HTTPException(status_code=404, detail="İstasyon bulunamadı")

    # 🔥 BURASI KRİTİK: TÜM PARAMETRELER
    PARAMETRELER = [1, 2, 3, 4]  # PM10, PM2.5, NO2, CO (örnek)

    results = []

    for parametre_id in PARAMETRELER:

        trend = get_station_trend(
            station["id"],
            parametre_id,
            trend_type
        )

        results.append({
            "parametre_id": parametre_id,
            "data": trend
        })

    return {
        "station": station,
        "trends": results
    }
@app.websocket("/ws/aqi")
async def websocket_aqi(websocket: WebSocket):

    await websocket.accept()

    lat = float(websocket.query_params.get("lat", 0))
    lon = float(websocket.query_params.get("lon", 0))

    if lat == 0 or lon == 0:
      await websocket.close()
      return

    PARAMETRELER = [1, 2, 3, 4]

    while True:

        station = find_nearest_station(lat, lon)

        results = []

        for parametre_id in PARAMETRELER:

            data = get_station_trend(
                station["id"],
                parametre_id,
                "hourly"
            )

            results.append({
                "parametre_id": parametre_id,
                "data": data
            })

        await websocket.send_text(
    json.dumps({
        "station_id": station["id"],
        "values": results
    })
)

        await asyncio.sleep(10)


import json
import os

@app.get("/shap-data")
def get_shap_data():

    file_path = "data/gunluk_tahmin_catboost.json"

    print("EXISTS:", os.path.exists(file_path))

    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    return data

@app.get("/model-drift")
def get_model_drift():

    result = analyze_model_drift()

    return result

@app.get("/nearby-health")
def nearby_health(lat: float, lon: float):
    try:
        data = get_nearby_health_places(lat, lon)
        return {"results": data}
    except Exception as e:
        print(f"[ENDPOINT] /nearby-health hata: {e}")
        raise HTTPException(status_code=503, detail="Sağlık noktaları şu an alınamıyor")


class CarbonRequest(BaseModel):
    car_km: float
    electricity: float
    flight_hours: float
    meat_meals: float
    public_transport_km: float


@app.post("/carbon-footprint")
def carbon_footprint(data: CarbonRequest):

    result = calculate_carbon_footprint(
        data.car_km,
        data.electricity,
        data.flight_hours,
        data.meat_meals,
        data.public_transport_km
    )

    return result

@app.get("/anomaly-detection")
def anomaly_detection(
    station_id: int,
    parametre_id: int
):

    # =====================================================
    # GEÇMİŞ VERİLER
    # =====================================================

    with get_db() as db:

        db.execute("""
            SELECT tahmin
            FROM saatlik_tahmin_gecmis
            WHERE istasyon_id=%s
            AND parametre_id=%s
            ORDER BY tarih_saat DESC
            LIMIT 48
        """, (
            station_id,
            parametre_id
        ))

        rows = db.fetchall()

    # =====================================================
    # VALUE LIST
    # =====================================================

    values = [
        float(r[0])
        for r in rows
        if r[0] is not None
    ]

    values.reverse()

    # =====================================================
    # ANOMALY DETECTION
    # =====================================================

    result = detect_anomaly(
        values,
        station_id,
        parametre_id
    )

    # =====================================================
    # POLLUTANT NAME
    # =====================================================

    with get_db() as db:

        db.execute("""
            SELECT isim
            FROM parametreler
            WHERE id=%s
        """, (parametre_id,))

        parametre = db.fetchone()

    pollutant_name = (

        parametre[0]

        if parametre

        else "Unknown"

    )

    # =====================================================
    # RESPONSE EXTRA DATA
    # =====================================================

    result["pollutant"] = pollutant_name
    result["station_id"] = station_id
    result["parametre_id"] = parametre_id

    # =====================================================
    # RETURN
    # =====================================================

    return result


@app.get("/risk-report")
def risk_report(
    station: str,
    disease: str
):
    return generate_risk_report(
    station,
    [disease]
)

class SimulationRequest(BaseModel):

    activity: str
    age: int
    disease: str
    aqi: int

@app.post("/air-quality-simulation")
def air_quality_simulation(
        data: SimulationRequest):

    return simulate_air_quality(

        data.activity,
        data.age,
        data.disease,
        data.aqi

    )

@app.get("/ai-health-report")
def ai_health_report(
        station_id: int,
        disease: str,
        user_name: str
):

    return generate_ai_health_report(
        station_id,
        disease,
        user_name
    )


class ManualTestRequest(BaseModel):

    pm10: float
    so2: float
    co: float
    o3: float
    exposure_hours: float
    disease: str

@app.post("/manual-air-quality-test")
def manual_air_quality_test(
        data: ManualTestRequest):

    return analyze_manual_test(
        data.pm10,
        data.so2,
        data.co,
        data.o3,
        data.exposure_hours,
        data.disease
    )