from flask import Blueprint, render_template, redirect, url_for, request, jsonify
from flask_login import login_required, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField
from wtforms.validators import InputRequired, Length

from database.database import db
from models.Comment import Comment

profile = Blueprint('profile', __name__, template_folder='templates')


class CommentForm(FlaskForm):
    # Basically the same as RegistrationForm but we do not need email to login
    body = StringField("body", validators=[InputRequired(), Length(min=1, max=1500)])
    post_id = IntegerField("post_id", validators=[InputRequired()])


@profile.route('/', methods=['GET', 'POST'])
@login_required
def profile_index():
    comment_form = CommentForm()
    posts = current_user.posts
    if comment_form.validate_on_submit():
        print(comment_form.body)
        c = Comment(user_id=current_user.id, post_id=comment_form.post_id.data, body=comment_form.body.data)
        db.session.add(c)
        db.session.commit()
        return redirect(url_for('profile.profile_index'))
    return render_template('profile/profile.html.jinja2', posts=posts, comment_form=comment_form)


@profile.route('/add_comment', methods=['POST'])
@login_required
def add_comment():
    data = request.json
    print(data, "ccccc")
    c = Comment(user_id=data["user_id"], post_id=data["post_id"], body=data["body"])
    db.session.add(c)
    db.session.commit()
    return jsonify('', render_template('profile/profile.html.jinja2'))
