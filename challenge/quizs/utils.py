#coding: utf-8

from werkzeug.utils import import_string
from flask import current_app as app


def load(name):
    quiz_module = app.config.get('CHALLENGE_QUIZ_MODULE', 'challenge.quizs')
    quiz_name = '%s.%s' % (quiz_module, name)
    module = import_string(quiz_name)
    return getattr(module, 'generate', module)
