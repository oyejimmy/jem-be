from fastapi import FastAPI
from app.database.db import init_db
from app.routes.jewelry import jewelry_router

init_db()
app = FastAPI()
app.include_router(jewelry_router)
