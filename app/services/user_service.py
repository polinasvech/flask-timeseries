from typing import Optional

from models import CalculationHistory, Session, User
from pydantic import BaseModel
from utils import UserNotFoundError


class UserSchema(BaseModel):
    id: int
    email: str


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
    def get_user_by_id(user_id):
        """
        Получение пользователя по id
        """
        with Session() as session:
            user = session.query(User).filter(User.id == user_id).first()
        return user

    @staticmethod
    def get_user_by_email(email):
        """
        Получение пользователя по email
        """
        with Session() as session:
            user = session.query(User).filter(User.email == email).first()
        return user

    @staticmethod
    def auth_user(user, password):
        """
        Для проверки данных пользователя

        :return: True если пароли совпадают
        """
        if user.password == password:
            return True
        return False

    @staticmethod
    def list_users():
        """
        Для получения списка пользователей

        :return: список пользователей
        """
        with Session() as session:
            users = session.query(User).all()
            return [UserSchema(id=user.id, email=user.email).dict() for user in users]

    @staticmethod
    def user_calc_history(user_id: int = None):
        """
        Для получения списка пользователей

        :return: список пользователей
        """
        with Session() as session:
            history_items = session.query(CalculationHistory).filter(CalculationHistory.user_id == user_id).all()

        return [HistoryItemSchema(i).dict() for i in history_items]
