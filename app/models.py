from app import db


class Path(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full = db.Column(db.String(2048), unique=True, nullable=False)
    shorten_path = db.Column(db.String(64), unique=True, nullable=False)
    password = db.Column(db.String(32), unique=True, nullable=True)
