# app/scripts/create_user.py
from app.database import db_session
from app.models import Users
from app.security import hash_password
import pyotp

def main():
    login = input("Login: ").strip()
    email = input("Email (opcional): ").strip() or None
    senha_plana = input("Senha: ").strip()

    senha_hash = hash_password(senha_plana)
    secret = pyotp.random_base32()
    print(f"TOTP secret para configurar no app autenticador: {secret}")

    u = Users(login=login, senha=senha_hash, email=email, UID=login, totp_secret=secret)
    db_session.add(u)
    db_session.commit()
    print("Usuário criado com sucesso.")

if __name__ == "__main__":
    main()
