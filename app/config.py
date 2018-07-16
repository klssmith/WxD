import os


class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class Development(Config):
    SECRET_KEY = 'top-secret'
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI', 'postgresql://localhost/wxd')


class Test(Config):
    SECRET_KEY = 'secret'
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_TEST_DATABASE_URI', 'postgresql://localhost/wxd_test')
    SERVER_NAME = 'wxd.test'
    TESTING = True


configs = {
    'development': Development,
    'test': Test,
}
