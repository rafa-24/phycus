from sqlmodel import Session

from app.modules.auth.schema.auth_schema import (
    AuthResponse,
    ChangePasswordRequest,
    ChangePasswordResponse,
    LoginRequest,
    PasswordRecoveryRequest,
    PasswordRecoveryResponse,
)
from app.modules.auth.utils.jwt import create_access_token
from app.modules.auth.utils.password import hash_password, verify_password
from app.modules.auth.utils.recovery_code import generate_recovery_code
from app.modules.email.service.email_service import EmailService
from app.modules.shared.schemas.api_response import ApiResponse
from app.modules.shared.exceptions.app_exceptions import (
    BadRequestException,
    NotFoundException,
    UnauthorizedException,
)
from app.modules.users.repository.user_repository import UserRepository


class AuthService:

    def __init__(self):
        self.user_repository = UserRepository()
        self.email_service = EmailService()

    def login(self, session: Session, credentials: LoginRequest):
        user = self.user_repository.get_user_by_email(session, credentials.email)

        if not user or not verify_password(credentials.password, user.password):
            raise UnauthorizedException("Correo o contraseña incorrectos.")

        access_token = create_access_token(
            {"sub": str(user.id), "email": user.email}
        )

        return ApiResponse(
            message="Inicio de sesión exitoso.",
            data=AuthResponse(access_token=access_token),
        )

    def request_password_recovery(
        self, session: Session, payload: PasswordRecoveryRequest
    ):
        user = self.user_repository.get_user_by_email(session, payload.email)

        if not user:
            raise NotFoundException(
                "No existe un usuario registrado con ese correo electrónico."
            )

        recovery_code = generate_recovery_code()

        self.user_repository.update_password_recovery_code(
            session, user, recovery_code
        )

        html = self.email_service.render_template(
            "password_recovery.html",
            {"name": user.first_name, "code": recovery_code},
        )

        self.email_service.send_email(
            to_email=user.email,
            subject="Código de recuperación de contraseña - Phycus",
            html_content=html,
        )

        return ApiResponse(
            message="Se ha enviado un código de recuperación a su correo electrónico.",
            data=PasswordRecoveryResponse(email=user.email),
        )

    def change_password(self, session: Session, payload: ChangePasswordRequest):
        user = self.user_repository.get_user_by_email(session, payload.email)

        if not user:
            raise NotFoundException(
                "No existe un usuario registrado con ese correo electrónico."
            )

        if user.password_recovery_code is None:
            raise BadRequestException(
                "No hay un código de recuperación activo para este usuario."
            )

        if user.password_recovery_code != payload.code:
            raise BadRequestException("El código de verificación es incorrecto.")

        hashed_password = hash_password(payload.password)

        self.user_repository.update_password(session, user, hashed_password)

        return ApiResponse(
            message="Contraseña actualizada de manera exitosa.",
            data=ChangePasswordResponse(email=user.email),
        )