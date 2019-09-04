"""Import flask module."""
from flask import Flask, jsonify, make_response, Blueprint
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_restful import Api

from app.api.v1.views.auth import auth
from app.config import app_config


def page_not_found(e):
    """Capture Not Found error."""
    return make_response(jsonify({
        "status": "400",
        "message": "resource not found"
    }), 404)


def method_not_allowed(e):
    """Capture method not allowed error."""
    return make_response(jsonify({
        "status": "405",
        "message": "method not allowed"
    }), 405)


def auth_app(config_name):
    """Create the authentication app."""
    app = Flask(__name__)
    CORS(app)

    app.config.from_pyfile('config.py')
    app.config["SECRET_KEY"] = 'thisisarrotech'
    jwt = JWTManager(app)

    api = Api(app)

    app.register_blueprint(auth, url_prefix='/api/v1/')
    app.register_error_handler(404, page_not_found)
    app.register_error_handler(405, method_not_allowed)

    return app
