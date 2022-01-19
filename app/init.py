from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from app.module.controllers import mod_auth as auth_module

app = Flask(__name__)


db = SQLAlchemy(app)


@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404


# Register blueprint(s)
app.register_blueprint(auth_module)
# app.register_blueprint(xyz_module)


db.create_all()
