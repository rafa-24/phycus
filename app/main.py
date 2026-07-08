from fastapi import FastAPI
from app.database.init_db import create_db
from app.modules.users.controller.user_controller import user
from app.modules.auth.controller.auth_controller import auth
from app.modules.shared.exceptions.exception_handlers import register_exception_handlers

app = FastAPI()

register_exception_handlers(app)

@app.on_event("startup")
async def startup():
    create_db()

@app.get("/")
async def root():
    return {"message": "Phycus api V.0.0.1"}

# incluir rutas en mi aplicacion

app.include_router(user)
app.include_router(auth)