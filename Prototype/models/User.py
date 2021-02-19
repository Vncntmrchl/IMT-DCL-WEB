from database.database import db
from flask_login import UserMixin


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    mail = db.Column(db.Text)
    name = db.Column(db.Text)
    username = db.Column(db.Text, unique=True)
    password = db.Column(db.Integer)
