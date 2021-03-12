from database.database import db
from flask_login import UserMixin
from models.Followers import followers
from models.Post import Post


class User(db.Model, UserMixin):
    # db.Model is necessary to store data in the database
    # UserMixin is here to use a standard model for login and sessions
    # email and username must be unique and have a maximum length
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(25), unique=True)
    username = db.Column(db.String(10), unique=True)
    password = db.Column(db.String(100))
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    followed = db.relationship('User',
                               secondary=followers,
                               primaryjoin=(followers.c.follower_id == id),
                               secondaryjoin=(followers.c.followed_id == id),
                               backref=db.backref('followers', lazy='dynamic'),
                               lazy='dynamic')

    def follow(self, user):
        if not self.is_following(user):
            self.followed.append(user)
            db.session.commit()
            return self

    def unfollow(self, user):
        if self.is_following(user):
            self.followed.remove(user)
            db.session.commit()
            return self

    def is_following(self, user):
        # TODO Correct the filter unresolved attribute reference
        return self.followed.filter(followers.c.followed_id == user.id).count() > 0

    def followed_posts(self):
        # To get the list of all posts made by people the current user follows
        return db.session.query(Post).join(followers, (followers.c.followed_id == Post.user_id)).filter(
            followers.c.follower_id == self.id).order_by(Post.date.desc())
