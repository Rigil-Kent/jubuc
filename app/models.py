from app import db, app
from datetime import datetime
from flask_login import UserMixin
from app import login
from werkzeug.security import check_password_hash, generate_password_hash


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True)
    pass_hash = db.Column(db.String(128))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    first_name = db.Column(db.String(64))
    last_name = db.Column(db.String(64))
    email = db.Column(db.String(256))
    pass_hash = db.Column(db.String(128))


    def set_password(self, password):
        self.pass_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.pass_hash, password)


@login.user_loader
def load_user(id):
    return db.session.query(User).get(int(id))

class Administrator(db.Model):  
    # the admin user will create a User object for the owner
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    first_name = db.Column(db.String(64))
    last_name = db.Column(db.String(64))
    email = db.Column(db.String(256))
    pass_hash = db.Column(db.String(128))

    # Front Page settings
    site_title = db.Column(db.String(64))
    site_logo_text = db.Column(db.String(28))
    site_logo_image = db.Column(db.String(256))
    jumbotron_image = db.Column(db.String(256))
    site_dominant_color = db.Column(db.String)
    site_accent_color = db.Column(db.String)
    site_background_color = db.Column(db.String)

    #social links
    facebook = db.Column(db.String(128))
    twitter = db.Column(db.String(128))
    instagram = db.Column(db.String(128))
    soundcloud = db.Column(db.String(128))
    youtube = db.Column(db.String(128))
    spotify = db.Column(db.String(128))

    #twitter integration
    twitter_consumer_key = db.Column(db.String(256))
    twitter_consumer_key_secret = db.Column(db.String(256))
    twitter_access_token = db.Column(db.String(256))
    twitter_access_token_secret = db.Column(db.String(256))



    def set_password(self, password):
        self.pass_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.pass_hash, password)


class Audio(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), index=True)
    file = db.Column(db.String(256))
    album_art = db.Column(db.String(256))
    is_active = db.Column(db.Boolean, index=True, default=False)
    active = db.relationship('Active', backref="audio", uselist=False)

class Active(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    track_id = db.Column(db.Integer, db.ForeignKey('audio.id'))