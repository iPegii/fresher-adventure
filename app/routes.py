from flask import render_template, request, redirect, session, flash, Blueprint
from werkzeug.security import check_password_hash, generate_password_hash
from app import app
from os import getenv
from app.models import db
from app.form import LoginForm, RegisterForm
from app.models import User
import logging
logging.basicConfig()
logging.getLogger(
    'sqlalchemy.engine').setLevel(logging.INFO)


mod_auth = Blueprint('auth', __name__, url_prefix='/auth')


@app.route("/")
def index():
    form = LoginForm()
    return render_template("index.html", form=form)


@app.route("/manage")
def page1():
    return render_template("manage.html")


@app.route("/checkpoint")
def page2():
    return render_template("checkpoint.html")


@app.route("/signup", methods=["GET", "POST"])
def sign_up():
    print('wow')
    if request.method == "POST":
        form = RegisterForm(request.form)
        username = form.username.data
        email = form.email.data
        print(getenv('DATABASE_URL'))
        user = User.query.filter(
            (User.email == email) | (User.name == username)).first()
        if user is None:
            print('success')
            hashed_password = generate_password_hash(
                form.password.data)
            new_user = User(
                name=username, email=email,
                password=hashed_password,
                modified_at=db.func.now(),
                created_at=db.func.now())
            db.session.add(new_user)
            db.session.commit()
            return redirect("/")
        return flash('Error in sign up')

    else:
        form = RegisterForm()
        return render_template(
            "signup.html", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        if request.form["submit_button"] == "signIn":
            form = LoginForm(request.form)
            username = form.username.data
            user = User.query.filter(
                (username == User.name) |
                (username == User.email)).first()
            if user and check_password_hash(
                    user.password, form.password.data):
                session['username'] = user.name
                flash(f'Welcome {user.name}')
                return redirect("/")
        elif request.form["submit_button"] == "signUp":
            form = RegisterForm(request.form)
            return render_template(
                "signup.html", username=form.username.data,
                form=form)
        else:
            return redirect("/")
    else:
        return redirect("/")