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
local_time = timezone('Europe/London')

from app.main.views import main as main_blueprint # noqa


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
