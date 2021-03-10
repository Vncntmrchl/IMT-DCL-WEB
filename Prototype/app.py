
from flask import Flask
from config import Config
from database import database
from flask_login import LoginManager

# Models imports
from models.User import User
from models.Post import post

# Blueprints imports
from auth.auth import auth
from routes.profile import profile
from routes.feed import feed


def setup():
    # First, we instantiate a Flask object and configure it
    app = Flask(__name__)
    app.config.from_object(Config)
    # Then, we initialize our database and login manager
    database.init_app(app)
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    @login_manager.user_loader
    def load_user(user_id):
        return database.db.session.query(User).get(int(user_id))

    # Finally, we register needed blueprints
    app.register_blueprint(auth, url_prefix='/auth')
    app.register_blueprint(feed, url_prefix='')
    app.register_blueprint(profile, url_prefix='/profile')
    app.register_blueprint(post, url_prefix='/post')

    # with app.app_context():
    #     database.db.create_all()
    #     database.db.session.add(Post(author='Vincent', description='First post!'))
    #     database.db.session.add(Post(author='Vincent', description='Second post!'))
    #     database.db.session.commit()

    return app
