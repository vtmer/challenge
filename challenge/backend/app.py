#coding: utf-8

import functools
import logging

from flask import Blueprint
from flask import request, redirect, url_for, render_template, session, flash

from challenge.db import db
from challenge.models import Auth, Stage, Record


__all__ = ['bp']


bp = Blueprint('backend', __name__, template_folder='templates',
               static_folder='static')
logger = logging.getLogger('app')


def auth_login():
    session['is_login'] = 'yes'


def auth_logout():
    session['is_login'] = 'no'


def is_login():
    return session.get('is_login') == 'yes'


def auth_require(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if not is_login():
            flash('You must login first!', category='error')
            flash(request.url, category='next')
            return redirect(url_for('.auth'))
        return func(*args, **kwargs)
    return wrapper


@bp.route('/auth', methods=['GET', 'POST'])
def auth():
    if request.method == 'POST':
        password = request.form.get('password')
        if not Auth.query.filter_by(password=Auth.encrypt(password)).first():
            flash('Password incorrect!', category='error')
            return redirect(url_for('.auth'))
        auth_login()
        return redirect(request.args.get('next') or url_for('.index'))
    return render_template('auth.html')


@bp.route('/out', methods=['GET'])
@auth_require
def logout():
    auth_logout()
    flash('Log out successfully, see you!', category='success')
    return redirect(url_for('.auth'))


@bp.route('/', methods=['GET'])
@auth_require
def index():
    return render_template('index.html')


@bp.route('/me', methods=['GET', 'POST'])
@auth_require
def me():
    if request.method == 'POST':
        original = request.form.get('orig_password')
        password = request.form.get('password')
        user = Auth.query.filter_by(password=Auth.encrypt(original)).first()
        if user:
            user.password = Auth.encrypt(password)
            db.session.commit()
            auth_logout()
            flash('Password updated, please login again!', category='success')
            return redirect(url_for('.auth'))
        flash('Original password incorrect!', category='error')
        return redirect(url_for('.me'))
    return render_template('me.html')


@bp.route('/quizs', methods=['GET'])
@auth_require
def list_quizs():
    return render_template('quizs.html', quizs=Stage.query.all())


@bp.route('/quiz/<int:quiz_id>', methods=['GET', 'POST'])
@auth_require
def quiz(quiz_id):
    q = Stage.query.filter_by(id=quiz_id).first_or_404()
    if request.method == 'POST':
        # TODO
        # form validation & record validation
        display_name = request.form.get('display_name')
        prev_quiz_id = int(request.form.get('prev_quiz') or 0)
        prev_quiz = Stage.query.filter_by(id=prev_quiz_id).first()
        q.display_name = display_name
        q.prev = prev_quiz
        db.session.commit()
        flash('Quiz\'s informations updated!', category='success')
        return redirect(url_for('.quiz', quiz_id=quiz_id))
    return render_template('quiz.html', quiz=q, quizs=Stage.query.all())


@bp.route('/quiz/<int:quiz_id>/remove', methods=['GET'])
@auth_require
def remove_quiz(quiz_id):
    q = Stage.query.filter_by(id=quiz_id).first_or_404()
    flash('Quiz %s removed successfully!' % q.display_name, category='success')
    db.session.delete(q)
    db.session.commit()
    return redirect(url_for('.list_quizs'))


@bp.route('/quiz/create', methods=['GET', 'POST'])
@auth_require
def create_quiz():
    if request.method == 'POST':
        # TODO
        # form validation & record validation
        display_name = request.form.get('display_name')
        quiz_name = request.form.get('quiz_name')
        prev_quiz_id = int(request.form.get('prev_quiz') or 0)
        prev_quiz = Stage.query.filter_by(id=prev_quiz_id).first()
        q = Stage(display_name, quiz_name, prev_quiz)
        db.session.add(q)
        db.session.commit()
        logger.info('Created %s' % q)
        flash('Created new quiz %s' % display_name, category='success')
        return redirect(url_for('.list_quizs'))
    return render_template('quiz.create.html', quizs=Stage.query.all())


@bp.route('/records', methods=['GET'])
@auth_require
def list_records():
    records = list(set([record.last for record in Record.query.all()]))
    finish_records = filter(lambda x: x.is_finish, records)
    return render_template('records.html', records=records,
                           finish_records=finish_records)


@bp.route('/records/empty', methods=['GET'])
@auth_require
def empty_records():
    # TODO batch expresssion
    for record in Record.query.all():
        db.session.delete(record)
    db.session.commit()
    flash('All records were removed successfully!', category='success')
    return redirect(url_for('.list_records'))
