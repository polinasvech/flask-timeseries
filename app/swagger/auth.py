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
    "tags": ["auth"],
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
    "tags": ["auth"],
}

LOGOUT = {
    "summary": "Logout",
    "responses": {
        200: {"description": "Success"},
    },
    "tags": ["auth"],
}
