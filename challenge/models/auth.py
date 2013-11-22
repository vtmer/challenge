#coding: utf-8

from hashlib import sha1

from challenge.db import db

__all__ = ['Auth']


class Auth(db.Model):
    __tablename__ = 'auth'

    id = db.Column(db.Integer, primary_key=True)
    password = db.Column(db.String(64), nullable=False)

    def __init__(self, password):
        self.password = Auth.encrypt(password)

    def __str__(self):
        return '<Auth %d>' % (self.id)

    def __repr__(self):
        return self.__str__()

    @staticmethod
    def encrypt(raw):
        return sha1(raw).hexdigest()
