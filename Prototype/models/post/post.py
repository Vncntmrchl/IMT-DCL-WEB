
from app import database
from datetime import datetime


class Post(database.Model):

    id = database.Column(database.Integer, primary_key=True)  # Post id, will also be used for unique post url
    author = database.Column(database.Integer)  # Author id
    date = database.Column(database.Date, default=datetime.now())
    description = database.Column(database.Text)

    def __init__(self, *args):
        super().__init__(*args)
