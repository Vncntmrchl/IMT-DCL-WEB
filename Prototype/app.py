
from flask import Flask
from config import Config
from database.database import db

# Blueprints imports
from routes.connexion import connexion
from routes.inscription import inscription
from routes.profile import profile
from routes.feed import feed

# Models import (maybe just for dev tests)
from models.post import Post


def setup():
    # First, we instantiate a Flask object and configure it
    app = Flask(__name__)
    app.config.from_object(Config)
    # Then, we initialize our database
    db.init_app(app)
    # Finally, we register needed blueprints
    app.register_blueprint(profile, url_prefix='/profile')
    app.register_blueprint(feed, url_prefix='')
    app.register_blueprint(inscription, url_prefix='/inscription')
    app.register_blueprint(connexion, url_prefix='/connexion')

    # p1 = Post(author='Vincent', description='First post!')
    # p2 = Post(author='Vincent', description='Second post!')

    # with app.app_context():
    #     db.create_all()
    #     db.session.add(p1, p2)
    #     db.session.commit()

    return app


darkTheme = True


def switch_theme():
    global darkTheme
    darkTheme = not darkTheme
