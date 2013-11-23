#coding: utf-8

from challenge import app as server_app
from configs import production


app = server_app.build(**production.__dict__)
