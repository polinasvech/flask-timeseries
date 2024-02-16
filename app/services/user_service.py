from datetime import datetime
from typing import List, Union

from exceptions import UserNotFoundError
from models import CalculationHistory, Session, User
from schemas import UserSchema, HistoryItemSchema


class UserService:
    @staticmethod
    def create(username, password) -> User:
        """
        Создание нового пользователя
        """
        from bcrypt_settings import bcrypt

        hashed_pass = bcrypt.generate_password_hash(password).decode("utf-8")
        user = User(
            username=username,
            password=hashed_pass,
            created_at=datetime.now(),
        )
        with Session() as session:
            session.add(user)
            session.commit()
        return user

    @staticmethod
    def get_user_by_id(user_id) -> User:
        """
        Получение пользователя по id
        """
        with Session() as session:
            user = session.query(User).filter(User.id == user_id).first()
        return user

    @staticmethod
    def auth_user(username, password) -> Union[User, None]:
        """
        Для проверки данных пользователя

        :return: True если пароли совпадают
        """
        from bcrypt_settings import bcrypt

        with Session() as session:
            user = session.query(User).filter(User.username == username).first()
        if not user:
            raise UserNotFoundError

        if bcrypt.check_password_hash(user.password, password):
            return user

    @staticmethod
    def list_users() -> List[dict]:
        """
        Для получения списка пользователей

        :return: список пользователей
        """
        with Session() as session:
            users = session.query(User).all()
            return [
                UserSchema(id=user.id, username=user.username, registration_date=user.created_at).dict()
                for user in users
            ]

    @staticmethod
    def user_calc_history(user_id: int = None) -> dict:
        """
        Для получения истории вычислений пользователя

        :return: список пользователей
        """
        with Session() as session:
            username = session.query(User.username).filter(User.id == user_id).scalar()
            history_items = session.query(CalculationHistory).filter(CalculationHistory.user_id == user_id).all()

        result = {
            "user": username,
            "history": [HistoryItemSchema(i).dict() for i in history_items],
            "total": len(history_items)
        }

        return result
