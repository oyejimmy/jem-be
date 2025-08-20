import os


DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./test.db")

# Auth/JWT
SECRET_KEY = os.getenv("SECRET_KEY", "change_me_in_production")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60"))


