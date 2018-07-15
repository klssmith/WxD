import os

from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()
migrate = Migrate()


from app.main.views import main as main_blueprint # noqa


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI', 'postgresql://localhost/wxd')
    db.init_app(app)
    migrate.init_app(app, db=db)

    app.register_blueprint(main_blueprint)

    return app
