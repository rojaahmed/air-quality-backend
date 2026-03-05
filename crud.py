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
        # Email kontrol
        db.execute(
            "SELECT 1 FROM kullanicilar WHERE email = %s",
            (data["email"],)
        )
        if db.fetchone():
            raise ValueError("Bu email zaten kayıtlı")

        # Kullanıcı ekleme
        db.execute("""
            INSERT INTO kullanicilar 
            (isim, email, sifre, dogum_tarihi, cinsiyet, kronik_hastalik, olusturma_tarihi)
            VALUES (%s, %s, %s, %s, %s, %s, CURRENT_TIMESTAMP)
            RETURNING id
        """, (
            data["isim"],
            data["email"],
            hashed,
            data["dogum_tarihi"],
            data.get("cinsiyet"),
            data.get("kronik_hastalik")
        ))

        user_id = db.fetchone()[0]  # 👈 MUTLAKA with İÇİNDE

    return user_id


# --------------------------
# Forget Password - Reset Kodu Oluştur
# --------------------------
def set_reset_code(email: str):
    with get_db() as db:
        db.execute(
            "SELECT id FROM kullanicilar WHERE email = %s",
            (email,)
        )
        user = db.fetchone()
        if not user:
            return None

        code = "".join(random.choices("0123456789", k=6))

        db.execute(
            "UPDATE kullanicilar SET reset_code = %s WHERE email = %s",
            (code, email)
        )

        print(f"[DEBUG] Reset code for {email}: {code}")
        return code


# --------------------------
# Kod Doğrulama
# --------------------------
def verify_reset_code(email: str, code: str):
    with get_db() as db:
        db.execute(
            "SELECT reset_code FROM kullanicilar WHERE email = %s",
            (email,)
        )
        user = db.fetchone()
        return user is not None and user[0] == code


# --------------------------
# Şifreyi Güncelleme
# --------------------------
def reset_password(email: str, new_password: str):
    hashed = bcrypt.hashpw(new_password.encode(), bcrypt.gensalt()).decode()
    with get_db() as db:
        db.execute(
            "UPDATE kullanicilar SET sifre = %s, reset_code = NULL WHERE email = %s",
            (hashed, email)
        )
    return True

# --------------------------
# Acil İletişim Ekle
# --------------------------
def add_emergency_contact(user_id: int, data: dict):

    with get_db() as db:

        db.execute("""
            INSERT INTO acil_iletisimler
            (kullanici_id, ad_soyad, telefon, yakinlik)
            VALUES (%s,%s,%s,%s)
        """,(
            user_id,
            data["name"],
            data["phone"],
            data["relation"]
        ))

    return True

    # --------------------------
# Kullanıcının Acil Kişileri
# --------------------------
def get_emergency_contacts(user_id:int):

    with get_db() as db:

        db.execute("""
            SELECT id, ad_soyad, telefon, yakinlik
            FROM acil_iletisimler
            WHERE kullanici_id = %s
        """,(user_id,))

        rows = db.fetchall()

    contacts = []

    for r in rows:
        contacts.append({
            "id": r[0],
            "name": r[1],
            "phone": r[2],
            "relation": r[3]
        })

    return contacts