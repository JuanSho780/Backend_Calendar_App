from app.domain.repositories.user_repository import UserRepository
from app.domain.entities.User import User
from typing import List, Optional
from app.domain.value_objects.create_user_schema import CreateUserSchema
from app.infrastructure.database.db_connection_factory import DBConnectionFactory # for db connection

class UserRepositoryImpl(UserRepository):
    list_users: List[User] = []
    count_id: int = 0

    def get_user_by_username(self, username: str) -> Optional[User]:
        for user in UserRepositoryImpl.list_users:
            if user.name == username:
                return user

    def get_all_users(self) -> List[User]:
        return UserRepositoryImpl.list_users

    def get_user_by_id(self, user_id: int) -> Optional[User]:
        for user in UserRepositoryImpl.list_users:
            if user.id == user_id:
                return user

    def create_user(self, user: CreateUserSchema) -> User:
        new_user = User(
            id=UserRepositoryImpl.count_id,
            name=user.name,
            email=user.email,
            password=user.password
        )
        UserRepositoryImpl.list_users.append(new_user)
        UserRepositoryImpl.count_id += 1
        return new_user

    def update_user(self, user_id: int, user: User) -> Optional[User]:
        for i, u in enumerate(UserRepositoryImpl.list_users):
            if u.id == user_id:
                UserRepositoryImpl.list_users[i] = user
                return user
        return None

    def delete_user(self, user_id: int) -> bool:
        for i, u in enumerate(UserRepositoryImpl.list_users):
            if u.id == user_id:
                del UserRepositoryImpl.list_users[i]
                return True
        return False