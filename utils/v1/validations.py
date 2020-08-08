import re
import os

from flask import jsonify, make_response, url_for, current_app
from itsdangerous import URLSafeTimedSerializer

def raise_error(status, msg):
    """Display error message."""
    return make_response(jsonify({
        "status": "400",
        "message": msg
    }), status)


def check_register_keys(request):
    """Check that registration json keys match the required ones."""
    res_keys = ['firstname', 'lastname',
                'phone', 'username', 'email', 'password']
    errors = []
    for key in res_keys:
        if not key in request.json:
            errors.append(key)
    return errors


def check_login_keys(request):
    """Check that login json keys match the required ones."""
    res_keys = ['email', 'password']
    errors = []
    for key in res_keys:
        if not key in request.json:
            errors.append(key)
    return errors


def is_valid_email(variable):
    """Check if email is a valid mail."""
    if re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+[a-zA-Z0-9-.]+$)",
                variable):
        return True
    return False


def is_valid_phone(variable):
    """Check if phone number is a valid mail."""
    if re.match(r"(^(?:254|\+254|0)?(7(?:(?:[129][0-9])|(?:0[0-8])|(4[0-1]))[0-9]{6})$)",
                variable):
        return True
    return False


def is_valid_password(variable):
    """Check if password is a valid password."""
    if re.match(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$", variable):
        return True
    return False

def default_encode_token(email, salt='email-confirm-key'):
    """Encode token using email."""
    serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    return serializer.dumps(email, salt=salt)


def default_decode_token(token, salt='email-confirm-key', expiration=3600):
    """Decode token and get the email."""
    serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    try:
        email = serializer.loads(
            token, salt='email-confirm-key', max_age=expiration)
        return email
    except Exception as e:
        return False


def generate_url(endpoint, token):
    """Generate url to concatenate at the end of another url."""
    return url_for(endpoint, token=token, _external=True)
