SWAGGER_SETTINGS = {
    "version": "1.0.0",
    "title": "Analyze dataset API",
}

GET_USERS = {
    "responses": {200: {"description": "List of users"}},
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
        200: {"description": "Analysis result"},
        400: {"description": "Bad Request"},
    },
}
