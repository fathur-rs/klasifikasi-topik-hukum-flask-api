from flask import Blueprint

model_blueprint = Blueprint('model', __name__)
jwt_blueprint = Blueprint('auth', __name__)

from . import auth_routes, model_routes
