from flask import Flask, render_template
from config import Config
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config.from_object(Config)

database = SQLAlchemy(app)

darkTheme = True


def switch_theme():
    global darkTheme
    darkTheme = not darkTheme
