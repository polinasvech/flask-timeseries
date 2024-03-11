import sqlalchemy.exc
from exceptions import UserNotFoundError
from flasgger import swag_from
from flask import Blueprint, request
from flask_login import login_user, logout_user
from services.user_service import UserService
from swagger import auth as swagger_auth

bp = Blueprint("auth", __name__, url_prefix="/auth")


@bp.post("/login")
@swag_from(swagger_auth.LOGIN)
def login():
    username = request.values["username"]
    password = request.values["password"]

    try:
        user = UserService.auth(username, password)
    except UserNotFoundError as e:
        return e.message, 404

    if user:
        login_user(user)
        return "Success", 200

    return "Wrong password", 401


@bp.post("/register")
@swag_from(swagger_auth.REGISTER)
def register():
    username = request.values["username"]
    password = request.values["password"]
    repeated_password = request.values["repeated_password"]

    if password != repeated_password:
        return "Password mismatch", 400

    try:
        user = UserService.create(username, password)
    except sqlalchemy.exc.IntegrityError:
        return f"User {username} already exists", 409

    if user:
        return f"Created user {username}", 201


@bp.post("/logout")
@swag_from(swagger_auth.LOGOUT)
def logout():
    logout_user()
    return "Success", 200
