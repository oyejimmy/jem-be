import secrets
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models import User
from app.schemas.user import UserCreate, UserLogin, UserOut, Token, ForgotPasswordRequest, ResetPasswordRequest
from app.core.security import get_password_hash, verify_password, create_access_token


router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/signup", response_model=UserOut)
def signup(user_in: UserCreate, db: Session = Depends(get_db)):
	existing = db.query(User).filter(User.email == user_in.email).first()
	if existing:
		raise HTTPException(status_code=400, detail="Email already registered")
	user = User(
		email=user_in.email,
		full_name=user_in.full_name,
		hashed_password=get_password_hash(user_in.password),
	)
	db.add(user)
	db.commit()
	db.refresh(user)
	return user


@router.post("/login", response_model=Token)
def login(user_in: UserLogin, db: Session = Depends(get_db)):
	user: Optional[User] = db.query(User).filter(User.email == user_in.email).first()
	if not user or not verify_password(user_in.password, user.hashed_password):
		raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
	token = create_access_token(subject=str(user.id))
	return {"access_token": token, "token_type": "bearer"}


@router.post("/forgot-password")
def forgot_password(req: ForgotPasswordRequest, db: Session = Depends(get_db)):
	user: Optional[User] = db.query(User).filter(User.email == req.email).first()
	if not user:
		# Do not reveal if email exists
		return {"message": "If the account exists, a reset link has been sent"}
	user.reset_token = secrets.token_urlsafe(32)
	db.add(user)
	db.commit()
	# In production, send email with the token link
	return {"reset_token": user.reset_token}


@router.post("/reset-password")
def reset_password(req: ResetPasswordRequest, db: Session = Depends(get_db)):
	user: Optional[User] = db.query(User).filter(User.reset_token == req.token).first()
	if not user:
		raise HTTPException(status_code=400, detail="Invalid token")
	user.hashed_password = get_password_hash(req.new_password)
	user.reset_token = None
	db.add(user)
	db.commit()
	return {"message": "Password reset successful"}


