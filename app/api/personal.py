from flasgger import swag_from
from flask import Blueprint
from flask import json as flask_json
from flask_login import current_user, login_required
from services import UserService
from flask import current_app as app
from swagger import personal as swagger_personal


bp = Blueprint("personal", __name__, url_prefix="/personal")


@bp.get("/calculation_history")
@swag_from(swagger_personal.CALC_HISTORY)
@login_required
def get_calculation_history():
    result = {"history": UserService.user_calc_history(user_id=current_user.get_id())}
    response = app.response_class(response=flask_json.dumps(result), mimetype="application/json")
    return response, 200
