
from flask import Blueprint, render_template

profile = Blueprint('profile', __name__, template_folder='templates')


@profile.route('/')
def profile_index():
    return render_template('profile/profile.html.jinja2')
