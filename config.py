import os
basedir = os.path.abspath(os.path.dirname(__file__))


CSRF_ENABLED = True
SECRET_KEY = 'you-will-never-guess'
DATABASE = basedir + '/tmp/data.db'
DEBUG = True
