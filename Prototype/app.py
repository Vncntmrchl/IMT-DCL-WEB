
from flask import Flask
from werkzeug.security import generate_password_hash

from config import Config
from database import database
from flask_login import LoginManager

# Models imports
from database.database import db
from models.User import User
from models.Post import Post

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
        return User.query.get(int(user_id))

    # Finally, we register needed blueprints
    app.register_blueprint(auth, url_prefix='/auth')
    app.register_blueprint(feed, url_prefix='')
    app.register_blueprint(profile, url_prefix='/profile')

    p1 = Post(author='Vincent', description='First post!')
    p2 = Post(author='Vincent', description='Second post!')

    # with app.app_context():
    #     u1 = User(email='john@example.com', username='john',
    #               password=generate_password_hash('petitkebab', method='sha256'))
    #     u2 = User(email='vincent@example.com', username='vincent',
    #               password=generate_password_hash('vincent', method='sha256'))
    #     for user in User.query.all():
    #         print(getattr(user, "username"))
    #
    #     db.session.add(u1)
    #     db.session.add(u2)
    #     print(u1.is_following(u2))
    #     u1.follow(u2)
    #     print(u1.is_following(u2))
    #     print(u1.followed.count(), u1.followed.first().username, u2.followers.count(), u2.followers.first().username)
    #     u1.unfollow(u2)
    #     print(u1.is_following(u2))

    return app
