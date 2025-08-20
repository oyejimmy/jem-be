from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import DATABASE_URL
from app.db.base import Base  # Ensures models are imported


is_sqlite = DATABASE_URL.startswith("sqlite")

engine = create_engine(
	DATABASE_URL,
	connect_args={"check_same_thread": False} if is_sqlite else {},
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
	db = SessionLocal()
	try:
		yield db
	finally:
		db.close()


def init_db() -> None:
	# Importing Base via app.db.base ensures all models are registered
	Base.metadata.create_all(bind=engine)


