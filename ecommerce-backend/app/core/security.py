from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import jwt

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

def hash_password(password: str) -> str:
    password = password[:72]  # argon2 limit
    return pwd_context.hash(password)

def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)

def create_access_token(subject: str, role: str, SECRET_KEY: str, ALGORITHM: str, expires_minutes: int):
    expire = datetime.utcnow() + timedelta(minutes=expires_minutes)
    to_encode = {
        "exp": expire,
        "sub": subject,
        "role": role  # ← هنا نمرر الدور (admin أو user)
    }
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def decode_token(token: str, SECRET_KEY: str, ALGORITHMS: list):
    return jwt.decode(token, SECRET_KEY, algorithms=ALGORITHMS)
