from flask import request, jsonify
from app.api import jwt_blueprint
from ..utilities import make_response_util, generate_token
from ..models.users import User
from ..extensions.db import db
from werkzeug.security import generate_password_hash, check_password_hash

@jwt_blueprint.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return make_response_util(400, description="Missing username or password", error="Bad Request")

    user = User.query.filter_by(username=username).first()
    if user:    
        return make_response_util(409, description="User already exists", error="Conflict")

    hashed_password = generate_password_hash(password)
    new_user = User(username=username, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()

    return make_response_util(201, message="User created successfully")

@jwt_blueprint.route("/delete_user/", methods=["DELETE"])
def delete_user():
    user_id = request.args.get('id', type=int)
    if not user_id:
        return make_response_util(400, description="No user ID provided", error="Bad Request")
    
    user = User.query.get(user_id)
    if not user:
        return make_response_util(404, description="User does not exist", error="Not Found")

    db.session.delete(user)
    db.session.commit()

    return make_response_util(200, message="User deleted successfully")

@jwt_blueprint.route("/user/", methods=["GET"])
def get_user():
    user_id = request.args.get('id', type=int)
    if not user_id:
        return make_response_util(400, description="No user ID provided", error="Bad Request")

    user = User.query.get(user_id)
    if not user:
        return make_response_util(404, description="User does not exist", error="Not Found")
    
    user_data = {'username': user.username, 'id': user.id}
    return make_response_util(200, message=user_data)

@jwt_blueprint.route("/users", methods=["GET"])
def list_users():
    users = User.query.all()
    users_list = [{'id': user.id, 'username': user.username} for user in users]
    return make_response_util(200, message=users_list)


@jwt_blueprint.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return make_response_util(400, description="Missing username or password", error="Bad Request")

    user = User.query.filter_by(username=username).first()
    if user and check_password_hash(user.password, password):
        token = generate_token(user.id)
        return make_response_util(200, message={"token": token})

    return make_response_util(401, description="Could not verify", error="Unauthorized", additional_headers={"WWW-Authenticate": "Basic realm='Login Required'"})
