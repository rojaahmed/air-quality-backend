from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import date



class KullaniciCreate(BaseModel):
    isim: str
    email: EmailStr
    sifre: str
    dogum_tarihi: date
    cinsiyet: str
    kronik_hastalik: Optional[str] = "Yok"

class LoginRequest(BaseModel):
    email: EmailStr
    sifre: str

