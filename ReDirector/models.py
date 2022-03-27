from . import db


class Alias(db.Model):

    __tablename__ = 'aliases'
    id = db.Column(db.Integer, primary_key=True)
    full = db.Column(db.String(64), index=False, unique=False, nullable=False)
    alias = db.Column(db.String(64), index=True, unique=True, nullable=False)
    password = db.Column(db.String(64), index=True, unique=True, nullable=False)
    created = db.Column(db.DateTime, index=False, unique=False, nullable=False)

    def __repr__(self):
        return '{}'.format(self.full)
