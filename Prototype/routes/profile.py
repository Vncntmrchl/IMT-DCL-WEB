from flask import Blueprint, render_template
from flask_login import login_required, current_user

profile = Blueprint('profile', __name__, template_folder='templates')


@profile.route('/')
@login_required
def profile_index():
    posts = current_user.posts
    return render_template('profile/profile.html.jinja2', posts=posts)
