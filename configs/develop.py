#coding: utf-8

import os

DEBUG = True

SECRET_KEY = 'haha'

LOGGING_CONFIG = {
    'formatters': {
        'brief': {
            'format': '%(asctime)s %(levelname)s %(name)s %(message)s'
        }
    },
    'filters': [],
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'brief'
        }
    },
    'loggers': {
        'app': {
            'propagate': True,
            'level': 'DEBUG',
            'handlers': ['console']
        }
    },
    'disable_existing_loggers': True,
    'incremental': False,
    'version': 1
}


SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.abspath('data/challenge.db')
