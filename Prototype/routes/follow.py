from flask import Blueprint, render_template, jsonify
from flask_login import login_required, current_user
from database.database import db
from models.User import User

follow = Blueprint('follow', __name__, template_folder='templates')


@follow.route('/')
@login_required
def follow_index():
    users = db.session.query(User).all()
    return render_template('profile/follow.html.jinja2', users=users)


@follow.route('/<int:followed_id>', methods=['POST'])
@login_required
def follow_user(followed_id):
    followed = db.session.query(User).get(int(followed_id))
    # If the current user does not follow the selected user, this user is added to the followed list
    # otherwise, it removes it
    if not current_user.is_following(followed):
        current_user.follow(followed)
    else:
        current_user.unfollow(followed)
    db.session.commit()
    return jsonify('', follow_index())
