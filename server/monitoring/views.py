# -*- coding: utf-8 -*-
from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from .models import WebSite, Notification, website_has_name, website_has_notification
from server.run import db
from .utils import method_to_class
import requests


monitoring_views = Blueprint('web_views', __name__)


@monitoring_views.route('/registerwebsite', methods=['POST'])
@login_required
def registerwebsite():
    if not request.json:
        return jsonify({'status': "invalid request"}), 400
    url = request.json.get('url', None)
    name = request.json.get('name', None)
    if url is None:
        return jsonify({'status': 1}), 400  # missing arguments
    elif requests.get(url).status_code >= 400:  # check if website is valid
        return jsonify({'status': 'x'}), 400  # invalid adress or inaccessible
        # request.get(url)
        # 404 site n'existe pas
        # exception timeout, site inaccessible
    else:
        user = current_user.user_id
        if name is None:
            name = url
        try:
            website = WebSite.query.filter(url == url).one()
        except:
            website = WebSite(url=url)

        try:
            #db.session.bulk_save_objects([website])
            db.session.add(website)
            db.session.commit()
            websitehasname = website_has_name.insert().values(website_id=website.website_id, user_id=user, name=name)
            db.engine.execute(websitehasname)
            return jsonify({'status': 0}), 200
        except Exception as e:
            db.session.rollback()  # cancel the transaction
            db.session.flush()  # empty the session
            return jsonify({'status': str(e)}), 400


@monitoring_views.route('/registernotification', methods=['POST'])
@login_required
def registernotification():
    if not request.json:
        return jsonify({'status': "invalid request"}), 400
    method = request.json.get('method', None)
    url = request.json.get('url', None)
    if method is None or url is None:
        return jsonify({'status': 1}), 400  # missing arguments

    # get arguments according to the method type defined by the classes
    else:
        user = current_user.user_id
        website = WebSite.query.filter(url == url).one()

        method_arguments = dict()
        arguments = method_to_class[method]().parameters  # get arguments for the method in a list
        for arg in arguments:
            method_arguments[arg] = request.json.get(arg, None)
            if method_arguments[arg] is None:
                return jsonify({'status': 1}), 400  # missing arguments

        notification = Notification(method=method, method_arguments=method_arguments, user_id=user)

        try:
            db.session.add(notification)
            db.session.commit()
            webSitehasnotification = website_has_notification.insert().values(website_id=website.website_id, notification_id=notification.notification_id)
            db.engine.execute(webSitehasnotification)
            return jsonify({'status': 0}), 200
        except Exception as e:
            db.session.rollback()  # cancel the transaction
            db.session.flush()  # empty the session
            return jsonify({'status': str(e)}), 400
