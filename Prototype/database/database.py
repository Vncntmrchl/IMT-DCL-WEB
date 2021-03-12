# https://codersdiaries.com/blog/flask-project-structure

from flask_sqlalchemy import SQLAlchemy

# We first instantiate a database for our project
db = SQLAlchemy()


# We use this method to initialize the database with the app
# and all the necessary models (we start by "resetting" the database to clean it)
def init_app(app):
    with app.app_context():
        db.init_app(app)
        db.drop_all()
        db.create_all(app=app)
