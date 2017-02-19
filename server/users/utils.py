# -*- coding: utf-8 -*-
import re
from itsdangerous import URLSafeTimedSerializer
from flask_mail import Message
from run import app, mail
from server.config import BaseConfig


ts = URLSafeTimedSerializer(app.config["SECRET_KEY"])


def load_user(username):
    """Given *user_id*, return the associated User object.
    :param unicode user_id: user_id (username) user to retrieve
    """
    from .models import User
    return User.get_user(username)


####################################
# Check email form for registration
####################################
def is_email_address_valid(email):
    """Validate the email address using a regex."""
    if not re.match("^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*$", email):
        return False
    return True


####################################
# Send email form for confirmation
####################################
def send_email(to, subject, body):
    msg = Message(
        subject,
        recipients=[to],
        body=body,
        sender=app.config['MAIL_DEFAULT_SENDER']
    )
    mail.send(msg)
