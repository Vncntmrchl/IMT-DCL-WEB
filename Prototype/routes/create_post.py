import os

from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import login_required, current_user
from flask_wtf import FlaskForm
from flask_wtf.file import FileRequired
from wtforms import FileField, StringField, SubmitField
from wtforms.validators import InputRequired, Length

from models.Post import Post
from database.database import db
from uploads.uploads import images_upload_set
from config import Config

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
        # We add and commit so that the post gets attributed an id
        db.session.add(new_post)
        db.session.commit()
        image = post_form.image.data
        old_filename, file_extension = os.path.splitext(image.filename)
        image.filename = str(new_post.id)+str(file_extension)
        new_post.image_name = image.filename
        images_upload_set.save(image)
        # We commit again to add the new image name to the post
        db.session.commit()
        return redirect(url_for('profile.profile_index'))
    return render_template('post/create_post.html.jinja2', user=user, post_form=post_form)


# @create_post.route('/', methods=['POST'])
# @login_required
# def add_post():
#     # We start by making sure the POST request contains a file
#     if 'file' not in request.files:
#         flash('Veuillez-ajouter une image.')
#         return redirect(request.url)
#     # If that's the case, we can verify and handle the file
#     file = request.files['file']
#     # Empty file
#     if file.filename == '':
#         flash('Aucune image sélectionnée.')
#         return redirect(request.url)
#     # We now check the extension
#     if file and allowed_file(file.filename):
#         # Let's first secure the filename and get the file extension
#         filename = secure_filename(file.filename)
#         file_extension = filename.split()[-1]
#         # We want the file to have a standard name, which corresponds to the post id
#         data = request.json
#         post = Post(user_id=data["id"], username=data["username"], description=data["description"])
#         new_filename = str(post.id) + str(file_extension)
#         db.session.add(Post)
#         db.session.commit()
#         file.save(os.path.join(Config.UPLOAD_FOLDER, new_filename))
#         return jsonify('', render_template('profile/profile.html.jinja2'))
