from sqlmodel import SQLModel


class LoginRequest(SQLModel):
    email: str
    password: str


class AuthResponse(SQLModel):
    access_token: str


class PasswordRecoveryRequest(SQLModel):
    email: str


class PasswordRecoveryResponse(SQLModel):
    email: str


class ChangePasswordRequest(SQLModel):
    email: str
    code: int
    password: str


class ChangePasswordResponse(SQLModel):
    email: str
