import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or b'dev',
    RECAPTCHA_PUBLIC_KEY = 'FIXME',
    RECAPTCHA_PRIVATE_KEY = 'FIXME'
