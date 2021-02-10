from flask import Flask, render_template
from profile.profile import profile
from feed.feed import feed

app = Flask(__name__)

# Blueprints
app.register_blueprint(profile, url_prefix='/profile')
app.register_blueprint(feed, url_prefix='')


@app.route('/')
def hello_world():
    return render_template('base.html.jinja2')
