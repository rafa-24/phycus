from datetime import UTC, datetime

from sqlmodel import Session, select

from app.modules.users.models.user_model import Users


class UserRepository:

    def create(self, session: Session, user: Users):
        session.add(user)
        session.commit()
        session.refresh(user)

        return user

    def get_user_by_email(self, session: Session, email: str):
        statement = select(Users).where(Users.email == email)
        user = session.exec(statement).first()

        return user

    def update_password_recovery_code(
        self, session: Session, user: Users, code: int
    ):
        user.password_recovery_code = code
        user.updated_at = datetime.now(UTC)
        session.add(user)
        session.commit()
        session.refresh(user)

        return user

    def update_password(self, session: Session, user: Users, hashed_password: str):
        user.password = hashed_password
        user.password_recovery_code = None
        user.updated_at = datetime.now(UTC)
        session.add(user)
        session.commit()
        session.refresh(user)

        return user
