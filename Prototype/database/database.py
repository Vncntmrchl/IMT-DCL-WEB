# https://codersdiaries.com/blog/flask-project-structure
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

# We first instantiate a database for our project
db = SQLAlchemy()


# We use this method to initialize the database with the app
# and all the necessary models
def init_app(app):
    db.init_app(app)
    login_manager = LoginManager()
    login_manager.login_view = 'connexion.fonction_formulaire_connexion'
    login_manager.init_app(app)
    db.create_all(app=app)
    from models import User


