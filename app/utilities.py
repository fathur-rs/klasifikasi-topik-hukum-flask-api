from flask import jsonify, make_response, request
from functools import wraps
import jwt
import datetime
import os
from jwt import ExpiredSignatureError, DecodeError, InvalidTokenError
from dotenv import load_dotenv 
load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")

from flask import make_response, jsonify

def make_response_util(status_code, message=None, description=None, error=None, additional_headers=None):
    response_content = {'status_code': status_code}
    if message:
        response_content.update({'message': message})
    if description:
        response_content.update({'description': description})
    if error:
        response_content.update({'error': error})
    response = make_response(jsonify(response_content), status_code)
    if additional_headers:
        for header, value in additional_headers.items():
            response.headers[header] = value
    return response


def handle_exceptions(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except ValueError as ve:
            return make_response_util(400, description=f"Value Error: {str(ve)}", error='Bad Request')
        except RuntimeError as re:
            return make_response_util(400, description=f"Runtime Error: {str(re)}", error='Bad Request')
        except Exception as e:
            return make_response_util(400, description=f"Unhandled exception: {str(e)}", error='Bad Request')
    return decorated_function

def generate_token(user):
    payload = {
        "user": user,
        "exp": datetime.datetime.now() + datetime.timedelta(minutes=18000),
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    return token

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('x-access-token')
        if not token:
            return make_response_util(401, description="Token is missing", error='Unauthorized')

        try:
            jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        except ExpiredSignatureError:
            return make_response_util(401, description="Token has expired", error='Unauthorized')
        except (DecodeError, InvalidTokenError):
            return make_response_util(401, description="Token is invalid", error='Unauthorized')

        return f(*args, **kwargs)
    return decorated

