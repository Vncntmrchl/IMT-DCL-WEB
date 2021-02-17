from database.database import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    mail = db.Column(db.Text)
    name = db.Column(db.Text)
    username = db.Column(db.Text)
    password = db.Column(db.Integer)
