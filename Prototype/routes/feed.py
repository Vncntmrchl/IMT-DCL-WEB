
from flask import Blueprint, render_template
from models.Post import Post
from database.database import db

feed = Blueprint('feed', __name__, template_folder='templates')


@feed.route('/')
def feed_index():
    posts = db.session.query(Post).all()
    return render_template('feed/feed.html.jinja2', posts=posts)


@feed.route('/test')
def navbar_test():
    return render_template('navigation.html.jinja2')
