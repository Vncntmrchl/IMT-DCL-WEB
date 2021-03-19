import os

from flask import Blueprint, render_template, redirect, url_for, jsonify, request
from flask_login import login_required, current_user
from flask_wtf import FlaskForm
from flask_wtf.file import FileRequired
from wtforms import FileField, StringField, SubmitField
from wtforms.validators import InputRequired, Length

from models.Post import Post
from database.database import db
from uploads.uploads import images_upload_set

create_post = Blueprint('create_post', __name__, template_folder='templates')


class NewPostForm(FlaskForm):
    image = FileField('Image', validators=[FileRequired()])
    description = StringField('Description', validators=[InputRequired(), Length(max=350)])
    submit = SubmitField('Submit')


@create_post.route('/', methods=['GET', 'POST'])
@login_required
def new_post_form():
    user = current_user
    post_form = NewPostForm()
    if post_form.validate_on_submit():
        # We first create the post, then process the image to give it the correct name
        new_post = Post(user_id=user.id, username=user.username, image_name='', description=post_form.description.data)
        # We add and commit so that the post gets attributed an id in the database
        db.session.add(new_post)
        db.session.commit()
        image = post_form.image.data
        old_filename, file_extension = os.path.splitext(image.filename)
        image.filename = str(new_post.id) + str(file_extension)
        new_post.image_name = image.filename
        images_upload_set.save(image)
        # We commit again to add the new image name to the post
        db.session.commit()
        return redirect(url_for('profile.profile_index'))
    return render_template('post/create_post.html.jinja2', user=user, post_form=post_form)


@create_post.route('/del_post', methods=['DELETE'])
@login_required
def del_post():
    post_id = request.json["id"]
    # An user can only delete its own posts
    current_post = db.session.query(Post).get(int(post_id))
    if current_post.user_id == current_user.id:
        db.session.query(Post).filter(Post.id == post_id).delete()
        db.session.commit()
    return jsonify('', render_template('profile/profile.html.jinja2'))
