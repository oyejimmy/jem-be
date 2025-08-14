from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import Base, Product, Anklet, Bangle, Bracelet, Combo, EarStud, Earing, Hoop, Pendant, Ring, WallFrame

DATABASE_URL = "sqlite:///./test.db"  # or your PostgreSQL URL

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    Base.metadata.create_all(bind=engine)
    print("✅ Database tables created successfully.")
    print("You can now run your application.")
    print("Use 'python -m app.seed_data' to seed the database with initial data.")
    print("Visit http://localhost:8000/docs to access the API documentation.")
    print("Happy coding! 🎉")