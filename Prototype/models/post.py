from database.database import db
from datetime import datetime


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Post id, will also be used for unique post url
    author = db.Column(db.Integer)  # Author id
    date = db.Column(db.Date, default=datetime.now())
    description = db.Column(db.Text)

    # TODO Add picture to a post

    def __init__(self, author, description):
        self.author = author
        self.description = description
