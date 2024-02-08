from typing import Optional

from flasgger import Schema, fields


class UserApiSchema(Schema):
    id = fields.Integer(description="User ID")
    email = fields.String(description="Email")


class AnalysisResultSchema(Schema):
    success: bool
    anomalies: Optional[dict] = None
    stationarity: Optional[dict] = None
    autocorrelation: Optional[dict] = None
    trends: Optional[dict] = None
    errors: Optional[dict] = None


class CalcHistorySchema(Schema):
    history: list[AnalysisResultSchema] = None


GET_USERS_SWAG = {"responses": {200: {"description": "List of users", "schema": UserApiSchema}}}

UPLOAD_DATASET_SWAG = {
    "summary": "Upload dataset",
    "consumes": ["multipart/form-data"],
    "parameters": [
        {"name": "file", "in": "formData", "description": "Dataset", "required": True, "type": "file"}
    ],
    "responses": {
        200: {"description": "Success"},
        400: {"description": "Bad Request"}
    },
}

ANALYZE_DATASET_SWAG = {
    "summary": "Analyze dataset",
    "parameters": [
        {
            "name": "filename",
            "in": "formData",
            "description": "Name of dataset to analyze",
            "default": "seattle-weather.csv",
            "required": True,
            "type": "string",
        },
        {
            "name": "email",
            "in": "formData",
            "description": "User email",
            "default": "user1@example.com",
            "required": True,
            "type": "string",
        },
    ],
    "responses": {
        200: {"description": "Analysis result", "schema": AnalysisResultSchema},
        400: {"description": "Bad Request"}
    },
}

CALC_HISTORY_SWAG = {
    "summary": "Get calculation history",
    "parameters": [
        {
            "name": "email",
            "in": "formData",
            "description": "User email",
            "default": "user1@example.com",
            "required": True,
            "type": "string",
        },
    ],
    "responses": {
        200: {"description": "Calculation history", "schema": CalcHistorySchema},
        400: {"description": "Bad Request"}
    },
}
