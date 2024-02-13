import sqlalchemy.exc
import swagger_schemas
from flasgger import Swagger, swag_from
from flask import Flask
from flask import json as flask_json
from flask import request
from flask_login import (LoginManager, current_user, login_required,
                         login_user, logout_user)
from services import AnalyzeService, FileService, UserService
from utils import (DatasetNotFoundError, EmptyFileError, FileExtensionError,
                   NotTimeSeriesError, UserNotFoundError)

app = Flask(__name__)
# для авторизации
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
@swag_from(swagger_schemas.LOGIN)
def login():
    email = request.values["email"]
    password = request.values["password"]

    try:
        user = UserService.auth_user(email, password)
    except UserNotFoundError as e:
        return e.message, 404

    if user:
        login_user(user)
        return "Success", 200

    return "Wrong password", 401


@app.post("/register")
@swag_from(swagger_schemas.REGISTER)
def register():
    email = request.values["email"]
    password = request.values["password"]
    repeated_password = request.values["repeated_password"]

    if password != repeated_password:
        return f"Password mismatch", 400

    try:
        user = UserService.create(email, password)
    except sqlalchemy.exc.IntegrityError:
        return f"User with email {email} already exists", 209

    if user:
        return f"Created user {email}", 201


@app.post("/logout")
@swag_from(swagger_schemas.LOGOUT)
def logout():
    logout_user()
    return "Success", 200


@app.get("/users")
@swag_from(swagger_schemas.GET_USERS)
@login_required
def get_users():
    users = UserService.list_users()
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
    except (FileExtensionError, NotTimeSeriesError) as e:
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
    except (UserNotFoundError, DatasetNotFoundError, EmptyFileError) as e:
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
