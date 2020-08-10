from flask_wtf import Form
from wtforms import StringField, PasswordField, validators

class EmailForm(Form):
    email = StringField('Email', [validators.Length(min=6, max=35)])

class PasswordForm(Form):
    password = PasswordField('Password', [
        validators.DataRequired()
    ])
