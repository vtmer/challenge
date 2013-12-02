#coding: utf-8

from logging import StreamHandler
from logging.handlers import SMTPHandler as _SMTPHandler


class SMTPHandler(_SMTPHandler):
    '''SMTP logging handler adapter'''

    def __init__(self, *args, **kwargs):
        super(SMTPHandler, self).__init__(*args, **kwargs)
        self._timeout = 15  # give me more time!


class ConsoleMailHandler(StreamHandler):
    '''Console mail mocking handler'''

    def __init__(self, *args, **kwargs):
        stream = kwargs.get('stream')
        super(ConsoleMailHandler, self).__init__(stream)
