from database.database import db
from flask_login import UserMixin


class User(db.Model, UserMixin):
    # db.Model is necessary to store data in the database
    # UserMixin is here to use the model for login and sessions
    # email and username must be unique and have a maximum length
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(25), unique=True)
    username = db.Column(db.String(10), unique=True)
    password = db.Column(db.String(100))
    posts = db.relationship('Post', backref='author', lazy='dynamic')
