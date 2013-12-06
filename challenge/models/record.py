#coding: utf-8

from sqlalchemy.orm import backref

from challenge.db import db

__all__ = ['Record']


class Record(db.Model):
    __tablename__ = 'record'

    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.String(64), nullable=False)
    key = db.Column(db.String(64), nullable=False, unique=True)

    stage_id = db.Column(db.Integer, db.ForeignKey('stage.id'))
    stage = db.relationship('Stage')

    next_record_id = db.Column(db.Integer, db.ForeignKey('record.id'))
    # records are single linked list
    prev = db.relationship('Record', uselist=False, remote_side=[id],
                           backref=backref('next', uselist=False))

    def __init__(self, session_id, key, stage, prev=None):
        self.session_id = session_id
        self.key = key
        self.stage_id = stage.id
        self.prev = prev

    def __str__(self):
        return '<Record %s %s>' % (self.key, self.session_id)

    def __repr__(self):
        return self.__str__()

    @property
    def last(self):
        '''Get last record from the records chains'''
        node = self
        while node.next:
            node = node.next
        return node

    @property
    def first(self):
        '''Get first record from the records chains'''
        node = self
        while node.prev:
            node = node.prev
        return node

    @property
    def is_finish(self):
        return self.last.stage.next is None
