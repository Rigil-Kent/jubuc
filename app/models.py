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
    posts = db.relationship('Post', backref="author", lazy="dynamic")
    shows = db.relationship('Show', backref="host", lazy="dynamic")
    photos = db.relationship('Photo', backref="owner", lazy="dynamic")


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
    jumbotron_header = db.Column(db.String(64))
    jumbotron_subheader = db.Column(db.String(64))
    desc_header = db.Column(db.String(64))
    desc_details = db.Column(db.Text)
    site_dominant_color = db.Column(db.String)
    site_accent_color = db.Column(db.String)
    site_background_color = db.Column(db.String)

    # AboutPage settings
    about_heading = db.Column(db.String(64))
    about_image = db.Column(db.String(256))
    about_detail = db.Column(db.Text)

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


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), index=True)
    slug = db.Column(db.String(128))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    featured_image = db.Column(db.String(256))
    body = db.Column(db.Text)
    
class Show(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), index=True)
    slug = db.Column(db.String(128))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    location = db.Column(db.String(256), index=True)
    url = db.Column(db.String(256), index=True)
    venue = db.Column(db.Text)
    details = db.Column(db.Text)
    featured_image = db.Column(db.String(256))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class Photo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), index=True)
    file = db.Column(db.String(256))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    caption = db.Column(db.String(256))

class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), index=True)
    email = db.Column(db.String(256), index=True)
    phone = db.Column(db.String(14), index=True)
    subject = db.Column(db.String(256), index=True)
    message = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
