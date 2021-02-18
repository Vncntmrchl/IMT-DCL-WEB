import flask
from flask import Blueprint, render_template

from models.User import User
from database.database import db

registration = Blueprint('registration', __name__, template_folder='templates')


def registration_form_process(form):
    return flask.render_template("base.html.jinja2") + flask.request.form.get("username", "") + " now registered."


def add_user_database(form):
    mail = flask.request.form.get("mail", "")
    name = flask.request.form.get("name", "")
    username = flask.request.form.get("username", "")
    password = hash(flask.request.form.get("password", ""))
    new_task = User(mail=mail, name=name, username=username, password=password)
    db.session.add(new_task)
    db.session.commit()
    for user in db.session.query(User).all():
        print(getattr(user, "password"))


def delete_all_user_database():
    for user in db.session.query(User).all():
        db.session.delete(user)
    db.session.commit()


def display_registration_form(form, errors):
    return render_template("registration/registration.jinja2", errors=errors, form=form)


def form_is_valid(form):
    mail = flask.request.form.get("mail", "")
    name = flask.request.form.get("name", "")
    username = flask.request.form.get("username", "")
    password = flask.request.form.get("password", "")

    result = True
    errors = []

    if mail == "":
        result = False
        errors += ["missing 'mail' parameter"]
    if name == "":
        result = False
        errors += ["missing 'name' parameter"]
    if username == "":
        result = False
        errors += ["missing 'username' parameter"]
    if password == "":
        result = False
        errors += ["missing 'password' parameter"]
    if not check_mail(mail):
        result = False
        errors += ["Ce mail est deja utilise"]
    if not check_username(username):
        result = False
        errors += ["Ce nom d'utilisateur est deja utilise"]

    return result, errors


def check_mail(mail):
    for user in db.session.query(User).all():
        if mail == getattr(user, "mail"):
            return False
    return True


def check_username(username):
    for user in db.session.query(User).all():
        if username == getattr(user, "username"):
            return False
    return True


@registration.route('/', methods=["GET", "POST"])
def registration_form_function():
    valid, errors = form_is_valid(flask.request.form)
    if not valid:
        return display_registration_form(flask.request.form, errors)
    else:
        add_user_database(flask.request.form)
        return registration_form_process(flask.request.form)
