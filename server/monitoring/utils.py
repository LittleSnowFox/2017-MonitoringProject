# -*- coding: utf-8 -*-
from flask import request, jsonify


class AbstractNotification(object):

    @staticmethod
    def notify(args):
        raise NotImplemented

    def __init__(self):
        self.parameters = []
        self.type = ""


class Email(AbstractNotification):

    def notify(args):
        if not request.json:
            return jsonify({'status': "invalid request"}), 400
        email = request.json.get('email', None)


class Slack(AbstractNotification):

    def notify(args):
        if not request.json:
            return jsonify({'status': "invalid request"}), 400
        token = request.json.get('token', None)
        channel = request.json.get('channel', None)


method_to_class = {"email": Email, "slack": Slack}
