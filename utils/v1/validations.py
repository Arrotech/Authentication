import re

from flask import jsonify, make_response


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
