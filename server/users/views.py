# -*- coding: utf-8 -*-
import datetime
from flask import Blueprint, request, jsonify, render_template, url_for
from flask_login import login_required, login_user, logout_user, current_user
from .models import User
from server.run import db, app
from .utils import is_email_address_valid, send_email
from server.addtoken import generate_confirmation_token, confirm_token


user_views = Blueprint('user_views', __name__)


@user_views.route('/register', methods=['POST'])
def register():
    if not request.json:
        return jsonify({'status': "invalid request"}), 400
    username = request.json.get('username', None)
    email = request.json.get('email', None)
    password = request.json.get('password', None)
    passwordconfirm = request.json.get('passwordconfirm', None)
    if email is None or password is None or username is None or passwordconfirm is None:
        return jsonify({'status': 1}), 400  # missing arguments
    elif User.query.filter_by(username=username).first() is not None:
        return jsonify({'status': 2}), 400  # existing user
    elif password != passwordconfirm:
        return jsonify({'status': 3}), 400  # invalid password
    elif not is_email_address_valid(email):
        return jsonify({'status': 4}), 400  # invalid email

    else:
        user = User(username=username, email=email, password=password)
        try:
            db.session.add(user)
            db.session.commit()

            token = generate_confirmation_token(user.email)
            subject = "Please confirm your email"
            body = "Go to {}/confirm/{}".format(app.config["CFG_SITE_URL"], token)
            send_email(user.email, subject, body)
            return jsonify({'status': 0}), 200

        except Exception as e:
            db.session.rollback()  # cancel the transaction
            db.session.flush()  # empty the session
            return jsonify({'status': str(e)}), 400


@user_views.route('/confirm/<token>')
def confirm_email(token):
    try:
        email = confirm_token(token)
    except:
        return jsonify({'status': "The confirmation link is invalid or has expired."}), 400

    if not email:
        return jsonify({'status': "The confirmation link is invalid."}), 400
    user = User.query.filter(User.email == email).one()
    if user.is_active:
        return jsonify({'status': "Account already confirmed. Please login."}), 200  # FIXME: redirect angular
    else:
        user.is_active = True
        user.activated_on = datetime.datetime.now()
        db.session.add(user)
        db.session.commit()
        return jsonify({'status': "You have confirmed your account. Thanks!"}), 200  # FIXME: redirect


@user_views.route('/login', methods=['POST'])
def login():
    user = User.get_user(request.json.get('username'))  # FIXME: Handle case where username is missing
    password = request.json.get('password')
    if not user or password != user.password:
        return jsonify({'status': 5}), 400  # invalid username or password
    else:
        login_user(user)
        user.is_authenticated = True
        db.session.commit()
        return jsonify({'status': 0}), 200  # Logged in successfully.


@user_views.route("/logout", methods=["POST"])
@login_required
def logout():
    user = current_user
    user.is_authenticated = False
    db.session.add(user)
    db.session.commit()
    logout_user()
    return jsonify({'status': 0}), 200  # Logged out successfully.


@user_views.route("/get_account", methods=["POST"])
@login_required
def get_account():
    return jsonify(current_user.to_json())


@user_views.route("/update_account", methods=["POST"])
@login_required
def update_account():
    if request.json:
        user_data = request.json
        user = current_user
        for key in user_data:
            if key != "password":
                user.__setattr__(key, user_data[key])  # !! va modifier le password sans passer par le hash
            else:
                # FIXME: ajouter la modif du password en repassant par le hash
                pass
        try:
            db.session.add(user)
            db.session.commit()
        except:
            db.session.rollback()
            return jsonify({"status": 6}), 400  # can't modify attributes
        return jsonify({"status": 0}), 200
    else:
        return jsonify({"status": 7}), 400  # invalid request, no value in the post
