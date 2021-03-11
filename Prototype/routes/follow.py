from flask import Blueprint, render_template, jsonify
from flask_login import login_required, current_user

from database.database import db
from models.Post import Post, post
from models.User import User

follow = Blueprint('follow', __name__, template_folder='templates')


@follow.route('/')
@login_required
def follow_index():
    users = db.session.query(User).all()
    return render_template('profile/follow.html.jinja2', users=users)


@follow.route('/<int:follower_id>', methods=['POST'])
@login_required
def follow_user(follower_id):
    follower = db.session.query(User).get(int(follower_id))
    # If the current user has never liked the post, it adds a heart
    # otherwise, it removes it (can't like several time the same post)
    if not current_user.is_following(follower):
        current_user.follow(follower)
    else:
        current_user.unfollow(follower)
    db.session.commit()
    return jsonify('', render_template('profile/follow.html.jinja2'))
