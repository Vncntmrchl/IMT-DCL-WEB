from flask_login import login_required, current_user, logout_user
from flask import Blueprint, render_template, redirect, url_for

profile = Blueprint('profile', __name__, template_folder='templates')


@profile.route('/')
@login_required
def profile_index():
    return render_template('profile/profile.html.jinja2', name=current_user.name)


@profile.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('connexion.fonction_formulaire_connexion'))