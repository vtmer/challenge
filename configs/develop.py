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
        },
        'mail': {
            'class': 'challenge.utils.mail.ConsoleMailHandler',
            'formatter': 'brief',
            'mailhost': ('smtp.gmail.com', 587),
            'fromaddr': 'somewhere@somehost.org',
            'toaddrs': ['bcxxxxxx+surprise@gmail.com'],
            'subject': '[VTM-CHALLENGE] report',
            'credentials': ('somewhere@somehost.org', 'pwd'),
            'secure': ()
        }
    },
    'loggers': {
        'app': {
            'propagate': True,
            'level': 'DEBUG',
            'handlers': ['console', 'mail']
        }
    },
    'disable_existing_loggers': True,
    'incremental': False,
    'version': 1
}


SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.abspath('data/challenge.db')
