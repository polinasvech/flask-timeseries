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
    update_info = UpdateUserSchema(id=1, username=request.values["new_username"])
    try:
        UserService.update(update_info)
    except IntegrityError:
        return "Username already taken", 400

    return "Username changed successfully", 200
