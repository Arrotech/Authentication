import os
from threading import Thread
from flask_mail import Message, Mail
from app.__init__ import auth_app
from utils.v1.validations import raise_error
from app.config import app_config

config_name = os.getenv('FLASK_ENV')
app = auth_app(config_name)
mail = Mail(app)


def send_async_email(app, msg):
    """Send asychronous email."""
    with app.app_context():
        try:
            mail.send(msg)
        except ConnectionRefusedError:
            return raise_error(500, 'Mail server not working')


def send_email(subject, sender, recipients, text_body, html_body):
    """Message body."""
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    Thread(target=send_async_email, args=(app, msg)).start()