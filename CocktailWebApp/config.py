#!usr/bin/env python3
"""Config"""

import pathlib
from dotenv import load_dotenv
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

def create_app():
    """Create Flask App"""
    this_app = Flask(__name__)

    if not pathlib.Path(".flaskenv").exists():
        load_dotenv("~/Desktop/BartendingProject/.flaskenv")
    this_app.config.from_prefixed_env()

    return this_app


app = create_app()

this_dir = pathlib.Path(__file__).parent
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + str(
    this_dir/pathlib.Path("iba-cocktails-web.sqlite3")
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

db = SQLAlchemy(app)

ma = Marshmallow(app)