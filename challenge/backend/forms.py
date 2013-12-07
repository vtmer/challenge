#coding: utf-8

from flask_wtf import Form
from wtforms import PasswordField, TextField, SelectField
from wtforms.validators import DataRequired


class FakeObj(object):
    '''Fake a attr base object from dict'''

    def __init__(self, d):
        self._data = d

    def __getattr__(self, key):
        return self._data[key]


class AuthForm(Form):

    password = PasswordField('password', validators=[DataRequired()])


class UpdatePasswordForm(Form):

    orig_password = PasswordField('orig_password', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])


class QuizForm(Form):

    display_name = TextField('display_name', validators=[DataRequired()])
    quiz_name = TextField('quiz_name')
    prev_quiz = SelectField('prev_quiz', coerce=int,
                            validators=[DataRequired()])

    def prepare_prev_quiz(self, other_quizs, quiz=None):
        pair = lambda x: [(i.id, i.display_name) for i in x]
        not_me_and_children = (lambda me: lambda x: x.id != me.id and
                               x not in me.children)

        quiz = quiz or FakeObj({
            'id': 0,
            'children': []
        })

        self.prev_quiz.choices = pair(filter(not_me_and_children(quiz),
                                             other_quizs))
