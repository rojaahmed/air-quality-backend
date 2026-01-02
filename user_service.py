from fastapi import HTTPException
from models import LoginRequest
from database import get_db
import bcrypt
import jwt

SECRET_KEY = "SECRET_KEY"  # ⚠️ Prod ortamında güvenli tut

def login_user(data: LoginRequest):
    with get_db() as db:
        db.execute(
            "SELECT * FROM kullanicilar WHERE email = %s",
            (data.email,)
        )
        user = db.fetchone()

        if not user:
            raise HTTPException(status_code=401, detail="Hatalı bilgiler")

        if not bcrypt.checkpw(
            data.sifre.encode(),
            user['sifre'].encode()
        ):
            raise HTTPException(status_code=401, detail="Hatalı bilgiler")

        token = jwt.encode(
            {"user_id": user['id']},
            SECRET_KEY,
            algorithm="HS256"
        )

        return {
            "token": token,
            "user": {
                "id": user['id'],
                "isim": user['isim'],
                "email": user['email'],
                "kronik_hastalik": user['kronik_hastalik']
            }
        }
