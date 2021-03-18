from flask import Flask
from werkzeug.security import generate_password_hash

from config import Config
from flask_login import LoginManager
from flask_uploads import configure_uploads

# Models imports
from database.database import db, db_init_app
from models.Comment import Comment
from uploads.uploads import images_upload_set
from models.User import User
from models.Post import Post, post

# Blueprints imports
from auth.auth import auth
from routes.create_post import create_post
from routes.follow import follow
from routes.profile import profile
from routes.feed import feed


def setup():
    # First, we instantiate a Flask object and configure it
    app = Flask(__name__)
    app.config.from_object(Config)
    # Then, we initialize our database, login manager and image upload system
    db_init_app(app)
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    configure_uploads(app, images_upload_set)

    @login_manager.user_loader
    def load_user(user_id):
        return db.session.query(User).get(int(user_id))

    # Finally, we register needed blueprints
    app.register_blueprint(auth, url_prefix='/auth')
    app.register_blueprint(feed, url_prefix='')
    app.register_blueprint(profile, url_prefix='/profile')
    app.register_blueprint(post, url_prefix='/post')
    app.register_blueprint(follow, url_prefix='/follow')
    app.register_blueprint(create_post, url_prefix='/create_post')

    # Here we create some tests models
    with app.app_context():
        test = User(email='testtest@example.com', username='testtest',
                    password=generate_password_hash('testtest', method='sha256'))
        u1 = User(email='john@example.com', username='john',
                  password=generate_password_hash('petitkebab', method='sha256'))
        u2 = User(email='vincent@example.com', username='vincent',
                  password=generate_password_hash('vincent', method='sha256'))
        u3 = User(email='samir@example.com', username='samir',
                  password=generate_password_hash('samirlemeilleur', method='sha256'))

        db.session.add_all([test, u1, u2, u3])
        db.session.commit()
        p1 = Post(user_id=u1.get_id(), username=u1.username, image_name='1.jpg', description='First post!')
        p2 = Post(user_id=u2.get_id(), username=u2.username, image_name='2.jpg', description='Second post!')
        p3 = Post(user_id=u3.get_id(), username=u3.username, image_name='3.jpg', description='vive le python')
        p4 = Post(user_id=u3.get_id(), username=u3.username, image_name='4.jpg', description='cqfd')
        u3.follow(u2)
        u1.follow(u2)
        u2.follow(u2)
        u3.follow(u3)
        db.session.add_all([p1, p2, p3, p4])
        u1.follow(u2)
        db.session.commit()
        c1 = Comment(user_id=u3.get_id(), body="1st comment", post_id=p2.id)
        c2 = Comment(user_id=u3.get_id(), body="2nd comment", post_id=p2.id)
        c3 = Comment(user_id=u2.get_id(), body="It do be like that sometime", post_id=p1.id)
        db.session.add_all([c1, c2, c3])
        db.session.commit()
        for comment in Comment.query.all():
            print(comment.body)
        for p in Post.query.all():
            for c in p.comments:
                print(p.id, c.body)
    return app
