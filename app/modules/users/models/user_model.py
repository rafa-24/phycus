from typing import Optional

from sqlmodel import Field, SQLModel
from datetime import datetime, UTC

class Users(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    email: str = Field(index=True, min_length=3, max_length=50)
    password: str = Field(min_length=8, max_length=50)
    first_name: str = Field(index=True, min_length=3, max_length=50)
    last_name: str = Field(index=True, min_length=3, max_length=50)
    cellphone: str = Field(index=True, min_length=3, max_length=50)
    password_recovery_code: Optional[int] = Field(default=None)

    # campos actualizados por registro
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
