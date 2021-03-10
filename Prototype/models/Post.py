from database.database import db
from datetime import datetime


# TODO add "liked posts list" to User model and check if the user already liked it or not


# from sqlalchemy_imageattach import entity


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Post id, will also be used for unique post url
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # Author id
    date = db.Column(db.Date, default=datetime.now())
    description = db.Column(db.Text)
    hearts = db.Column(db.Integer)  # The number of "likes" of the post
    current_user_liked_it = db.Column(
        db.Boolean)  # To know if the current user liked this post or not (no multiple likes)

    # picture = entity.image_attachment('Picture')
    # __tablename__ = 'post'

    # TODO Add picture to a post

    def __init__(self, author, description):
        self.user_id = author
        self.description = description
        self.hearts = 0
        self.current_user_liked_it = False

    def add_heart(self):
        # TODO adapt this function with user liked posts list
        if not self.current_user_liked_it:
            self.hearts += 1
            self.current_user_liked_it = True

# class Picture(db.Model, entity.Image):
#     post_id = db.Column(db.Integer, db.ForeignKey(Post.id), primary_key=True)
#     post = db.relationship(Post)
#     __tablename__ = 'post_picture'
