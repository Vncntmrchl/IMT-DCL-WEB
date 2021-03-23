from flask import Blueprint, render_template
from flask_login import login_required, current_user
from database.database import db
from models.Post import Post
import os

profile = Blueprint('profile', __name__, template_folder='templates')


@profile.route('/')
@login_required
def profile_index():
    app_path = os.path.dirname(os.path.abspath(__name__))
    images_path = os.path.join(app_path, 'static/images_storage')

    # We'll consider that the user has seen all posts in his feed as well as its own posts
    posts_user = db.session.query(Post).filter(Post.user_id == current_user.id)
    posts_in_feed = current_user.followed_posts()
    posts_global = db.session.query(Post)

    number_images_user = posts_user.count()
    number_images_seen = posts_in_feed.count() + number_images_user
    number_images_global = posts_global.count()
    images_global_size, images_user_size, images_seen_size = 0, 0, 0

    for post in posts_global:
        images_global_size += os.path.getsize(os.path.join(images_path, post.image_name))
    for post in posts_user:
        images_user_size += os.path.getsize(os.path.join(images_path, post.image_name))
    for post in posts_in_feed:
        images_seen_size += os.path.getsize(os.path.join(images_path, post.image_name))
    images_seen_size += images_user_size  # The user also saw its own posts

    images_global_size = str(round(images_global_size / (1024 * 1024), 3))  # Convert to megabytes
    images_user_size = str(round(images_user_size / (1024 * 1024), 3))  # Convert to megabytes
    images_seen_size = str(round(images_seen_size / (1024 * 1024), 3))

    return render_template('profile/profile.html.jinja2', posts=posts_user, number_images_user=number_images_user,
                           number_images_global=number_images_global, number_images_seen=number_images_seen,
                           images_global_size=images_global_size,
                           images_user_size=images_user_size, images_seen_size=images_seen_size)
