import os

from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from app.config import configs
from app.datapoint_client.client import DatapointClient


db = SQLAlchemy()
migrate = Migrate()
client = DatapointClient(os.getenv('DATAPOINT_API_KEY'))


from app.main.views import main as main_blueprint # noqa


def create_app():
    app = Flask(__name__)

    app.config.from_object(configs[app.env])

    db.init_app(app)
    migrate.init_app(app, db=db)

    app.register_blueprint(main_blueprint)

    return app
