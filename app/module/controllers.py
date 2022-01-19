from os import getenv
from flask import render_template, request, redirect, Blueprint, url_for, g, session, flash
from werkzeug.security import check_password_hash, generate_password_hash
from app import db
from app import app
from app.form import LoginForm, RegisterForm
from app.module.models import User
app.secret_key = getenv("SECRET_KEY")

# Define the blueprint: 'auth', set its url prefix: app.url/auth
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


@app.route("/signup")
def sign_up():
    form = RegisterForm()
    return render_template(
        "signup.html", form=form)


@mod_auth.route("/login", methods=["POST"])
def login():
    if request.method == 'POST':
        if request.form["submit_button"] == "signIn":
            form = LoginForm(request.form)
            user = User.query.filter_by(
                email=form.email.data).first()
            if user and check_password_hash(
                    user.password, form.password.data):
                session['user_id'] = user.id
                flash(f'Welcome {user.name}')
    # login and redirect to page
            return redirect("index.html")
        elif request.form["submit_button"] == "signUp":

            """
            form = RegisterForm(request.form)
            return render_template(
            "signup.html", username=form.username.data,
            password=form.password.data, form=form)
            """
            form = RegisterForm()
            username = request.args.get("username", None)
            password = request.args.get("password", None)
            return render_template(
                "signup.html", username=username,
                password=password, form=form)
