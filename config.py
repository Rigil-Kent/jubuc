import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    WTF_CSRF_ENABLED = True
    SECRET_KEY = os.environ.get('SECRET_KEY') or "Jubuc - DJ life"
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI') or \
        'sqlite:///' + os.path.join(basedir, 'jubuc.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = basedir + "/app/static/uploads"
    POSTS = UPLOAD_FOLDER + "/posts"
    ALBUMS = UPLOAD_FOLDER + "/albums/"
    AUDIO = UPLOAD_FOLDER + "/audio/"
    ADMIN = "bryan.bailey@brizzle.dev"
    POSTS_PER_PAGE = 12