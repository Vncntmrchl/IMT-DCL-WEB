
from flask import Flask
from config import Config
from database import database

# Blueprints imports
from routes.connection import connection
from routes.registration import registration
from routes.profile import profile
from routes.feed import feed


def setup():
    # First, we instantiate a Flask object and configure it
    app = Flask(__name__)
    app.config.from_object(Config)
    # Then, we initialize our database
    database.init_app(app)
    # Finally, we register needed blueprints
    app.register_blueprint(profile, url_prefix='/profile')
    app.register_blueprint(feed, url_prefix='')
    app.register_blueprint(registration, url_prefix='/registration')
    app.register_blueprint(connection, url_prefix='/connection')

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
