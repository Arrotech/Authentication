import json
from flask import make_response, jsonify, request, Blueprint
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, create_refresh_token, jwt_refresh_token_required, get_raw_jwt
from app.api.v1.models.auth import UsersModel
from utils.v1.validations import is_valid_email, raise_error, check_register_keys, check_login_keys, is_valid_password, is_valid_phone
import datetime
from werkzeug.security import check_password_hash

auth = Blueprint('auth', __name__)


@auth.route('/auth/register', methods=['POST'])
def signup():
    """A new user can create a new account."""
    errors = check_register_keys(request)
    if errors:
        return raise_error(400, "Invalid {} key".format(', '.join(errors)))
    details = request.get_json()
    firstname = details['firstname']
    lastname = details['lastname']
    phone = details['phone']
    username = details['username']
    email = details['email']
    password = details['password']
    if details['firstname'].isalpha() is False:
        return raise_error(400, "First name is in wrong format")
    if details['lastname'].isalpha() is False:
        return raise_error(400, "Last name is in wrong format")
    if not is_valid_phone(phone):
        return raise_error(400, "Invalid phone number!")
    if not is_valid_email(email):
        return raise_error(400, "Invalid email!")
    if not is_valid_password(password):
        return raise_error(400, "Minimum eight characters, at least one uppercase letter, one lowercase letter, one number and one special character!")
    user_phone = json.loads(UsersModel().get_phone(phone))
    if user_phone:
        return raise_error(400, "Phone number already exists!")
    user_username = json.loads(UsersModel().get_username(username))
    if user_username:
        return raise_error(400, "Username already exists!")
    user_email = json.loads(UsersModel().get_email(email))
    if user_email:
        return raise_error(400, "Email already exists!")
    user = UsersModel(firstname, lastname, phone,
                      username, email, password).save()
    user = json.loads(user)
    return make_response(jsonify({
        "message": "Account created successfully!",
        "status": "201",
        "user": user
    }), 201)


@auth.route('/auth/login', methods=['POST'])
def login():
    """Already existing user can sign in to their account."""
    errors = check_login_keys(request)
    if errors:
        return raise_error(400, "Invalid {} key".format(', '.join(errors)))
    details = request.get_json()
    email = details['email']
    password = details['password']
    user = json.loads(UsersModel().get_email(email))
    if user:
        password_db = user['password']
        if check_password_hash(password_db, password):
            expires = datetime.timedelta(days=365)
            token = create_access_token(identity=email, expires_delta=expires)
            refresh_token = create_refresh_token(
                identity=email, expires_delta=expires)
            return make_response(jsonify({
                "status": "200",
                "message": "Successfully logged in!",
                "token": token,
                "refresh_token": refresh_token,
                "user": user
            }), 200)
        return make_response(jsonify({
            "status": "401",
            "message": "Invalid Email or Password"
        }), 401)
    return make_response(jsonify({
        "status": "401",
        "message": "Invalid Email or Password"
    }), 401)


@auth.route('/auth/refresh', methods=['POST'])
@jwt_refresh_token_required
def refresh():
    """Get the access token."""
    current_user = get_jwt_identity()
    expires = datetime.timedelta(days=365)
    access_token = create_access_token(current_user, expires_delta=expires)
    ret = {
        'access_token': access_token
    }
    return jsonify(ret), 200


@auth.route('/auth/protected', methods=['GET'])
@jwt_required
def protected():
    """Access the protected route."""
    email = get_jwt_identity()
    return jsonify(logged_in_as=email), 200


@auth.route('/users', methods=['GET'])
@jwt_required
def get_users():
    """Get all users."""
    return make_response(jsonify({
        "message": "success",
        "status": "200",
        "users": json.loads(UsersModel().get_users())
    }), 200)


@auth.route('/users/<string:username>', methods=['GET'])
@jwt_required
def get_user(username):
    """Get a specific user by the username."""
    user = UsersModel().get_username(username)
    user = json.loads(user)
    if user:
        return make_response(jsonify({
            "message": "success",
            "status": "200",
            "user": user
        }), 200)
    return make_response(jsonify({
        "message": "User not found",
        "status": "404"
    }), 404)
