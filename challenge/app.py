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
    from .views import quiz
    app.register_blueprint(quiz.bp, url_prefix='/quiz')

    return app


def register_logging(app):
    import logging.config
    logging.config.dictConfig(app.config['LOGGING_CONFIG'])

    return app
