from fastapi import FastAPI

from app.database.init_db import create_db

app = FastAPI()

@app.on_event("startup")
async def startup():
    create_db()

@app.get("/")
async def root():
    return {"message": "Phycus api V.0.0.1"}