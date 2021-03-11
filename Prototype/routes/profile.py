from flask import Blueprint, render_template
from flask_login import login_required

profile = Blueprint('profile', __name__, template_folder='templates')


@profile.route('/')
@login_required
def profile_index():
    return render_template('profile/profile.html.jinja2')
