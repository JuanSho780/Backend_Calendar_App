from app.domain.repositories.user_repository import UserRepository
from app.domain.entities.User import User
from app.domain.value_objects.create_user_schema import CreateUserSchema

class UserService:
    def __init__(self, user_repository: UserRepository): # Dependency Injection
        self.user_repository = user_repository

    def login_user(self, username: str, password: str) -> int | None:
        user = self.user_repository.get_user_by_username(username)
        if user and user.password == password:
            return user.id
        return None

    def get_all_users(self) -> list[User]:
        return self.user_repository.get_all_users()

    def get_user_by_id(self, user_id: int) -> User:
        return self.user_repository.get_user_by_id(user_id)

    def create_user(self, user: CreateUserSchema) -> User:
        return self.user_repository.create_user(user)

    def update_user(self, user_id: int, user: User) -> User:
        return self.user_repository.update_user(user_id, user)

    def delete_user(self, user_id: int) -> bool:
        return self.user_repository.delete_user(user_id)