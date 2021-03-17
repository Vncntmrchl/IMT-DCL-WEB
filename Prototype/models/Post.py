from database.database import db
from datetime import datetime
from flask import Blueprint, render_template, jsonify
from flask_login import login_required

post = Blueprint('post', __name__, template_folder='templates')


class Post(db.Model):
    id = db.Column(db.Integer,
                   primary_key=True)  # Post id, will also be used for unique post url and image naming as we don't
    # have a dedicated server to store images for this project
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # Author id
    username = db.Column(db.String)  # Easier to display username this way (avoid circular import)
    date = db.Column(db.Date, default=datetime.now())
    image_name = db.Column(db.String)  # For local storage, post_id + file_extension (.jpg, .png ...)
    description = db.Column(db.Text)
    hearts = db.Column(db.Integer)  # The number of "likes" of the post
    current_user_liked_it = db.Column(
        db.Boolean)  # To know if the current user liked this post or not (no multiple likes)

    def __init__(self, user_id, username, image_name, description):
        self.user_id = user_id
        self.username = username
        self.image_name = image_name
        self.description = description
        self.hearts = 0
        self.current_user_liked_it = False


# We give the post id as an argument in the url to select the right post
@post.route('/heart/<int:post_id>', methods=['POST'])
@login_required
def heart(post_id):
    current_post = db.session.query(Post).get(int(post_id))
    # If the current user has never liked the post, it adds a heart
    # otherwise, it removes it (can't like several times the same post)
    if not current_post.current_user_liked_it:
        current_post.hearts += 1
        current_post.current_user_liked_it = not current_post.current_user_liked_it
    else:
        current_post.hearts -= 1
        current_post.current_user_liked_it = not current_post.current_user_liked_it
    db.session.commit()
    # This string is for the html template that will need a standardized id for the "heart" button
    post_card_id = 'post_card_' + str(current_post.id)
    return jsonify('', render_template('post/post.html.jinja2', post=current_post, post_card_id=post_card_id))
