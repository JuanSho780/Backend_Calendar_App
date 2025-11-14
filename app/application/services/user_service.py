from app.domain.repositories.user_repository import UserRepository
from app.domain.apis.mail_sending_api import MailSendingAPI
from app.domain.entities.User import User
from app.domain.value_objects.create_user_schema import CreateUserSchema

from app.authentication.password import verify_password, get_password_hash

class UserService:
    def __init__(self, user_repository: UserRepository, mail_sending_api: MailSendingAPI): # Dependency Injection
        self.user_repository = user_repository
        self.mail_sending_api = mail_sending_api

    def login_user(self, email: str, password: str) -> bool:
        try:
            user = self.user_repository.get_user_by_email(email)
            if user and verify_password(password, user.password):
                verification_code = self.mail_sending_api.send_verification_email(user.email)
                if verification_code is not None:
                    self.user_repository.update_verification_code(user.id, verification_code)
                    return True
        except Exception:
            return False
        return False

    def login_user_verification(self, email: str, verification_code: str) -> int | None:
        user = self.user_repository.get_user_by_email(email)
        db_verification_code = self.user_repository.get_verification_code(user.id)
        response = None
        if db_verification_code == verification_code:
            response = user.id

        self.user_repository.update_verification_code(user.id, None)
        return response

    def get_all_users(self) -> list[User]:
        return self.user_repository.get_all_users()

    def get_user_by_id(self, user_id: int) -> User:
        return self.user_repository.get_user_by_id(user_id)

    def create_user(self, user: CreateUserSchema) -> User:
        user.password = get_password_hash(user.password)
        user_complete = self.user_repository.create_user(user)
        verification_code = self.mail_sending_api.send_verification_email(user_complete.email)

        self.user_repository.update_verification_code(user_complete.id, verification_code)
        return user_complete

    def validate_user_is_verified(self, email: str, verification_code: str) -> bool:
        user = self.user_repository.get_user_by_email(email)
        db_verification_code = self.user_repository.get_verification_code(user.id)

        if db_verification_code == verification_code:
            self.user_repository.update_is_verified(user.id, True)
            self.user_repository.update_verification_code(user.id, None)
            return True
        return False

    def update_user(self, user_id: int, user: CreateUserSchema) -> User:
        return self.user_repository.update_user(user_id, user)

    def delete_user(self, user_id: int) -> bool:
        return self.user_repository.delete_user(user_id)