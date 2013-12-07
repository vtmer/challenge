#coding: utf-8

import os

from flask import Flask, session


def build(**settings):
    app = Flask(__name__)

    app.config.from_pyfile(os.path.abspath('./configs/settings.py'))
    app.config.from_envvar('CHALLENGE_CONFIG', silent=True)
    app.config.update(settings)

    register_db(app)
    register_logging(app)
    register_blueprint(app)

    @app.before_first_request
    def init_app():
        session.permanent = True

    return app


def register_db(app):
    from .db import db
    db.init_app(app)
    db.app = app

    return app


def register_blueprint(app):
    from .quizs import bp as quiz_bp
    app.register_blueprint(quiz_bp, url_prefix='/quiz')

    from .backend import bp as backend_bp
    app.register_blueprint(backend_bp, url_prefix='/backend')

    return app


def register_logging(app):
    import logging.config
    logging.config.dictConfig(app.config['LOGGING_CONFIG'])

    return app
