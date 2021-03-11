from database.database import db
from datetime import datetime
from flask import Blueprint, render_template, jsonify
from flask_login import login_required
# from sqlalchemy_imageattach import entity

post = Blueprint('post', __name__, template_folder='templates')


# TODO add "liked posts list" to User model and check if the user already liked it or not

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Post id, will also be used for unique post url
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # Author id
    username = db.Column(db.String)  # Easier to display username this way (avoid circular import)
    date = db.Column(db.Date, default=datetime.now())
    description = db.Column(db.Text)
    hearts = db.Column(db.Integer)  # The number of "likes" of the post
    current_user_liked_it = db.Column(
        db.Boolean)  # To know if the current user liked this post or not (no multiple likes)

    # picture = entity.image_attachment('Picture')
    # __tablename__ = 'post'

    # TODO Add picture to a post

    def __init__(self, user_id, username, description):
        self.user_id = user_id
        self.username = username
        self.description = description
        self.hearts = 0
        self.current_user_liked_it = False

# class Picture(db.Model, entity.Image):
#     post_id = db.Column(db.Integer, db.ForeignKey(Post.id), primary_key=True)
#     post = db.relationship(Post)
#     __tablename__ = 'post_picture'


@post.route('/heart/<int:post_id>', methods=['POST'])
@login_required
def heart(post_id):
    current_post = db.session.query(Post).get(int(post_id))
    # If the current user has never liked the post, it adds a heart
    # otherwise, it removes it (can't like several time the same post)
    if not current_post.current_user_liked_it:
        current_post.hearts += 1
        current_post.current_user_liked_it = not current_post.current_user_liked_it
    else:
        current_post.hearts -= 1
        current_post.current_user_liked_it = not current_post.current_user_liked_it
    db.session.commit()
    post_card_id = 'post_card_' + str(current_post.id)
    return jsonify('', render_template('post/post.html.jinja2', post=current_post, post_card_id=post_card_id))
