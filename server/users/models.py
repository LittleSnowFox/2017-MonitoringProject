# -*- coding: utf-8 -*-
from sqlalchemy import Column, String, Boolean, Integer, DateTime
from werkzeug.security import check_password_hash

from server.run import db

# from passlib.apps import custom_app_context as pwd_context

"""
Contains table's models of the user part.
"""


class User(db.Model):
    __tablename__ = 'user'
    userid = Column(Integer(), unique=True, primary_key=True)
    username = Column(String(100), unique=True)
    email = Column(String(255), unique=True)
    password = Column(String(100), unique=False)
    is_active = Column(Boolean(), unique=False, default=False)
    activated_on = Column(DateTime, nullable=True)
    is_authenticated = Column(Boolean(), nullable=False, default=False)
    is_anonymous = Column(Boolean(), nullable=False, default=True)

    def __init__(self, userid=None, username=None, email=None, password=None, is_active=None, confirmed_on=None,
                 is_authenticated=None, is_anonymous=None):
        self.userid = userid
        self.username = username
        self.email = email
        self.set_password(password)
        self.is_active = is_active  # returns True if the user’s account is active - in addition to being authenticated,
        # they also have activated their account, not been suspended, or any condition your application has for
        # rejecting an account. Inactive accounts may not log in (without being forced of course)
        self.confirmed_on = confirmed_on
        self.is_authenticated = is_authenticated  # returns True if the user has provided valid credentials
        self.is_anonymous = is_anonymous  # returns True if the current user is an anonymous user

    @staticmethod
    def get_user(username):
        try:
            return User.query.filter(User.username == username).one()
        except:
            return User()

    def set_password(self, password):
        self.password = self.hash_password(password)

    def hash_password(self, password):
        return password
        # FIXME: use pysha3 + salt

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def get_id(self):
        """Method which, given a User instance, returns the unique ID for that object."""
        return self.userid

    @staticmethod
    def load_user(userid):
        """Given *user_id*, return the associated User object.
        :param unicode userid: user_id (username) user to retrieve
        """
        return User.query.filter(User.userid == userid).one()

    def __repr__(self):
        return '<user %r>' % self.username

    def to_json(self):
        return {"username": self.username, "email": self.email}
