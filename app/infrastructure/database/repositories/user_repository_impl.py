from app.domain.repositories.user_repository import UserRepository
from app.domain.entities.User import User
from typing import List, Optional
from app.domain.value_objects.create_user_schema import CreateUserSchema
from app.infrastructure.database.db_connection_factory import DBConnectionFactory # for db connection
from fastapi import HTTPException

class UserRepositoryImpl(UserRepository):

    def get_user_by_username(self, username: str) -> Optional[User]:
        connection = DBConnectionFactory.get_connection()

        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT id, name, email, password, is_verified FROM users WHERE name = %s", (username,))
                user_data = cursor.fetchone()
                if user_data:
                    return User(
                        id=user_data[0],
                        name=user_data[1],
                        email=user_data[2],
                        password=user_data[3],
                        is_verified=user_data[4]
                    )
                else:
                    raise HTTPException(status_code=404, detail="User not found")
        finally:
            DBConnectionFactory.release_connection(connection)

    def get_all_users(self) -> List[User]:
        connection = DBConnectionFactory.get_connection()

        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT id, name, email, password, is_verified FROM users")
                users_data = cursor.fetchall()
                return [
                    User(
                        id=user[0],
                        name=user[1],
                        email=user[2],
                        password=user[3],
                        is_verified=user[4]
                    ) for user in users_data
                ]
        finally:
            DBConnectionFactory.release_connection(connection)

    def get_user_by_id(self, user_id: int) -> Optional[User]:
        connection = DBConnectionFactory.get_connection()

        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT id, name, email, password, is_verified FROM users WHERE id = %s", (user_id,))
                user_data = cursor.fetchone()
                if user_data:
                    return User(
                        id=user_data[0],
                        name=user_data[1],
                        email=user_data[2],
                        password=user_data[3],
                        is_verified=user_data[4]
                    )
                else:
                    raise HTTPException(status_code=404, detail="User not found")
        finally:
            DBConnectionFactory.release_connection(connection)

    def create_user(self, user: CreateUserSchema) -> User:
        connection = DBConnectionFactory.get_connection()

        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO users (name, email, password) VALUES (%s, %s, %s) RETURNING id",
                    (user.name, user.email, user.password)
                )
                user_id = cursor.fetchone()[0]
                connection.commit()
                return User(
                    id=user_id,
                    name=user.name,
                    email=user.email,
                    password=user.password,
                    is_verified=False
                )
        finally:
            DBConnectionFactory.release_connection(connection)

    def get_verification_code(self, user_id: int) -> Optional[str]:
        connection = DBConnectionFactory.get_connection()

        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT now_verification_code FROM users WHERE id = %s",
                    (user_id,)
                )
                result = cursor.fetchone()
                if result:
                    return result[0]
                return None
        finally:
            DBConnectionFactory.release_connection(connection)

    def update_verification_code(self, user_id: int, verification_code: str | None) -> None:
        connection = DBConnectionFactory.get_connection()

        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    "UPDATE users SET now_verification_code = %s WHERE id = %s",
                    (verification_code, user_id)
                )
                connection.commit()
        finally:
            DBConnectionFactory.release_connection(connection)

    def update_is_verified(self, user_id: int, is_verified: bool) -> None:
        connection = DBConnectionFactory.get_connection()

        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    "UPDATE users SET is_verified = %s WHERE id = %s",
                    (is_verified, user_id)
                )
                connection.commit()
        finally:
            DBConnectionFactory.release_connection(connection)

    def update_user(self, user_id: int, user: User) -> Optional[User]:
        connection = DBConnectionFactory.get_connection()

        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    "UPDATE users SET name = %s, email = %s, password = %s WHERE id = %s",
                    (user.name, user.email, user.password, user_id)
                )
                connection.commit()
                return user
        finally:
            DBConnectionFactory.release_connection(connection)

    def delete_user(self, user_id: int) -> bool:
        connection = DBConnectionFactory.get_connection()

        try:
            with connection.cursor() as cursor:
                cursor.execute("DELETE FROM users WHERE id = %s", (user_id,))
                connection.commit()
                return cursor.rowcount > 0
        finally:
            DBConnectionFactory.release_connection(connection)
