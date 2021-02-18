import flask
from flask import Blueprint, render_template
from database.database import db

from models.User import User

connection = Blueprint('connection', __name__, template_folder='templates')


def connection_form_process(form):
    return flask.render_template("base.html.jinja2") + flask.request.form.get("username", "") + " now connected."


@connection.route('/', methods=["GET", "POST"])
def connection_form_function():
    valid, errors = form_is_valid(flask.request.form)
    if not valid:
        return display_connection_form(flask.request.form, errors)
    else:
        return connection_form_process(flask.request.form)


def display_connection_form(form, errors):
    return render_template('connection/connection.html.jinja2', errors=errors, form=form)


def form_is_valid(form):

    username = flask.request.form.get("username", "")
    password = flask.request.form.get("password", "")
    passw = hash(password)
    result = True
    is_in = False
    u = None
    errors = []
    print(username, "user")
    if username == "":
        errors += ["missing 'username' parameter"]
        result = False
    if password == "":
        errors += ["missing 'password' parameter"]
        result = False
    for user in db.session.query(User).all():
        print(getattr(user, "username"), username)
        if getattr(user, "username") == username:
            is_in = True
            u = user
    if not is_in:
        errors += ["Unknown username"]
        result = False
    if is_in:
        if getattr(u, "password") != passw:
            errors += ["Password doesn't match username"]
            result = False
    return result, errors
