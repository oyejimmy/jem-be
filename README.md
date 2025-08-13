# FastAPI Backend

A backend API built with **FastAPI** and **PostgreSQL**, including JWT-based authentication and database migrations using Alembic.


## 📌 Features

- FastAPI framework
- PostgreSQL database connection
- SQLAlchemy ORM
- Alembic migrations
- JWT authentication
- Modular folder structure


## 📂 Project Structure

app/
├── main.py # Entry point
├── routes/ # API route handlers
├── models/ # SQLAlchemy models
├── schemas/ # Pydantic schemas
├── db/ # Database connection
├── auth/ # Authentication logic
└── init.py
.env # Environment variables

## ⚙️ Installation & Setup

### 1️⃣ Clone the Repository

git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name

### 2️⃣ Create Virtual Environment

python -m venv venv

Activate it:

# Windows

venv\Scripts\activate

# Mac/Linux

source venv/bin/activate

### 3️⃣ Install Dependencies

pip install -r requirements.txt

If `requirements.txt` is not yet generated:
pip install fastapi uvicorn[standard] psycopg2-binary sqlalchemy alembic python-dotenv python-jose passlib[bcrypt] pydantic[email]
pip freeze > requirements.txt

### 4️⃣ Environment Variables

Create a `.env` file in the project root:

DATABASE_URL=postgresql://username:password@localhost:5432/dbname
SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

### 5️⃣ Database Migrations

Initialize Alembic:

alembic init migrations

Generate migration:

alembic revision --autogenerate -m "Initial migration"

Apply migration:

alembic upgrade head

### 6️⃣ Run the Application

uvicorn app.main:app --reload

## 🚀 API Endpoints

### Health Check

**GET** `/`
{
"message": "Hello, FastAPI!"
}

### Example User Endpoint

**GET** `/users`
[
{
"id": 1,
"name": "Jamil"
}
]

## 🛠 Development Notes

- Make sure PostgreSQL is running locally or remotely before starting the app.
- Always activate the virtual environment before running commands.
- Run `pip freeze > requirements.txt` after adding new dependencies.
