from flask import Flask
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


def create_app():
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object('config.Config')

    db.init_app(app)

    with app.app_context():
        from . import views  # Import routes
        db.create_all()  # Create sql tables for our data models

        return app

'''
from apscheduler.schedulers.background import BackgroundScheduler
import os


app = Flask(__name__)
app.config.from_object('config')

from ReDirector import views


if not os.path.exists(app.config['DATABASE']):
    views.init_db()


sched = BackgroundScheduler(timezone='Europe/Moscow')
sched.add_job(views.my_scheduled_job, 'interval', hours=1)
sched.start()
'''