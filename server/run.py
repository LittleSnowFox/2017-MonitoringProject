# -*- coding: utf-8 -*-

from flask import Flask
from flask_login import LoginManager
#from Users.utils import load_user
#from Core.views import core_page
#from Users.views import user_page
import os


app = Flask(__name__)

# Creation and configuration of the loginManager class
login_manager = LoginManager()
login_manager.init_app(app)
# User_loader callback to reload the user object from the user ID stored in the session. It should return None (not
# raise an exception) if the ID is not valid. (In that case, the ID will manually be removed from the session and
# processing will continue.)
#login_manager.user_callback = load_user

# Register blueprints
#app.register_blueprint(core_page)
#app.register_blueprint(user_page)

# Generates secret key using a cryptographic random generator
app.config["SECRET_KEY"] = os.urandom(24)

# Run application
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True)
