import flask
from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user
from werkzeug.security import check_password_hash

from database.database import db

from models.User import User

login = Blueprint('login', __name__, template_folder='templates')


def login_form_process(form):
    return redirect(url_for('profile.profile_index'))


@login.route('/', methods=["GET", "POST"])
def login_form_function():
    valid, errors = form_is_valid(flask.request.form)
    if not valid:
        return display_login_form(flask.request.form, errors)
    else:
        return login_form_process(flask.request.form)


def display_login_form(form, errors):
    return render_template('authentication/login.html.jinja2', errors=errors, form=form)


def form_is_valid(form):
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
