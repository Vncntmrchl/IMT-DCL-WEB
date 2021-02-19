from flask import Flask
from flask_login import LoginManager

from config import Config
from database import database

# Blueprints imports
from database.database import db
from models.User import User
from routes.login import login
from routes.registration import registration
from routes.profile import profile
from routes.feed import feed


def setup():
    # First, we instantiate a Flask object and configure it
    app = Flask(__name__)
    app.config.from_object(Config)
    #
    app.config['SECRET_KEY'] = 'secret-key-goes-here'
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database/database.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    #
    # Then, we initialize our database
    db.init_app(app)
    login_manager = LoginManager()
    login_manager.login_view = 'login.login_form_function'
    login_manager.init_app(app)

    # Finally, we register needed blueprints
    app.register_blueprint(profile, url_prefix='/profile')
    app.register_blueprint(feed, url_prefix='')
    app.register_blueprint(registration, url_prefix='/registration')
    app.register_blueprint(login, url_prefix='/login')

    # p1 = Post(author='Vincent', description='First post!')
    # p2 = Post(author='Vincent', description='Second post!')

    @login_manager.user_loader
    def load_user(user_id):
        # since the user_id is just the primary key of our user table, use it in the query for the user
        return User.query.get(int(user_id))

    return app


darkTheme = True


def switch_theme():
    global darkTheme
    darkTheme = not darkTheme


