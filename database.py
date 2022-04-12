import os
import flask
from flask import Flask
from flask_sqlalchemy import SQLAlchemy


APP = Flask(__name__)

APP.secret_key = os.getenv("SECRET_KEY")

# Point SQLAlchemy to your Heroku database
# app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
APP.config[
    "SQLALCHEMY_DATABASE_URI"
] = "postgresql://rsylquycrfjuxa:3d3d72977801c29b13d7969c33082eaf5b0ca43c756239d2e4d942282def3b59@ec2-3-216-221-31.compute-1.amazonaws.com:5432/d19vv310s7lnp5"
# Gets rid of a warning
APP.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

DB = SQLAlchemy(APP)


BP = flask.Blueprint(
    "bp",
    __name__,
    template_folder="./static/react",
)
APP.register_blueprint(BP)
# IMPORTANT: This must be AFTER creating db variable to prevent
# circular import issues

from models import User
