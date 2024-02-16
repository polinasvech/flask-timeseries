from datetime import datetime
from typing import Optional

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


class CalcHistorySchema(BaseModel):
    user: str
    history: list[HistoryItemSchema] = None
    total: int
