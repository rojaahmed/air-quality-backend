from fastapi import HTTPException
from models import LoginRequest
from database import get_db
import bcrypt
import jwt

SECRET_KEY = "SECRET_KEY"

def login_user(data: LoginRequest):
    with get_db() as db:
        db.execute(
            """
            SELECT
                id,
                isim,
                email,
                sifre,
                kronik_hastalik,
                yas
            FROM kullanicilar
            WHERE email = %s
            """,
            (data.email,)
        )

        user = db.fetchone()

        if not user:
            raise HTTPException(status_code=401, detail="Hatalı bilgiler")

        if not bcrypt.checkpw(
            data.sifre.encode(),
            user[3].encode()
        ):
            raise HTTPException(status_code=401, detail="Hatalı bilgiler")

        token = jwt.encode(
            {"user_id": user[0]},
            SECRET_KEY,
            algorithm="HS256"
        )

        return {
            "token": token,
            "user": {
                "id": user[0],
                "isim": user[1],
                "email": user[2],
                "kronik_hastalik": user[4],
                "yas": user[5]
            }
        }