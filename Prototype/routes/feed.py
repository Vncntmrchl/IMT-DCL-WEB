from flask import Blueprint, render_template
from flask_login import login_required, current_user

feed = Blueprint('feed', __name__, template_folder='templates')


@feed.route('/')
@login_required
def feed_index():
    posts = current_user.followed_posts().all()
    return render_template('feed/feed.html.jinja2', posts=posts)
