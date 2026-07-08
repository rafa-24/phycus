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
    
    
