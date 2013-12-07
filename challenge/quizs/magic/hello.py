#coding: utf-8

from flask import render_template


def generate(key):
    return render_template('hello.html', key=key)
