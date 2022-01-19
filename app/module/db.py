from os import getenv
from flask_sqlalchemy import SQLAlchemy
from app import app
app.config["SQLALCHEMY_DATABASE_URI"] = getenv(
    "DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = getenv("SECRET_KEY")
db = SQLAlchemy(app)

db.create_all()
