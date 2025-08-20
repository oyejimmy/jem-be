from fastapi import Header, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError

from app.core.config import SECRET_KEY, ALGORITHM


def get_current_role(x_role: str | None = Header(None)) -> str:
	if x_role not in {"admin", "customer"}:
		raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid role header")
	return x_role


def require_admin(role: str = Depends(get_current_role)) -> None:
	if role != "admin":
		raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin only")


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


def get_current_user_id(token: str = Depends(oauth2_scheme)) -> int:
	try:
		payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
		user_id = int(payload.get("sub"))
		return user_id
	except (JWTError, ValueError, TypeError):
		raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")


def require_admin_or_header(role: str = Depends(get_current_role), user_id: int = Depends(get_current_user_id)) -> None:
	# Accept either admin header or a valid token; extend to check DB for is_admin if needed
	if role == "admin":
		return
	return

