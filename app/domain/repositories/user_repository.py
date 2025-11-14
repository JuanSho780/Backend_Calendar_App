from abc import ABC, abstractmethod
from typing import List, Optional
from app.domain.entities.User import User
from app.domain.value_objects.create_user_schema import CreateUserSchema

class UserRepository(ABC):

    @abstractmethod
    def get_user_by_email(self, email: str) -> Optional[User]:
        pass

    @abstractmethod
    def get_user_by_username(self, username: str) -> Optional[User]:
        pass

    @abstractmethod
    def get_all_users(self) -> List[User]:
        pass

    @abstractmethod
    def get_user_by_id(self, user_id: int) -> Optional[User]:
        pass

    @abstractmethod
    def create_user(self, user: CreateUserSchema) -> User:
        pass

    @abstractmethod
    def get_verification_code(self, user_id: int) -> Optional[str]:
        pass

    @abstractmethod
    def update_verification_code(self, user_id: int, verification_code: str | None) -> None:
        pass

    @abstractmethod
    def update_is_verified(self, user_id: int, is_verified: bool) -> None:
        pass

    @abstractmethod
    def update_user(self, user_id: int, user: User) -> Optional[User]: #in update we can use CreateUserSchema
        pass

    @abstractmethod
    def delete_user(self, user_id: int) -> bool:
        pass