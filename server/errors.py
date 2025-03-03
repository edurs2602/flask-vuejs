from werkzeug.exceptions import HTTPException
from flask import jsonify

class InternalServerError(HTTPException):
    pass

class SchemaValidationError(HTTPException):
    pass

class UserNotFoundError(HTTPException):
    pass

class UsernameAlreadyExistError(HTTPException):
    pass

errors = {
    "InternalServerError": {
        "message": "Oops something wrong",
        "status": 500
    },
    "SchemaValidationError": {
        "message": "Required fields missing",
        "status": 400
    },
    "UserNotFoundError": {
        "message": "User not found in database",
        "status": 400
    },
    "UsernameAlreadyExistError": {
        "message": "User with specified username already exists in database",
        "status": 400
    },
}

def register_error_handlers(app):
    @app.errorhandler(SchemaValidationError)
    def handle_schema_validation_error(error):
        response = {
            "message": error.description if hasattr(error, "description") and error.description else errors["SchemaValidationError"]["message"],
            "status": errors["SchemaValidationError"]["status"]
        }
        return jsonify(response), errors["SchemaValidationError"]["status"]

    @app.errorhandler(UserNotFoundError)
    def handle_user_not_found_error(error):
        response = {
            "message": error.description if hasattr(error, "description") and error.description else errors["UserNotFoundError"]["message"],
            "status": errors["UserNotFoundError"]["status"]
        }
        return jsonify(response), errors["UserNotFoundError"]["status"]

    @app.errorhandler(EmailAlreadyExistError)
    def handle_email_already_exist_error(error):
        response = {
            "message": error.description if hasattr(error, "description") and error.description else errors["EmailAlreadyExistError"]["message"],
            "status": errors["EmailAlreadyExistError"]["status"]
        }
        return jsonify(response), errors["EmailAlreadyExistError"]["status"]

    @app.errorhandler(InternalServerError)
    def handle_internal_server_error(error):
        response = {
            "message": error.description if hasattr(error, "description") and error.description else errors["InternalServerError"]["message"],
            "status": errors["InternalServerError"]["status"]
        }
        return jsonify(response), errors["InternalServerError"]["status"]
