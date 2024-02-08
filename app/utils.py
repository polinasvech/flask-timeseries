import os


class UserNotFoundError(Exception):
    def __init__(self, message="User not found"):
        self.message = message
        super().__init__(message)


class FileExtensionError(Exception):
    def __init__(self, filename):
        file_ext = filename.split(".")
        self.message = f"Invalid file extension: {file_ext[-1]}"
        super().__init__(self.message)


class DatasetNotFoundError(Exception):
    def __init__(self, datasets_folder):
        self.message = (
            f"File not found. Available datasets: {os.listdir(datasets_folder)}"
            if os.listdir(datasets_folder)
            else "File not found"
        )
        super().__init__(self.message)
