from flask import Blueprint, render_template
from flask_login import login_required
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import InputRequired, Length
from models.Post import Post
from database.database import db

search_post = Blueprint('search_post', __name__, template_folder='templates')


class NewSearchForm(FlaskForm):
    description = StringField('Description', validators=[InputRequired(), Length(max=350)])


@search_post.route('/search', methods=['GET', 'POST'])
@login_required
def search():
    search_form = NewSearchForm()
    posts = []
    if search_form.validate_on_submit():
        for post in db.session.query(Post).all():
            for tag in post.tags.split():
                if tag == search_form.description.data:
                    posts.append(post)
                    break
            # We can also look for users
            if post.username == search_form.description.data and post not in posts:
                posts.append(post)
        return render_template('post/search_result.html.jinja2', posts=posts)
    return render_template('post/search_post.html.jinja2', search_form=search_form)
