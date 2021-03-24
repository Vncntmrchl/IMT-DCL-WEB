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
from routes.create_comment import create_comment
from routes.search_post import search_post


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
    app.register_blueprint(create_comment, url_prefix='/create_comment')
    app.register_blueprint(search_post, url_prefix='/search_post')

    # Here we create some demo models
    with app.app_context():
        test = User(email='euryclee@example.com', username='Euryclée',
                    password=generate_password_hash('eurycleemdp', method='sha256'))
        u1 = User(email='john@example.com', username='John',
                  password=generate_password_hash('johnmdp', method='sha256'))
        u2 = User(email='esteban@example.com', username='Esteban',
                  password=generate_password_hash('estebanmdp', method='sha256'))
        u3 = User(email='Samir@example.com', username='Samir',
                  password=generate_password_hash('samirmdp', method='sha256'))
        u4 = User(email='brittany@example.com', username='Brittany',
                  password=generate_password_hash('brittanymdp', method='sha256'))
        db.session.add_all([test, u1, u2, u3, u4])
        u3.follow(u2)
        u1.follow(u2)
        u2.follow(u2)
        u3.follow(u3)
        u1.follow(u2)
        u1.follow(u4)
        db.session.commit()

        p1 = Post(user_id=u1.get_id(), username=u1.username, image_name='1.jpg',
                  description='Une superbe vue de la plage !', tags="plage mer", hearts=12)
        p2 = Post(user_id=u2.get_id(), username=u2.username, image_name='2.jpg', description="Vive l'espace",
                  tags="espace galaxie", hearts=23)
        p3 = Post(user_id=u3.get_id(), username=u3.username, image_name='3.jpg', description='Photo de nuit.',
                  tags="nuit ciel", hearts=7)
        p4 = Post(user_id=u3.get_id(), username=u3.username, image_name='4.jpg',
                  description='Souvenir de mon séjour à la montagne.', tags="montagnes vacances", hearts=9)
        p5 = Post(user_id=u4.get_id(), username=u4.username, image_name='5.gif',
                  description='Chill bears.', tags="chill ours", hearts=141)
        p6 = Post(user_id=u1.get_id(), username=u1.username, image_name='6.jpg',
                  description='Trop classe le Pape', tags="voiture pape", hearts=36)
        p7 = Post(user_id=u2.get_id(), username=u2.username, image_name='7.jpg',
                  description="J'adore les glaces !", tags="glace glaces", hearts=25)
        p8 = Post(user_id=u3.get_id(), username=u3.username, image_name='8.jpg',
                  description='Lever de soleil sur la mer', tags="soleil mer vacances", hearts=59)
        db.session.add_all([p1, p2, p3, p4, p5, p6, p7, p8])
        db.session.commit()

        c1 = Comment(user_id=u3.get_id(), username=u3.username, body="trop b1 cette tof omg", post_id=p4.id)
        c2 = Comment(user_id=u3.get_id(), username=u3.username, body="les rageux diront photoshop", post_id=p4.id)
        c3 = Comment(user_id=u2.get_id(), username=u2.username, body="It do be like that sometime", post_id=p1.id)
        db.session.add_all([c1, c2, c3])
        db.session.commit()
    return app
