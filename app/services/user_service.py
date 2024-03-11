from datetime import datetime

from exceptions import UserNotFoundError
from flask import current_app as app
from flask_bcrypt import Bcrypt
from models import CalculationHistory, Session, User
from schemas import HistoryItemSchema, UpdateUserSchema, UserSchema
from sqlalchemy import and_


class UserService:
    @staticmethod
    def create(username: str, password: str) -> User:
        """
        Создание нового пользователя
        """
        bcrypt = Bcrypt(app)
        hashed_pass = bcrypt.generate_password_hash(password).decode("utf-8")
        user = User(
            username=username,
            password=hashed_pass,
        )
        with Session() as session:
            session.add(user)
            session.commit()
        return user

    @classmethod
    def update(cls, user_info: UpdateUserSchema):
        """
        Обновление данных пользователя
        """
        bcrypt = Bcrypt(app)

        user_info = user_info.dict(exclude_none=True)
        if user_info.get("password"):
            hashed_pass = bcrypt.generate_password_hash(user_info.get("password")).decode("utf-8")
            user_info["password"] = hashed_pass

        with Session() as session:
            user = session.query(User).where(User.id == user_info["id"]).first()
            for key, value in user_info.items():
                setattr(user, key, value)
            user.updated_at = datetime.now()
            session.commit()

    @classmethod
    def delete(cls, user_id: int):
        """
        Обновление данных пользователя
        """
        with Session() as session:
            user = session.query(User).where(User.id == user_id).first()
            user.deleted_at = datetime.now()
            session.commit()

    @staticmethod
    def auth(username: str, password: str) -> User | None:
        """
        Для проверки данных пользователя

        :return: True если пароли совпадают
        """
        with Session() as session:
            user = session.query(User).where(and_(User.username == username, User.deleted_at.is_(None))).first()
        if not user:
            raise UserNotFoundError

        bcrypt = Bcrypt(app)
        if bcrypt.check_password_hash(user.password, password):
            return user

    @staticmethod
    def get_user_by_id(user_id: int) -> User:
        """
        Получение пользователя по id
        """
        with Session() as session:
            user = session.query(User).filter(User.id == user_id).first()
        return user

    @staticmethod
    def list_users() -> list[dict]:
        """
        Для получения списка пользователей

        :return: список пользователей
        """
        with Session() as session:
            users = session.query(User).all()
            return [
                UserSchema(
                    id=user.id,
                    username=user.username,
                    registration_date=user.created_at,
                    updated_at=user.updated_at,
                    deleted_at=user.deleted_at,
                ).dict()
                for user in users
            ]

    @staticmethod
    def user_calc_history(user_id: int = None) -> dict:
        """
        Для получения истории вычислений пользователя

        :return: список результатов вычислений пользователя
        """
        with Session() as session:
            username = session.query(User.username).filter(User.id == user_id).scalar()
            history_items = session.query(CalculationHistory).filter(CalculationHistory.user_id == user_id).all()

        result = {
            "user": username,
            "history": [HistoryItemSchema(i).dict() for i in history_items],
            "total": len(history_items),
        }

        return result
