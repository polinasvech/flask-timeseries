SWAGGER_SETTINGS = {
    "version": "1.0.0",
    "title": "Analyze dataset API",
}

REGISTER = {
    "summary": "Register user",
    "parameters": [
        {
            "name": "username",
            "in": "formData",
            "description": "Username",
            "required": True,
            "type": "string",
        },
        {
            "name": "password",
            "in": "formData",
            "description": "Password",
            "required": True,
            "type": "string",
            "format": "password",
        },
        {
            "name": "repeated_password",
            "in": "formData",
            "description": "Repeat password",
            "required": True,
            "type": "string",
            "format": "password",
        },
    ],
    "responses": {
        201: {"description": "Created user"},
        409: {"description": "Already exists"},
        400: {"description": "Bad Request"},
    },
}

LOGIN = {
    "summary": "Authorize user",
    "parameters": [
        {
            "name": "username",
            "in": "formData",
            "description": "Username",
            "required": True,
            "type": "string",
        },
        {
            "name": "password",
            "in": "formData",
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

CALC_HISTORY = {
    "summary": "Get calculation history",
    "responses": {
        200: {"description": "Calculation history"},
        400: {"description": "Bad Request"},
    },
}
