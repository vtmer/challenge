#coding: utf-8

import random


CHARSET = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'


def generate(length):
    return ''.join([random.choice(CHARSET) for i in xrange(length)])
