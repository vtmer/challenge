#coding: utf-8

from flask.ext.script import Manager

from challenge import app as server_app
from configs import develop


app = server_app.build(**develop.__dict__)
manager = Manager(app)


@manager.command
def run():
    app.run(host='0.0.0.0', port=9003, debug=True)


if __name__ == '__main__':
    manager.run()
