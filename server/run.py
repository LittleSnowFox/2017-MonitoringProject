# -*- coding: utf-8 -*-
from flask import Flask
from flask_mail import Mail
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
import os

#################################
# Application and api definition
#################################
app = Flask(__name__)

app.config.from_object("server.config.BaseConfig")
mail = Mail()
mail.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)


######################################################################################
# Generates a secret random key for the session with a cryptographic random generator
######################################################################################
def generate_secretkey(name):
    if os.path.exists(name):
        return open(name).read()
    else:
        key = os.urandom(24)
        with open(name, "w+") as skf:
            skf.write(key.hex())
        return key


app.config["SECRET_KEY"] = generate_secretkey("secret_key.txt")
app.config["SQLALCHEMY_DATABASE_URI"] = 'postgresql+psycopg2://docker:docker@db/dbmonitoring'

db = SQLAlchemy(app)

app.config["SECURITY_PASSWORD_SALT"] = generate_secretkey("salt.txt")

##################
# Run application
##################
if __name__ == "__main__":
    from server.users.models import User
    from server.users.views import user_views

    #################################
    # Register blueprints
    #################################
    app.register_blueprint(user_views)


    # User_loader callback to reload the user object from the user ID stored in the session. It should return None (not
    # raise an exception) if the ID is not valid. (In that case, the ID will manually be removed from the session and
    # processing will continue.)
    @login_manager.user_loader
    def load_user(userid):
        return User.load_user(userid)


    app.run(host='0.0.0.0', port=80, debug=True)
