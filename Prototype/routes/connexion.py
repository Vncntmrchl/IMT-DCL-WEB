import flask
import flask_login
from flask import Blueprint, render_template, flash, redirect, url_for, request
from flask_login import login_user
from werkzeug.security import generate_password_hash, check_password_hash

from models.User import User

connexion = Blueprint('connexion', __name__, template_folder='templates')


@connexion.route('/', methods=["GET", "POST"])
def fonction_formulaire_connexion():
    form_est_valide, errors = formulaire_est_valide(flask.request.form)
    if not form_est_valide:
        return afficher_formulaire_connexion(flask.request.form, errors)
    else:
        return traitement_formulaire_connexion(flask.request.form)


def afficher_formulaire_connexion(form, errors):
    return render_template('connexion/connexion.html.jinja2', errors=errors, form=form)


def formulaire_est_valide(form):
    username = flask.request.form.get("username", "")
    password = flask.request.form.get("password", "")
    remember = True if request.form.get('remember') else False
    errors = []
    if username == "":
        errors += ["missing 'username' parameter"]
    if password == "":
        errors += ["missing 'password' parameter"]
    user = User.query.filter_by(username=username).first()
    if not user or not check_password_hash(user.password, password):
        flash('Please check your login details and try again.')
        return False, errors
    login_user(user, remember=remember)
    return True, errors


def traitement_formulaire_connexion(form):

    return redirect(url_for('profile.profile_index'))