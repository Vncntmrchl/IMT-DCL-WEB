from flask import Blueprint, render_template, request, jsonify
from models.Post import Post
from database.database import db
from flask_login import login_required

feed = Blueprint('feed', __name__, template_folder='templates')


@feed.route('/')
@login_required
def feed_index():
    posts = db.session.query(Post).all()
    return render_template('feed/feed.html.jinja2', posts=posts)
