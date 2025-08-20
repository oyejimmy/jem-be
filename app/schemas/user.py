from pydantic import BaseModel, EmailStr
from typing import Optional


class UserBase(BaseModel):
	email: EmailStr
	full_name: Optional[str] = None


class UserCreate(UserBase):
	password: str


class UserLogin(BaseModel):
	email: EmailStr
	password: str


class UserOut(UserBase):
	id: int
	is_active: bool
	is_admin: bool

	class Config:
		from_attributes = True


class Token(BaseModel):
	access_token: str
	token_type: str = "bearer"


class ForgotPasswordRequest(BaseModel):
	email: EmailStr


class ResetPasswordRequest(BaseModel):
	token: str
	new_password: str


