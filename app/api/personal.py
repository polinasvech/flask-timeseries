from flasgger import swag_from
from flask import Blueprint
from flask import current_app as app
from flask import json as flask_json
from flask import request
from flask_login import current_user, login_required
from schemas import UpdateUserSchema
from services.user_service import UserService
from sqlalchemy.exc import IntegrityError
from swagger import personal as swagger_personal
from flask_login import logout_user

bp = Blueprint("personal", __name__, url_prefix="/personal")


@bp.get("/calculation_history")
@swag_from(swagger_personal.CALC_HISTORY)
@login_required
def get_calculation_history():
    result = {"history": UserService.user_calc_history(user_id=current_user.get_id())}
    response = app.response_class(response=flask_json.dumps(result), mimetype="application/json")
    return response, 200


@bp.post("/change_username")
@swag_from(swagger_personal.CHANGE_USERNAME)
@login_required
def change_username():
    update_info = UpdateUserSchema(id=current_user.get_id(), username=request.values["new_username"])
    try:
        UserService.update(update_info)
    except IntegrityError:
        return "Username already taken", 400

    return "Username changed successfully", 200


@bp.post("/change_password")
@swag_from(swagger_personal.CHANGE_PASSWORD)
@login_required
def change_password():
    current_password = request.values["current_password"]
    new_password = request.values["new_password"]
    repeated_password = request.values["repeated_password"]

    user = UserService.get_user_by_id(current_user.get_id())
    if UserService.auth(user.username, current_password):
        if new_password != repeated_password:
            return "Password mismatch", 400

        update_info = UpdateUserSchema(id=current_user.get_id(), password=new_password)
        UserService.update(update_info)

        return "Password changed successfully", 200

    return "Wrong current password", 400


@bp.post("/delete")
@swag_from(swagger_personal.DELETE_PROFILE)
@login_required
def delete_user():
    password = request.values["password"]

    user = UserService.get_user_by_id(current_user.get_id())
    if UserService.auth(user.username, password):
        UserService.delete(current_user.get_id())
        logout_user()
        return "Successfully deleted user", 200

    return "Something went wrong...", 400
