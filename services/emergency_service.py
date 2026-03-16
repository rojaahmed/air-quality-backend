from fastapi import APIRouter
from pydantic import BaseModel
from crud import add_emergency_contact, get_emergency_contacts
from database import get_db
from services.notification_service import send_notification

router = APIRouter()

# -----------------------
# MODELLER
# -----------------------

class EmergencyContact(BaseModel):
    user_id: int
    name: str
    phone: str
    relation: str
    firebase_token: str


class EmergencyRequest(BaseModel):
    user_id: int
    lat: float
    lon: float


# -----------------------
# Acil kişi ekleme
# -----------------------

@router.post("/add_emergency")
def add_contact(data: EmergencyContact):

    add_emergency_contact(data.user_id, data.dict())

    return {"status": "ok"}


# -----------------------
# Acil kişileri getir
# -----------------------

@router.get("/get_emergency/{user_id}")
def get_contacts(user_id: int):

    contacts = get_emergency_contacts(user_id)

    return contacts


# -----------------------
# SOS gönder
# -----------------------

@router.post("/send_emergency")
def send_emergency(data: EmergencyRequest):

    with get_db() as db:

        db.execute("""
            SELECT firebase_token
            FROM acil_iletisimler
            WHERE kullanici_id = %s
        """, (data.user_id,))

        rows = db.fetchall()

    # Google maps linki oluştur
    map_link = f"https://maps.google.com/?q={data.lat},{data.lon}"

    # Tüm acil kişilere bildirim gönder
    for r in rows:

        token = r[0]

        if token:
            send_notification(
                token,
                "🚨 ACİL DURUM",
                f"Kullanıcı yardım istiyor\nKonum: {map_link}"
            )

    return {"status": "sent"}