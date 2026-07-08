from fastapi import FastAPI
from app.database.init_db import create_db
from app.modules.users.controller.user_controller import user

app = FastAPI()

@app.on_event("startup")
async def startup():
    create_db()

@app.get("/")
async def root():
    return {"message": "Phycus api V.0.0.1"}

# incluir rutas en mi aplicacion

app.include_router(user)