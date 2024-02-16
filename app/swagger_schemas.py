from typing import Optional

from flasgger import Schema, fields


class UserApiSchema(Schema):
    id = fields.Integer(description="User ID")
    username = fields.String(description="Username")
    created_at = fields.DateTime(description="Registration date")


class AnalysisResultSchema(Schema):
    success: bool
    anomalies: Optional[dict] = None
    stationarity: Optional[dict] = None
    autocorrelation: Optional[dict] = None
    trends: Optional[dict] = None
    errors: Optional[dict] = None


class CalcHistorySchema(Schema):
    history: list[AnalysisResultSchema] = None


SWAGGER_SETTINGS = {
    "version": "1.0.0",
    "title": "Analyze dataset API",
}

REGISTER = {
    "summary": "Register user",
    "parameters": [
        {
            "name": "username",
            "in": "query",
            "description": "Username",
            "required": True,
            "type": "string",
        },
        {
            "name": "password",
            "in": "query",
            "description": "Password",
            "required": True,
            "type": "string",
            "format": "password",
        },
        {
            "name": "repeated_password",
            "in": "query",
            "description": "Repeat password",
            "required": True,
            "type": "string",
            "format": "password",
        },
    ],
    "responses": {
        201: {"description": "Created user"},
        209: {"description": "Already exists"},
        400: {"description": "Bad Request"},
    },
}

LOGIN = {
    "summary": "Authorize user",
    "parameters": [
        {
            "name": "username",
            "in": "query",
            "description": "Username",
            "required": True,
            "type": "string",
        },
        {
            "name": "password",
            "in": "query",
            "description": "Password",
            "required": True,
            "type": "string",
            "format": "password",
        },
    ],
    "responses": {
        200: {"description": "Success"},
        404: {"description": "User not found"},
        401: {"description": "Wrong password"},
    },
}

LOGOUT = {
    "summary": "Logout",
    "responses": {
        200: {"description": "Success"},
    },
}

GET_USERS = {
    "responses": {200: {"description": "List of users", "schema": UserApiSchema}},
}

UPLOAD_DATASET = {
    "summary": "Upload dataset",
    "consumes": ["multipart/form-data"],
    "parameters": [{"name": "file", "in": "formData", "description": "Dataset", "required": True, "type": "file"}],
    "responses": {200: {"description": "Success"}, 400: {"description": "Bad Request"}},
}

ANALYZE_DATASET = {
    "summary": "Analyze dataset",
    "parameters": [
        {
            "name": "filename",
            "in": "formData",
            "description": "Dataset to analyze",
            "required": True,
            "type": "string",
        },
    ],
    "responses": {
        200: {"description": "Analysis result", "schema": AnalysisResultSchema},
        400: {"description": "Bad Request"},
    },
}

CALC_HISTORY = {
    "summary": "Get calculation history",
    "responses": {
        200: {"description": "Calculation history", "schema": CalcHistorySchema},
        400: {"description": "Bad Request"},
    },
}
