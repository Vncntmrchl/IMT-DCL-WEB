import os

DB_DIRECTORY = os.path.dirname(os.path.abspath(__name__))


class Config:
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(DB_DIRECTORY, 'database/database.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'SoMuchSecretHere'
    UPLOADED_IMAGES_DEST = 'static/images_storage'
