from flask import Response, request, current_app as app
from db.models import User
from flask_restful import Resource
from mongoengine.errors import DoesNotExist, NotUniqueError, ValidationError
from errors import InternalServerError, SchemaValidationError, UserNotFoundError, UsernameAlreadyExistError


class UsersApi(Resource):
    def get(self):
        users_json = User.objects().to_json()
        return Response(users_json, mimetype="application/json", status=200)

    def post(self):
        body = request.get_json()

        required_fields = ["username", "password", "preferences", "created_ts"]
        missing_fields = [field for field in required_fields if field not in body]

        if "preferences" in body and "timezone" not in body["preferences"]:
            missing_fields.append("preferences.timezone")

        if missing_fields:
            error_message = "Missing required fields: " + ", ".join(missing_fields)
            raise SchemaValidationError(description=error_message)

        for field in required_fields:
            if not body.get(field):
                missing_fields.append(f"Field {field} cannot be empty.")

        if missing_fields:
            error_message = "Fields cannot be empty: " + ", ".join(missing_fields)
            raise SchemaValidationError(description=error_message)

        try:
            user = User(**body).save()
            return {'id': str(user.id)}, 201
        except NotUniqueError:
            raise UsernameAlreadyExistError(description="User with specified username already exists")
        except ValidationError as ve:
            raise SchemaValidationError(description=str(ve))
        except Exception as e:
            app.logger.error(e)
            raise InternalServerError()


class UserApi(Resource):
    def put(self, id):
        body = request.get_json()
        try:
            User.objects.get(id=id).update(**body)
            return '', 200
        except DoesNotExist:
            raise UserNotFoundError(description="User not found")
        except Exception as e:
            app.logger.error(e)
            raise InternalServerError()

    def get(self, id):
        try:
            user_json = User.objects.get(id=id).to_json()
            return Response(user_json, mimetype="application/json", status=200)
        except DoesNotExist:
            raise UserNotFoundError(description="User not found")
        except Exception as e:
            app.logger.error(e)
            raise InternalServerError()

    def delete(self, id):
        try:
            User.objects.get(id=id).delete()
            return '', 200
        except DoesNotExist:
            raise UserNotFoundError(description="User not found")
        except Exception as e:
            app.logger.error(e)
            raise InternalServerError()
