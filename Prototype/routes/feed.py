from flask import Blueprint, render_template
from models.Post import Post
from database.database import db
from flask_login import login_required

feed = Blueprint('feed', __name__, template_folder='templates')


@feed.route('/')
@login_required
def feed_index():
    posts = db.session.query(Post).all()
    return render_template('feed/feed.html.jinja2', posts=posts, add_heart=add_heart)


def add_heart(post_id):
    # TODO adapt this function with user liked posts list
    post = db.session.query(Post).get(int(post_id))
    if post:
        if not post.current_user_liked_it:
            post.hearts += 1
            post.current_user_liked_it = True
