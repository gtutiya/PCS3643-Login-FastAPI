import hashlib, os

def hash_password(password: str) -> str:
    salt = os.urandom(16)
    key = hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 100000)
    return salt.hex() + key.hex()

def verify_password(password_db: str, input_password: str) -> bool:
    salt = bytes.fromhex(password_db[:32])
    key = bytes.fromhex(password_db[32:])
    new_key = hashlib.pbkdf2_hmac('sha256', input_password.encode(), salt, 100000)
    return new_key == key
