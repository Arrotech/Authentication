"""Import flask module."""
import os
from os import path
from dotenv import load_dotenv
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_mail import Mail
from flask import Flask, jsonify, make_response, Blueprint
from flask_restful import Api

from app.api.v1.models.database import Database
from app.api.v1 import auth_v1
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
    app = Flask(__name__, template_folder='../../../templates')
    config_name = os.getenv('FLASK_ENV')
    app.config.from_pyfile('config.py')
    app.config['SECRET_KEY'] = "thisisarrotech"
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 465
    app.config['MAIL_USE_TLS'] = False
    app.config['MAIL_USE_SSL'] = True
    app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
    app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
 

    CORS(app)
    JWTManager(app)
    Mail(app)

    app.register_blueprint(auth_v1, url_prefix='/api/v1/')
    app.register_error_handler(404, page_not_found)
    app.register_error_handler(405, method_not_allowed)

    basedir = path.abspath(path.dirname(__file__))
    load_dotenv(path.join(basedir, '.env'))

    return app
