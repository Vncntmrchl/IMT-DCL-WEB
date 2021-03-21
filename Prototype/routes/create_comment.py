from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required, current_user

from database.database import db
from models.Comment import Comment
from models.User import User

create_comment = Blueprint('create_comment', __name__, template_folder='templates')


@create_comment.route('/add_comment', methods=['POST'])
@login_required
def add_comment():
    data = request.json
    user_id = current_user.get_id()
    author = db.session.query(User).get(user_id)
    print(data)
    c = Comment(user_id=author.id, username=author.username, post_id=data["post_id"], body=data["body"])
    db.session.add(c)
    db.session.commit()
    return jsonify('', render_template('feed/feed.html.jinja2'))
