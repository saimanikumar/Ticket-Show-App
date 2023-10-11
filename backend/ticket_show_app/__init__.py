import os
from os import path
from flask_restful import Api
from .model import User, Theatre, Show, TicketBooking
from .database import db
from .app import app

from .workers import celer, ContextTask

api = None
celery = None

DB_NAME = "ticket_show.sqlite3"


def create_app():
    if not hasattr(app, 'extensions') or 'sqlalchemy' not in app.extensions:
        db.init_app(app)

    app.app_context().push()
    create_database(app)

    api = Api(app)

    celery = celer

    celery.conf.update(
        broker_url=app.config['CELERY_BROKER_URL'],
        result_backend=app.config['CELERY_RESULT_BACKEND'],
        timezone="Asia/Calcutta",
        enable_utc=False
    )

    celery.Task = workers.ContextTask

    return app, api, celery


def create_database(app):
    basedir = os.path.abspath(os.path.dirname(__file__))
    SQLITE_DB_DIR = os.path.join(basedir, "../db_directory")

    if not path.exists(SQLITE_DB_DIR + DB_NAME):
        db.create_all()

