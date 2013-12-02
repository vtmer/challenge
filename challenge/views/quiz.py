#coding: utf-8

import logging

from flask import current_app as app
from flask import Blueprint, session, render_template

from challenge.utils import key
from challenge.quizs import load
from challenge.db import db
from challenge.models import Stage, Record


bp = Blueprint('quiz', __name__, template_folder='templates')
logger = logging.getLogger('app')


def generate_session_id():
    return key.generate(app.config['CHALLENGE_SESSION_KEY_LENGTH'])


def generate_key():
    return key.generate(app.config['CHALLENGE_KEY_LENGTH'])


def new_record(stage, session_id=None, prev=None):
    session_id = session_id or generate_session_id()
    while True:
        key = generate_key()
        # TODO use raw sql
        if not Record.query.filter_by(key=key).first():
            break
    record = Record(session_id=session_id, key=key, stage=stage, prev=prev)

    db.session.add(record)
    db.session.commit()

    logger.debug('created new %s' % record)
    return record


def retrieve_record(stage, session_id=None, prev=None):
    record = Record.query.filter_by(stage_id=stage.id,
                                    session_id=session_id).first()
    if not record:
        record = new_record(stage, session_id, prev)

    return record


@bp.errorhandler(404)
def not_your_key(error):
    return render_template('404.html'), 404


@bp.route('/', methods=['GET'])
@bp.route('/start', methods=['GET'])
def start():
    init_stage = app.config['CHALLENGE_FIRST_QUIZ']
    init = Stage.query.filter_by(**init_stage).first_or_404()
    record = new_record(init)
    session['session_id'] = record.session_id

    quiz = load(init.quiz_name)

    return quiz(record.key)


@bp.route('/<string:key>', methods=['GET'])
def quiz(key):
    session_id = session.get('session_id')
    query = {
        'session_id': session_id,
        'key': key
    }
    last_record = Record.query.filter_by(**query).first_or_404()

    if not last_record.stage.next:
        logger.info('%s has finished all quizs!' % session_id)
        return 'You have finished it! Congs!'

    record = retrieve_record(last_record.stage.next, session_id, last_record)
    quiz = load(record.stage.quiz_name)

    return quiz(record.key)
