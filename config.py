"""Flask configuration variables."""
from os import getenv, path, environ
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = path.abspath(path.dirname(__file__))
# General Config
SECRET_KEY = getenv("SECRET_KEY")
FLASK_APP = getenv('FLASK_APP')
FLASK_ENV = getenv('FLASK_ENV')

# Database
SQLALCHEMY_DATABASE_URI = environ.get(
    'DATABASE_URL?sslmode=require').replace('postgres://', 'postgresql://')
SQLALCHEMY_ECHO = False
SQLALCHEMY_TRACK_MODIFICATIONS = False
