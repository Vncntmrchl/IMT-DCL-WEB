from flask import Flask
from werkzeug.security import generate_password_hash

from config import Config
from database import database
from flask_login import LoginManager

# Models imports
from database.database import db
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

    # u1 = User(email='john@example.com', username='john',
    #           password=generate_password_hash('petitkebab', method='sha256'))
    # u2 = User(email='vincent@example.com', username='vincent',
    #           password=generate_password_hash('vincent', method='sha256'))
    # u3 = User(email='samir@example.com', username='samir',
    #           password=generate_password_hash('samirlemeilleur&', method='sha256'))
    #
    # with app.app_context():
    #     for user in User.query.all():
    #         print(getattr(user, "username"))
    #     db.session.add(u1)
    #     db.session.add(u2)
    #     db.session.add(u3)
    #     db.session.commit()
    #     p1 = Post(user_id=u1.get_id(), description='First post!')
    #     p2 = Post(user_id=u2.get_id(), description='Second post!')
    #     p3 = Post(user_id=u3.get_id(), description='vive le python')
    #     p4 = Post(user_id=u3.get_id(), description='trop hâte de donner mon salaire à vincent mon maitre')
    #     u1.follow(u1)
    #     u1.follow(u2)
    #     u2.follow(u2)
    #     u2.follow(u3)
    #     db.session.add(u1)
    #     db.session.add(u2)
    #     db.session.add(u3)
    #     db.session.add(p1)
    #     db.session.add(p2)
    #     db.session.add(p3)
    #     db.session.add(p4)
    #     print(u1.followed_posts().all())
    #     print(u2.followed_posts().all())
    #     print(u1.is_following(u2))
    #     for user in User.query.all():
    #         db.session.delete(user)
    #     for post in Post.query.all():
    #         db.session.delete(post)
    #     db.session.commit()
        # db.session.commit()
    #     u1.follow(u2)
    #     print(u1.is_following(u2))
    #     print(u1.followed.count(), u1.followed.first().username, u2.followers.count(), u2.followers.first().username)
    #     u1.unfollow(u2)
    #     print(u1.is_following(u2))

    return app
