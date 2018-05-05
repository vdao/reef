import os
import logging

from logging import FileHandler, StreamHandler, Formatter
from logging.handlers import SysLogHandler

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or b'dev'

    RECAPTCHA_PUBLIC_KEY = 'FIXME'
    RECAPTCHA_PRIVATE_KEY = 'FIXME'

    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
                              'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    LOG_FILE = 'application.log'

    UPLOAD_FOLDER = os.path.join(basedir, 'reef/static/uploads')

    ITEMS_PER_PAGE = 50
