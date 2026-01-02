import bcrypt
import random
from database import get_db

# --------------------------
# Kullanıcı Oluşturma
# --------------------------
def create_user(data: dict):
    hashed = bcrypt.hashpw(
        data['sifre'].encode(),
        bcrypt.gensalt()
    ).decode()

    with get_db() as db:
        db.execute(
            "SELECT email FROM kullanicilar WHERE email = ?",
            (data["email"],)
        )
        if db.fetchone():
            raise ValueError("Bu email zaten kayıtlı")

        db.execute("""
            INSERT INTO kullanicilar 
            (isim, email, sifre, dogum_tarihi, cinsiyet, kronik_hastalik, olusturma_tarihi)
            OUTPUT INSERTED.id
            VALUES (?, ?, ?, ?, ?, ?, GETDATE())
        """, (
            data["isim"],
            data["email"],
            hashed,
            data["dogum_tarihi"],
            data["cinsiyet"],
            data["kronik_hastalik"]
        ))

        user_id = db.fetchone()[0]

    return user_id

# --------------------------
# Forget Password - Reset Kodu Oluştur
# --------------------------
def set_reset_code(email: str):
    with get_db() as db:
        user = db.execute(
            "SELECT * FROM kullanicilar WHERE email = ?",
            (email,)
        ).fetchone()
        if not user:
            return None

        # 6 haneli rastgele kod
        code = "".join(random.choices("0123456789", k=6))

        # DB’ye kodu kaydet (reset_expire eklenebilir)
        db.execute(
            "UPDATE kullanicilar SET reset_code = ? WHERE email = ?",
            (code, email)
        )

        print(f"[DEBUG] Reset code for {email}: {code}")  # terminalde göster

        return code

# --------------------------
# Kod Doğrulama
# --------------------------
def verify_reset_code(email: str, code: str):
    with get_db() as db:
        user = db.execute(
            "SELECT reset_code FROM kullanicilar WHERE email = ?",
            (email,)
        ).fetchone()
        return user and user.reset_code == code

# --------------------------
# Şifreyi Güncelleme
# --------------------------
def reset_password(email: str, new_password: str):
    hashed = bcrypt.hashpw(new_password.encode(), bcrypt.gensalt()).decode()
    with get_db() as db:
        db.execute(
            "UPDATE kullanicilar SET sifre = ?, reset_code = NULL WHERE email = ?",
            (hashed, email)
        )
        return True
