from flask import render_template, redirect, url_for, Blueprint, flash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, Length
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user
from models.User import User
from database.database import db

auth = Blueprint('auth', __name__, template_folder='templates')


# First we create the classes used to register and login on our app

class RegistrationForm(FlaskForm):
    email = StringField('E-mail',
                        validators=[InputRequired(), Length(max=25)])
    username = StringField("Nom d'utilisateur", validators=[InputRequired(), Length(min=5, max=12)])
    password = PasswordField('Mot de passe', validators=[InputRequired(), Length(min=8, max=100)])


class LoginForm(FlaskForm):
    # Basically the same as RegistrationForm but we do not need email to login
    username = StringField("Nom d'utilisateur", validators=[InputRequired(), Length(min=5, max=12)])
    password = PasswordField('Mot de passe', validators=[InputRequired(), Length(min=8, max=100)])


# Then we create the routes to manage registering and logging in


@auth.route('/register', methods=['GET', 'POST'])
def register():
    registration_form = RegistrationForm()
    # If the user validates the form, we can process it and register him if it is valid
    if registration_form.validate_on_submit():
        # We secure the password by hashing it
        user = User(email=registration_form.email.data, username=registration_form.username.data,
                    password=generate_password_hash(registration_form.password.data, method='sha256'))
        # And we register the user in the database
        db.session.add(user)
        db.session.commit()
        # We can now redirect the user to the login page
        return redirect(url_for('auth.login'))
    else:
        flash(
            "Rappel : votre nom d'utilisateur doit contenir entre 5 et 12 caractères et votre mot de passe au moins 8 "
            "caractères.")
    # Form given as an argument so that if the form is not valid, all input data won't be reset
    return render_template('authentication/registration.jinja2', registration_form=registration_form)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm()
    # If the user validates the form
    if login_form.validate_on_submit():
        # Usernames are unique so if we find a match we can process the form
        user = db.session.query(User).filter_by(username=login_form.username.data).first()
        if user:
            # We check if the given password is correct
            if check_password_hash(user.password, login_form.password.data):
                # If it's the case, the user is logged in and we get him to the feed
                login_user(user)
                return redirect(url_for('feed.feed_index'))
            else:
                flash("Erreur ! Mot de passe incorrect.")
        else:
            flash("Erreur ! Ce nom d'utilisateur n'existe pas.")
        # If there is no such username we redirect the user to the login page
        # Form given as an argument so that if the form is not valid, all input data won't be reset
        return render_template('authentication/login.html.jinja2', login_form=login_form)
    # Form given as an argument so that if the form is not valid, all input data won't be reset
    return render_template('authentication/login.html.jinja2', login_form=login_form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('feed.feed_index'))
