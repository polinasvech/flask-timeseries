import datetime
import os.path

import numpy as np
import pandas as pd
from flask import current_app as app
from models import CalculationHistory, Session
from utils import DatasetNotFoundError, EmptyFileError


class AnalyzeService:
    def __init__(self, filename: str, user_id: str):
        self._errors = {}
        self._user_id = user_id

        datasets_folder = f"{os.path.dirname(os.path.dirname(__file__))}{app.config['FILE_UPLOAD_FOLDER']}"
        if not os.path.exists(datasets_folder):
            os.mkdir(datasets_folder)

        if not os.path.isfile(f"{datasets_folder}/{filename}"):
            raise DatasetNotFoundError(datasets_folder)

        try:
            self._df = pd.read_csv(f"{datasets_folder}/{filename}")
        except pd.errors.EmptyDataError:
            raise EmptyFileError

        self._filename = filename

        # переводим даты в формат datetime
        date_column = self._df.columns[0]
        self._df[date_column] = pd.to_datetime(self._df[date_column])
        # устанавливаем дату в качестве индекса
        self._df.set_index(date_column, inplace=True)
        try:
            # устанавливаем периодичность наблюдений - день
            self._df.index.freq = "D"
        except ValueError as e:
            self._errors["preprocess"] = str(e)

        # удаляем строки с пропущенными значениями
        self._df = self._df.dropna()

        # находим столбцы с числовыми значениями - они пригодны для анализа
        self._numeric_columns = []
        for col_name, col_type in zip(self._df.columns, self._df.dtypes):
            if col_type in [np.float64, np.int64]:
                self._numeric_columns.append(col_name)

        self.__stationarity_info = {}
        self.__anomalies_info = {}
        self.__autocorr_info = {}
        self.__trend_info = {"linear": {}, "seasonal": {}}

    def check_stationarity(self):
        """
        Cтационарный ряд — это ряд, в котором статистические характеристики, такие как среднее и дисперсия,
        остаются постоянными во времени. Позволяет строить надежные модели и прогнозировать будущие значения.

        Для проверки использован тест Дики-Фуллера (DF-тест, Dickey-Fuller test)
        """
        from statsmodels.tsa.stattools import adfuller

        # проверяем на стационарность все числовые столбцы (кроме даты и погоды)
        for col in self._numeric_columns:
            result = adfuller(self._df[col])
            pvalue = result[1]
            # Если p-значение меньше уровня значимости (0.05) => отклоняем нулевую гипотезу о нестационарности ряда
            # => ряд можно считать стационарным.
            self.__stationarity_info[col] = True if pvalue < 0.05 else False

    def check_anomalies(self):
        """
        Выявление аномальных наблюдений

        Аномальными считаются наблюдения, не попадающие в интервал
        среднее +- 2 стандартных отклонения
        """
        for col in self._numeric_columns:
            col_mean = np.mean(self._df[col])
            col_std = np.std(self._df[col])

            # в качестве интервала выбираем +- 2 стандартных отклонения
            lower_bound = col_mean - 2 * col_std
            upper_bound = col_mean + 2 * col_std

            # определяем аномалию как значение, выходящие за границы инвервала
            anomalies = self._df[(self._df[col] < lower_bound) | (self._df[col] > upper_bound)]
            self.__anomalies_info[col] = anomalies.count()[col].item()

    def check_autocorrelation(self):
        """
        Автокорреляция - это корреляция между значениями временного ряда в разные моменты времени.
        Помогает определить, насколько значения временного ряда зависят от его предыдущих значений.

        Для проверки использован критерий Дарбина—Уотсона  (Durbin-Watson test)
        """
        from statsmodels.stats.stattools import durbin_watson

        for col in self._numeric_columns:
            residuals = self._df[col] - self._df[col].mean()  # разность между соседними значениями
            dw_statistic = durbin_watson(residuals)
            self.__autocorr_info[col] = True if dw_statistic < 1.5 or dw_statistic > 2.5 else False

    def check_linear_trend(self):
        """
        Проверка на наличие линейного тренда
        """
        import statsmodels.api as sm

        x = np.arange(len(self._df))
        x = sm.add_constant(x)

        for col in self._numeric_columns:
            y = self._df[col]
            model = sm.OLS(y, x).fit()
            trend_coeff = model.params.iloc[1]

            if trend_coeff > 0:
                self.__trend_info["linear"][col] = (True, "positive", trend_coeff.item())
            elif trend_coeff < 0:
                self.__trend_info["linear"][col] = (True, "negative", trend_coeff.item())
            else:
                self.__trend_info["linear"][col] = False

    def check_seasonal_trend(self):
        """
        Провека на наличие сезонного тренда
        """
        from statsmodels.tsa.seasonal import seasonal_decompose

        # Используем сезонную декомпозицию для проверки наличия тренда
        for col in self._numeric_columns:
            result = seasonal_decompose(self._df[col], model="additive")
            self.__trend_info["seasonal"][col] = True if result.resid.isnull().any() else False

    def analyze(self):
        try:
            self.check_anomalies()  # поиск аномальных значений
        except Exception as e:
            self._errors["anomalies_check"] = str(e)

        try:
            self.check_stationarity()  # проверка на стационарность
        except Exception as e:
            self._errors["stationarity_check"] = str(e)

        try:
            self.check_autocorrelation()  # проверяем наличие автокорреляции
        except Exception as e:
            self._errors["autocorrelation_check"] = str(e)

        # проверяем наличие трендов
        try:
            self.check_linear_trend()
        except Exception as e:
            self._errors["trends_check"] = {}
            self._errors["trends_check"]["linear"] = str(e)

        try:
            self.check_seasonal_trend()
        except Exception as e:
            self._errors["trends_check"] = (
                {} if "trends_check" not in self._errors.keys() else self._errors["trends_check"]
            )
            self._errors["trends_check"]["seasonal"] = str(e)

        result = {
            "success": True if not self._errors else False,
            "anomalies": self.__anomalies_info,
            "stationarity": self.__stationarity_info,
            "autocorrelation": self.__autocorr_info,
            "trends": self.__trend_info,
            "errors": self._errors,
        }

        calc_history = CalculationHistory(
            user_id=self._user_id,
            dataset_file_name=self._filename,
            calculation_date=datetime.datetime.now(),
            success=True if not self._errors else False,
            result=result,
            errors=self._errors,
        )

        with Session() as session:
            session.add(calc_history)
            session.commit()

        return result
