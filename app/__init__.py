from flask import Flask
from apscheduler.schedulers.background import BackgroundScheduler
import os
import platform


app = Flask(__name__)
app.config.from_object('config')

from app import views


if platform.system() == 'Linux':
    if not os.path.exists(os.getcwd() + '/' + app.config['DATABASE']):
        views.init_db()
elif platform.system() == 'Windows':
    if not os.path.exists(os.getcwd() + '\\' + app.config['DATABASE'].replace('/', '\\')):
        views.init_db()
else:
    views.init_db()

sched = BackgroundScheduler(timezone='Europe/Moscow')
sched.add_job(views.my_scheduled_job, 'interval', hours=1)
sched.start()
