from sqlalchemy import Column, Integer, String, Boolean

from app.db.base_class import Base


class User(Base):
	__tablename__ = "users"
	id = Column(Integer, primary_key=True, index=True)
	email = Column(String, unique=True, index=True, nullable=False)
	full_name = Column(String, nullable=True)
	hashed_password = Column(String, nullable=False)
	is_active = Column(Boolean, default=True)
	is_admin = Column(Boolean, default=False)
	reset_token = Column(String, nullable=True, index=True)


