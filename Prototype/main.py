from app import app, database
from models.profile.profile import profile
from models.feed.feed import feed


# Blueprints
app.register_blueprint(profile, url_prefix='/profile')
app.register_blueprint(feed, url_prefix='')

if __name__ == '__main__':
    app.run()
