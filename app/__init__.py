from flask import Flask
from os import getenv
from dotenv import load_dotenv
from flask_wtf import csrf

load_dotenv()

app = Flask(__name__)
csrf_handler = csrf
csrf = csrf.CSRFProtect(app)
uri = getenv("DATABASE_URL")  # or other relevant config var
if uri and uri.startswith("postgres://"):
    uri = uri.replace("postgres://", "postgresql://", 1)

app.config["SQLALCHEMY_DATABASE_URI"] = uri
app.config["SQLALCHEMY_ECHO"] = False
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = getenv("SECRET_KEY")

from app import routes  # noqa: F401, E402
