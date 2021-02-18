import flask
from flask import Blueprint, render_template

from models.User import User
from models.post import Post
from database.database import db

connexion = Blueprint('connexion', __name__, template_folder='templates')


@connexion.route('/', methods=["GET", "POST"])
def fonction_formulaire_connexion():
    form_est_valide, errors = formulaire_est_valide(flask.request.form)
    print(form_est_valide)
    if not form_est_valide:
        return afficher_formulaire_connexion(flask.request.form, errors)
    else:
        return traitement_formulaire_inscription(flask.request.form)


def afficher_formulaire_connexion(form, errors):
    return render_template('connexion/connexion.html.jinja2', errors=errors, form=form)


def formulaire_est_valide(form):

    username = flask.request.form.get("username", "")
    password = flask.request.form.get("password", "")
    passw = hash(password)
    result = True
    isIn = False
    u = None
    errors = []
    print(username,"user")
    if username == "":
        errors += ["missing 'username' parameter"]
        result = False
    if password == "":
        errors += ["missing 'password' parameter"]
        result = False
    for user in User.query.all():
        print(getattr(user, "username"), username)
        if getattr(user, "username") == username:
            isIn = True
            u = user
    if not isIn:
        errors += ["Unknown username"]
        result = False
    if isIn:
        if getattr(u, "password") != passw:
            errors += ["Password doesn't match username"]
            result = False
    return result, errors


def traitement_formulaire_connexion(form):
    return flask.render_template("base.html.jinja2") + "félicitation " + flask.request.form.get("username", "") + " tu es maintenant connecté"