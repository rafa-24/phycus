from sqlmodel import SQLModel

class UserCreate(SQLModel):
    email: str
    password: str
    first_name: str
    last_name: str
    cellphone: str


class UserResponse(SQLModel):
    id: int
    email: str
    first_name: str
    last_name: str
    cellphone: str