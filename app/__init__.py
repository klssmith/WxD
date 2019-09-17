import logging
import os

from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from pytz import timezone

from app.config import configs
from datapoint_client.client import DatapointClient


db = SQLAlchemy()
migrate = Migrate()
client = DatapointClient(os.getenv('DATAPOINT_API_KEY'))
logger = logging.getLogger(__name__)
local_time = timezone('Europe/London')

from app.main.views import main as main_blueprint # noqa


# logging.basicConfig(filename='example.log', level=logging.DEBUG)

dp_client_logger = logging.getLogger('datapoint_client')

file_handler = logging.FileHandler('example.log')
stream_handler = logging.StreamHandler()

logger.setLevel(logging.DEBUG)
dp_client_logger.setLevel(logging.DEBUG)

logger.addHandler(file_handler)
logger.addHandler(stream_handler)
dp_client_logger.addHandler(stream_handler)


def format_date(datetime):
    datetime = datetime.astimezone(local_time)
    return datetime.strftime('%A %d %b')


def format_time(datetime):
    datetime = datetime.astimezone(local_time)
    return datetime.strftime('%-I%p').lower()


def create_app():
    app = Flask(__name__)

    app.config.from_object(configs[app.env])

    db.init_app(app)
    migrate.init_app(app, db=db)

    app.register_blueprint(main_blueprint)

    app.jinja_env.filters['format_date'] = format_date
    app.jinja_env.filters['format_time'] = format_time

    return app


# def logger_stuff():
#     level = configs[app.env]
