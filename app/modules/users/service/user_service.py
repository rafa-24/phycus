from sqlmodel import Session

from app.modules.users.schema.user_schema import UserCreate, UserResponse
from app.modules.users.models.user_model import Users
from app.modules.users.repository.user_repository import UserRepository
from app.modules.auth.utils.password import hash_password

from app.modules.shared.schemas.api_response import ApiResponse
from app.modules.email.service.email_service import EmailService
from app.modules.shared.exceptions.app_exceptions import (
    ConflictException,
    InternalServerException,
)

class UserService:

    def __init__(self):
        self.user_repository = UserRepository()
        self.email_service = EmailService()

    def create(self, session: Session, user: UserCreate):

        existing_user = self.user_repository.get_user_by_email(session, user.email)

        if existing_user:
            raise ConflictException("El correo ya esta registrado.")
        
        # Instanciar nuevo usuario
        new_user = Users(
            email= user.email,
            password= hash_password(user.password),
            first_name= user.first_name,
            last_name= user.last_name,
            cellphone= user.cellphone
        )

        # Guardar en la db
        created_user = self.user_repository.create(session, new_user)

        # verificar si el usuario se creo
        if created_user.id is None:
            raise InternalServerException("No fue posible crear usuario")
        
        # enviar email
        html = self.email_service.render_template(
            "welcome.html",
            {"name": created_user.first_name}
        )

        self.email_service.send_email(
            to_email= created_user.email,
            subject= "Bienvenido a phycus",
            html_content= html
        )

        return ApiResponse(
            message= "Su registro se completo de manera exitosa.",
            data= UserResponse.model_validate(created_user)
        )
    
