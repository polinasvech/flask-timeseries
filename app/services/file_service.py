import os
import re

import pandas as pd
from flask import current_app as app
from utils import FileExtensionError, NotTimeSeriesError
from werkzeug.datastructures.file_storage import FileStorage


class FileService:
    @classmethod
    def save_file(cls, uploaded_file: FileStorage) -> str:
        if not re.search(r"\.csv$", uploaded_file.filename):
            # если загрузили файл не .csv формата, возвращаем ошибку
            raise FileExtensionError(uploaded_file.filename)

        datasets_folder = f"{os.path.dirname(os.path.dirname(__file__))}{app.config['FILE_UPLOAD_FOLDER']}"
        if not os.path.exists(datasets_folder):
            os.mkdir(datasets_folder)

        new_df = pd.read_csv(uploaded_file)
        # тк анализируем временные ряды, если в первой колонке НЕ даты - ошибка
        pattern = re.compile(r"(?i:date(time)?)")
        if not re.match(pattern, new_df.columns[0]):
            raise NotTimeSeriesError

        new_df.to_csv(f"{datasets_folder}/{uploaded_file.filename}")
        # обновление списка доступных датасетов
        cls.list_datasets()

        return uploaded_file.filename

    @staticmethod
    def list_datasets():
        """Для перечисления возможных для анализа датасетов"""
        from swagger_schemas import ANALYZE_DATASET

        datasets_folder = f"{os.path.dirname(os.path.dirname(__file__))}{app.config['FILE_UPLOAD_FOLDER']}"
        ANALYZE_DATASET["parameters"][0]["enum"] = os.listdir(datasets_folder)
