from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from time import time
from markdown import markdown
from config import Config
from flask_migrate import Migrate
from flask_colorpicker import colorpicker
from flask_login import LoginManager
from flask_pagedown import PageDown
from flask_moment import Moment
from flask_bootstrap import Bootstrap



app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
colorpicker(app)
login = LoginManager(app)
login.login_view = 'login'
pagedown = PageDown(app)
moment = Moment(app)
bootstrap = Bootstrap(app)


from app import routes, models

if __name__ == "__main__":
    app.run()