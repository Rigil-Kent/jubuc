from wtforms import SubmitField, StringField, BooleanField, PasswordField, TextAreaField, SelectField, FileField, RadioField, MultipleFileField, DateTimeField
from wtforms.ext.sqlalchemy.fields import QuerySelectField, QuerySelectMultipleField
from flask_wtf import FlaskForm
from app.models import Audio
from wtforms import validators
from wtforms.validators import DataRequired, EqualTo
from wtforms.ext.sqlalchemy.fields import QuerySelectField, QuerySelectMultipleField
from flask_pagedown.fields import PageDownField


def audio_factory():
    return Audio.query

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign In')

class AdminForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm = PasswordField('Repeat Password', validators=[EqualTo('password')])
    site_title = StringField('Site Title', validators=[DataRequired()])
    site_logo_text = StringField('Site Logo (Text)', validators=[DataRequired()])
    site_logo_image = FileField('Site Logo (Image)')
    jumbotron_image = FileField('Header Image')
    site_dominant_color = StringField('Dominant Color', validators=[DataRequired()])
    site_accent_color = StringField('Accent Color', validators=[DataRequired()])
    site_background_color = StringField('Background Color', validators=[DataRequired()])

    facebook = StringField('Facebook')
    twitter = StringField('Twitter')
    instagram = StringField('Instagram')
    soundcloud = StringField('Soundcloud')
    youtube = StringField('Youtube')
    spotify = StringField('Spotify')
    twitter_consumer_key = StringField('Twitter Consumer Key')
    twitter_consumer_key_secret = StringField('Twitter Consumer Key Secret')
    twitter_access_token = StringField('Twitter Access Token')
    twitter_access_token_secret = StringField('Twitter Access Token Secret')
    submit = SubmitField('Launch')


class UserForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm = PasswordField('Repeat Password', validators=[EqualTo('password')])
    facebook = StringField('Facebook')
    twitter = StringField('Twitter')
    instagram = StringField('Instagram')
    bio = TextAreaField('About Me')
    avatar = FileField('Avatar')

class AudioForm(FlaskForm):
    name = StringField('Track Title', validators=[DataRequired()])
    file = FileField('Track File', validators=[DataRequired()])
    album_art = FileField('Album Art')
    is_active = BooleanField('Active?')
    submit = SubmitField('Add')

class PlayerForm(FlaskForm):
    active_track = QuerySelectField('Active Track ', query_factory=audio_factory, allow_blank=True, get_label="name")
    submit = SubmitField('Set Active Track')

class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    featured_image = FileField('Feature Image')
    body = PageDownField('Post', validators=[DataRequired()])
    submit = SubmitField("Submit")


class ShowForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    timestamp = DateTimeField('Date & Time', id="datepick", format='%m/%d/%Y %H:%M %p',validators=[DataRequired()])
    location = StringField('Location', validators=[DataRequired()])
    featured_image = FileField('Featured Image',)
    url = StringField('Website')
    details = StringField('Details')
    submit = SubmitField('Submit')