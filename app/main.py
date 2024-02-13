import swagger_schemas
from flasgger import Swagger, swag_from
from flask import Flask
from flask import json as flask_json
from flask import request
from flask_login import (LoginManager, current_user, login_required,
                         login_user, logout_user)
from models import User
from services import AnalyzeService, FileService, UserService
from utils import DatasetNotFoundError, FileExtensionError, UserNotFoundError

app = Flask(__name__)

login_manager = LoginManager()
login_manager.init_app(app)

# автоматическая генерация OpenAPI, доступна по /apidocs
app.config["SWAGGER"] = swagger_schemas.SWAGGER_SETTINGS
swagger = Swagger(app)

app.config["FILE_UPLOAD_FOLDER"] = "/datasets"


@login_manager.user_loader
def load_user(user):
    user = UserService.get_user_by_id(user)
    return user


@app.post("/login")
@swag_from(swagger_schemas.AUTH)
def login():
    email = request.values["email"]
    password = request.values["password"]

    user = UserService.get_user_by_email(email)
    if not user:
        return "User not found", 404
    if not UserService.auth_user(user, password):
        return "Wrong password", 401

    login_user(user)
    return "Success", 200


@app.post("/logout")
@swag_from(swagger_schemas.LOGOUT)
def logout():
    logout_user()
    return "Success", 200


@app.get("/users")
@swag_from(swagger_schemas.GET_USERS)
@login_required
def get_users():
    users: list[User] = UserService.list_users()
    return users


@app.get("/calculation_history")
@swag_from(swagger_schemas.CALC_HISTORY)
@login_required
def get_calculation_history():
    result = {"history": UserService.user_calc_history(user_id=current_user.get_id())}
    response = app.response_class(response=flask_json.dumps(result), mimetype="application/json")
    return response, 200


@app.post("/upload_dataset")
@swag_from(swagger_schemas.UPLOAD_DATASET)
@login_required
def upload_file():
    uploaded_file = request.files["file"]

    try:
        filename = FileService.save_file(uploaded_file)
    except FileExtensionError as e:
        return e.message, 422

    return f"File {filename} saved successfully", 200


@app.post("/analyze")
@swag_from(swagger_schemas.ANALYZE_DATASET)
@login_required
def analyze():
    filename = request.values["filename"]

    try:
        analyze_service = AnalyzeService(
            filename=filename,
            user_id=current_user.get_id(),
        )
        result = analyze_service.analyze()
    except (UserNotFoundError, DatasetNotFoundError) as e:
        return e.message, 400

    response = app.response_class(response=flask_json.dumps(result), mimetype="application/json")
    return response, 200


@app.before_request
def before_request():
    with app.app_context():
        FileService.list_datasets()


if __name__ == "__main__":
    app.secret_key = "37f2ab79-9be0-4c0b-8c73-8ac63a816629"
    app.run(debug=True)
