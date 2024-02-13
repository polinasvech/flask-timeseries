from datetime import datetime

from flask_login import UserMixin
from sqlalchemy import (JSON, Boolean, Column, DateTime, ForeignKey, Integer,
                        String, Text, create_engine, event)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

DB_URL = "sqlite:///ts-database.db"
# создание движка БД
engine = create_engine(DB_URL, echo=True)
Base = declarative_base()
Session = sessionmaker(bind=engine)


class User(UserMixin, Base):
    """
    Модель пользователя
    """

    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String(100), unique=True, nullable=False)
    password = Column(String(100), nullable=False)


# Пользователи, которые будут добавлены в таблицу при создании базы
primary_records = [
    {"email": "user1@example.com", "password": "password1"},
    {"email": "user2@example.com", "password": "password2"},
]


# Добавляем listener для отслеживание события создания таблицы пользователей
# если событие произошло - добавляем записи
@event.listens_for(User.__table__, "after_create")
def insert_initial_values(*args, **kwargs):
    with Session() as session:
        for record in primary_records:
            user = User(**record)
            session.add(user)
        session.commit()


class CalculationHistory(Base):
    """
    Модель для хранения истории вычислений
    """

    __tablename__ = "calculation_history"

    id = Column(Integer, primary_key=True)
    dataset_file_name = Column(String(100), nullable=False)
    calculation_date = Column(DateTime, nullable=False, default=datetime.utcnow)
    success = Column(Boolean, nullable=False, default=False)
    result = Column(JSON, nullable=True)
    errors = Column(JSON, nullable=True)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    user = relationship("User", backref="calculation_history")


Base.metadata.create_all(engine)
