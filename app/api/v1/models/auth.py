import json
from werkzeug.security import generate_password_hash
from app.api.v1.models.database import Database
from datetime import datetime


class UsersModel(Database):
    """Add a new user and retrieve User(s) by Id, Username or Email."""

    def __init__(self, firstname=None, lastname=None, phone=None, username=None, email=None, password=None, is_confirmed=False, confirmed_on=None, date=None):
        super().__init__()
        self.firstname = firstname
        self.lastname = lastname
        self.phone = phone
        self.username = username
        self.email = email
        if password:
            self.password = generate_password_hash(password)
        self.is_confirmed = is_confirmed
        self.confirmed_on = datetime.now()
        self.date = datetime.now()

    def save(self):
        """Save information of the new user."""
        self.curr.execute(
            ''' INSERT INTO users(firstname, lastname, phone, username, email, password, is_confirmed, date)\
                VALUES('{}','{}','{}','{}','{}','{}','{}','{}') RETURNING firstname, lastname, phone, username, email, password, is_confirmed, date'''
            .format(self.firstname, self.lastname, self.phone, self.username, self.email, self.password, self.is_confirmed,
                    self.date))
        user = self.curr.fetchone()
        self.conn.commit()
        self.curr.close()
        return json.dumps(user, default=str)

    def get_users(self):
        "Get all users."
        query = "SELECT * from users"
        users = Database().fetch(query)
        return json.dumps(users, default=str)

    def get_username(self, username):
        """Request a single user with specific Username."""
        query = "SELECT * FROM users WHERE username=%s"
        var = username
        user = Database().fetch_one(query, (var,),)
        return json.dumps(user, default=str)

    def get_email(self, email):
        """Request a single user with specific Email Address."""
        query = "SELECT * FROM users WHERE email=%s"
        var = email
        user = Database().fetch_one(query, (var,),)
        return json.dumps(user, default=str)

    def get_phone(self, phone):
        """Request a single user with specific Phone Number."""
        query = "SELECT * FROM users WHERE phone=%s"
        var = phone
        user = Database().fetch_one(query, (var,),)
        return json.dumps(user, default=str)

    def confirm_email(self, user_id, is_confirmed):
        """Confirm user email."""
        self.curr.execute(
            """UPDATE users SET is_confirmed=True WHERE user_id={} RETURNING is_confirmed, confirmed_on""".format(user_id, is_confirmed))
        response = self.curr.fetchone()
        self.conn.commit()
        self.curr.close()
        return json.dumps(response, default=str)
