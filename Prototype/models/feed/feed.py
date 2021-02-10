
from flask import Blueprint, render_template
from models.post.post import Post

feed = Blueprint('feed', __name__, template_folder='templates')


@feed.route('/')
def feed_index():
    return render_template('feed/feed.html.jinja2')
