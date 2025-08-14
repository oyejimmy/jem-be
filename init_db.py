from app.database.db import init_db

if __name__ == "__main__":
    init_db()
    print("✅ Database initialized successfully.")
    print("You can now run your application.")