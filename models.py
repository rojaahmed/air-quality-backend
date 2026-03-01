from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import date
from sqlalchemy import Column, Integer, Float, String, Date
from database import Base

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

class GunlukTahminCatboost(Base):
    __tablename__ = "gunluk_tahmin_catboost"

    id = Column(Integer, primary_key=True, index=True)
    istasyon_id = Column(Integer)
    parametre_id = Column(Integer)
    gun = Column(Integer)
    tahmin = Column(Float)
    kategori = Column(String)
    mae = Column(Float)
    mse = Column(Float)
    r2 = Column(Float)
    olusturma_tarihi = Column(Date)
    tahmin_tarihi = Column(Date)