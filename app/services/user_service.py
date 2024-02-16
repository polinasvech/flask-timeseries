from datetime import datetime
from typing import List, Optional, Union

from exceptions import UserNotFoundError
from models import CalculationHistory, Session, User
from pydantic import BaseModel


class UserSchema(BaseModel):
    id: int
    username: str
    registration_date: datetime


class HistoryItemSchema(BaseModel):
    time_series: str = None
    date: str = None
    success: bool = False
    anomalies: Optional[dict] = None
    stationarity: Optional[dict] = None
    autocorrelation: Optional[dict] = None
    trends: Optional[dict] = None
    errors: Optional[dict] = None

    def __init__(self, history_item):
        super().__init__()
        self.time_series = str(history_item.dataset_file_name)
        self.date = history_item.calculation_date.strftime("%d/%m/%y %H:%M:%S")
        self.success = history_item.success
        self.anomalies = history_item.result["anomalies"]
        self.stationarity = history_item.result["stationarity"]
        self.autocorrelation = history_item.result["autocorrelation"]
        self.trends = history_item.result["trends"]
        self.errors = history_item.errors


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
            created_at=datetime.datetime.now(),
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
    def user_calc_history(user_id: int = None) -> List[dict]:
        """
        Для получения списка пользователей

        :return: список пользователей
        """
        with Session() as session:
            history_items = session.query(CalculationHistory).filter(CalculationHistory.user_id == user_id).all()

        return [HistoryItemSchema(i).dict() for i in history_items]
