# -*- coding: utf-8 -*-
import os


class BaseConfig(object):
    """Base configuration."""

    # main config
    DEBUG = False
    BCRYPT_LOG_ROUNDS = 13
    WTF_CSRF_ENABLED = True
    DEBUG_TB_ENABLED = False
    DEBUG_TB_INTERCEPT_REDIRECTS = False

    # mail settings
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False

    # gmail authentication
    MAIL_USERNAME = 'berengere.bouillon@gmail.com'
    MAIL_PASSWORD = 'chimaera74%'

    # mail accounts
    MAIL_DEFAULT_SENDER = 'berengere.bouillon@gmail.com'

    CFG_SITE_URL = 'www.webmonitoring.com'
