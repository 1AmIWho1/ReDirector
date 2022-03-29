from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_apscheduler import APScheduler
from datetime import datetime as dt


db = SQLAlchemy()
scheduler = APScheduler()


@scheduler.task('interval', id='delete', minutes=1)
def delete_expired_aliases():
    from . import models
    expired = db.session.query(models.Alias).filter(models.Alias.expiration <= dt.now()).all()
    for alias in expired:
        db.session.delete(alias)
    db.session.commit()


def create_app():
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object('config.Config')

    db.init_app(app)
    scheduler.init_app(app)
    scheduler.start()

    with app.app_context():
        from . import views
        db.create_all()
    db.app = app

    return app
