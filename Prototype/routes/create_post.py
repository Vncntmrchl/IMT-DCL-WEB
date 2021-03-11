from flask import Blueprint, render_template, jsonify, request
from models.Post import Post
from database.database import db
from flask_login import login_required, current_user

create_post = Blueprint('create_post', __name__, template_folder='templates')


@create_post.route('/')
@login_required
def create_post_index():
    user = current_user
    return render_template('post/create_post.html.jinja2', user=user)


@create_post.route('/', methods=['POST'])
@login_required
def add_post():
    data = request.json
    print(data)
    post = Post(user_id=data["id"], username=data["username"], description=data["description"])
    db.session.add(post)
    db.session.commit()
    return jsonify('', render_template('profile/profile.html.jinja2'))
