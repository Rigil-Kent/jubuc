from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from time import time
from markdown import markdown
from config import Config
from flask_migrate import Migrate
from flask_colorpicker import colorpicker
from flask_login import LoginManager


app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
colorpicker(app)
login = LoginManager(app)
login.login_view = 'login'


from app import routes, models

if __name__ == "__main__":
    app.run()