from flask import Flask
import os
from config import DATABASE
from apscheduler.schedulers.background import BackgroundScheduler


app = Flask(__name__)
app.config.from_object('config')

from app import views

if not os.path.isfile(DATABASE):
    views.init_db()

sched = BackgroundScheduler(timezone='Europe/Moscow')
sched.add_job(views.my_scheduled_job, 'interval', hours=1)
sched.start()
