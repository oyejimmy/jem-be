from datetime import datetime, timedelta, timezone
from typing import Optional

from jose import jwt
from passlib.context import CryptContext

from app.core.config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES


pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")


def create_access_token(subject: str, expires_delta: Optional[timedelta] = None) -> str:
	if expires_delta is None:
		expires_delta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
	expire = datetime.now(timezone.utc) + expires_delta
	to_encode = {"sub": subject, "exp": expire}
	encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
	return encoded_jwt


def verify_password(plain_password: str, hashed_password: str) -> bool:
	return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
	return pwd_context.hash(password)


