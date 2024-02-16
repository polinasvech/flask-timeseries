import os
import re

import pandas as pd
from exceptions import FileExtensionError, NotTimeSeriesError
from flask import current_app as app
from werkzeug.datastructures.file_storage import FileStorage


class FileService:
    @classmethod
    def save_file(cls, uploaded_file: FileStorage) -> str:
        if not re.search(r"\.csv$", uploaded_file.filename):
            # если загрузили файл не .csv формата, возвращаем ошибку
            raise FileExtensionError(uploaded_file.filename)

        datasets_folder = cls.get_folder()

        new_df = pd.read_csv(uploaded_file)
        # тк анализируем временные ряды, если в первой колонке НЕ даты - ошибка
        pattern = re.compile(r"(?i:date(time)?)")
        if not re.match(pattern, new_df.columns[0]):
            raise NotTimeSeriesError

        new_df.to_csv(f"{datasets_folder}/{uploaded_file.filename}")
        # обновление списка доступных датасетов
        cls.list_datasets()

        return uploaded_file.filename

    @classmethod
    def list_datasets(cls):
        """Для перечисления возможных для анализа датасетов"""
        from swagger_schemas import ANALYZE_DATASET

        datasets_folder = cls.get_folder()
        ANALYZE_DATASET["parameters"][0]["enum"] = os.listdir(datasets_folder)

    @staticmethod
    def get_folder() -> os.path:
        """
        Для создания папки /datasets, если не создана

        :return: путь к папке с датасетами
        """
        datasets_folder = f"{os.path.dirname(os.path.dirname(__file__))}{app.config['FILE_UPLOAD_FOLDER']}"

        if not os.path.exists(datasets_folder):
            os.mkdir(datasets_folder)

        return datasets_folder
