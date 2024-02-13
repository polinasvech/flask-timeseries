import os
import re

from flask import current_app as app
from utils import FileExtensionError
from werkzeug.datastructures.file_storage import FileStorage


class FileService:
    @staticmethod
    def save_file(uploaded_file: FileStorage) -> str:
        if not re.search(r"\.csv$", uploaded_file.filename):
            # если загрузили файл не .csv формата, возвращаем ошибку
            raise FileExtensionError(uploaded_file.filename)

        datasets_folder = f"{os.path.dirname(os.path.dirname(__file__))}{app.config['FILE_UPLOAD_FOLDER']}"
        if not os.path.exists(datasets_folder):
            os.mkdir(datasets_folder)

        uploaded_file.save(f"{datasets_folder}/{uploaded_file.filename}")

        return uploaded_file.filename

    @staticmethod
    def list_datasets():
        """Для перечисления возможных для анализа датасетов"""
        from swagger_schemas import ANALYZE_DATASET

        datasets_folder = f"{os.path.dirname(os.path.dirname(__file__))}{app.config['FILE_UPLOAD_FOLDER']}"
        ANALYZE_DATASET["parameters"][0]["enum"] = os.listdir(datasets_folder)
