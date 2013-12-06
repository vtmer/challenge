#coding: utf-8

from sqlalchemy.orm import backref

from challenge.db import db

__all__ = ['Stage']


class Stage(db.Model):
    __tablename__ = 'stage'

    id = db.Column(db.Integer, primary_key=True)
    display_name = db.Column(db.String(150), unique=True, nullable=False)
    quiz_name = db.Column(db.String(150), nullable=True)

    prev_stage_id = db.Column(db.Integer, db.ForeignKey('stage.id'))
    # stages are single linked list
    next = db.relationship('Stage', uselist=False, remote_side=[id],
                           backref=backref('prev', uselist=False))

    def __init__(self, display_name, quiz_name, prev_stage=None):
        self.display_name = display_name
        self.quiz_name = quiz_name
        if prev_stage:
            self.prev = prev_stage

    def __str__(self):
        return '<Stage %s %s>' % (self.display_name, self.quiz_name)

    def __repr__(self):
        return self.__str__()

    @property
    def ancestors(self):
        '''ancectors stages

        TODO cache result
        '''
        parents, node = [], self
        while node.prev:
            parents.append(node.prev)
            node = node.prev

        return parents

    @property
    def children(self):
        '''children stages

        TODO cache result
        '''
        children, node = [], self
        while node.next:
            children.append(node.next)
            node = node.next

        return children
