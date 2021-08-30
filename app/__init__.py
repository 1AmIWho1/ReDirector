from flask import Flask
from apscheduler.schedulers.background import BackgroundScheduler
import os
import platform


app = Flask(__name__)
app.config.from_object('config')

from app import views


if not os.path.exists(app.config['DATABASE']):
    views.init_db()


sched = BackgroundScheduler(timezone='Europe/Moscow')
sched.add_job(views.my_scheduled_job, 'interval', hours=1)
sched.start()
