from fastapi import APIRouter
from pydantic import BaseModel
from crud import add_emergency_contact, get_emergency_contacts

router = APIRouter()

class EmergencyContact(BaseModel):
    user_id: int
    name: str
    phone: str
    relation: str


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