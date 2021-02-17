import flask
from flask import Blueprint, render_template

from models.User import User
from models.post import Post
from database.database import db

inscription = Blueprint('inscription', __name__, template_folder='templates')


def traitement_formulaire_inscription(form):
    return "super nickel !"


def add_user_database(form):
    mail = flask.request.form.get("mail", "")
    name = flask.request.form.get("name", "")
    username = flask.request.form.get("username", "")
    password = hash(flask.request.form.get("password", ""))
    new_task = User(mail=mail, name=name, username=username, password=password)
    db.session.add(new_task)
    db.session.commit()
    for user in User.query.all():
        print(getattr(user, "password"))


def delete_data_base():
    for user in User.query.all():
        db.session.delete(user)
    db.session.commit()


def afficher_formulaire_inscription(form, errors):
    return flask.render_template("inscription/inscription.html.jinja2", errors=errors, form=form)


def formulaire_est_valide(form):
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
    for user in User.query.all():
        if mail == getattr(user, "mail"):
            return False
    return True


def check_username(username):
    for user in User.query.all():
        if username == getattr(user, "username"):
            return False
    return True


@inscription.route('/', methods=["GET", "POST"])
def fonction_formulaire_inscription():
    form_est_valide, errors = formulaire_est_valide(flask.request.form)
    if not form_est_valide:
        return afficher_formulaire_inscription(flask.request.form, errors)
    else:
        add_user_database(flask.request.form)
        return traitement_formulaire_inscription(flask.request.form)
