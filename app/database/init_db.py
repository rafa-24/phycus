from sqlmodel import SQLModel
from .database import engine

# Importar TODOS los modelos
#from app.modules.users.model import User


def create_db():
    SQLModel.metadata.create_all(engine)
    print("Base de datos creada correctamente.")