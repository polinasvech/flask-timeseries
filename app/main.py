import os

from api_schemas import (ANALYZE_DATASET_SWAG, CALC_HISTORY_SWAG,
                         GET_USERS_SWAG, UPLOAD_DATASET_SWAG)
from flasgger import Swagger, swag_from
from flask import Flask
from flask import json as flask_json
from flask import request
from models import User
from services import (AnalyzeService, FileExtensionError, FileService,
                      UserService)

app = Flask(__name__)

# автоматическая генерация OpenAPI, доступна по /apidocs
swagger = Swagger(app)

app.config["FILE_UPLOAD_FOLDER"] = "/datasets"


@app.route("/users/", methods=["GET"])
@swag_from(GET_USERS_SWAG)
def get_users():
    users: list[User] = UserService.list_users()
    return users


@app.post("/upload_dataset")
@swag_from(UPLOAD_DATASET_SWAG)
def upload_file():
    uploaded_file = request.files["file"]

    try:
        filename = FileService.save_file(uploaded_file)
    except FileExtensionError as e:
        return e.message, 422

    return f"File {filename} saved successfully", 200


@app.post("/analyze")
@swag_from(ANALYZE_DATASET_SWAG)
def analyze():
    email = request.values["email"]
    filename = request.values["filename"]
    analyze_service = AnalyzeService(
        filepath=f"{os.path.dirname(os.path.dirname(__file__))}/app{app.config['FILE_UPLOAD_FOLDER']}/{filename}",
        user_email=email,
    )
    result = analyze_service.analyze()

    response = app.response_class(response=flask_json.dumps(result), mimetype="application/json")
    return response, 200


@app.post("/calculation_history")
@swag_from(CALC_HISTORY_SWAG)
def get_calculation_history():
    email = request.values["email"]
    result = {"history": UserService.user_calc_history(email=email)}
    response = app.response_class(response=flask_json.dumps(result), mimetype="application/json")
    return response, 200


if __name__ == "__main__":
    app.run(debug=True)
