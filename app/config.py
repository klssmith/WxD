import logging
import os


class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class Production(Config):
    SECRET_KEY = os.getenv('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI')
    LOGLEVEL = logging.WARNING


class Development(Config):
    SECRET_KEY = 'top-secret'
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI', 'postgresql://localhost/wxd')
    LOGLEVEL = logging.DEBUG


class Test(Config):
    SECRET_KEY = 'secret'
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_TEST_DATABASE_URI', 'postgresql://localhost/wxd_test')
    SERVER_NAME = 'wxd.test'
    TESTING = True
    LOGLEVEL = logging.NOTSET


configs = {
    'production': Production,
    'development': Development,
    'test': Test,
}
