from os import getenv
from flask import render_template, request, redirect, Blueprint, url_for, g, session, flash
from werkzeug.security import check_password_hash, generate_password_hash
from fresher_adventure_app import app
from fresher_adventure_app import db
from fresher_adventure_app.form import LoginForm, RegisterForm
from fresher_adventure_app.db import User
app.secret_key = getenv("SECRET_KEY")


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
    if request.method == "POST":
        form = RegisterForm(request.form)
        user = User.query.filter_by(
            email=form.email.data, user=form.username.data).first()
        if user is None:
            hashed_password = generate_password_hash(form.password)
            new_user = User(username=form.username, email=form.email,
                            password=hashed_password, permission=0)
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
            user = User.query.filter_by(
                email=form.email.data).first()
            if user and check_password_hash(
                    user.password, form.password.data):
                session['username'] = user.name
                flash(f'Welcome {user.name}')
                return redirect("/")
        elif request.form["submit_button"] == "signUp":
            form = RegisterForm(request.form)
            return render_template(
                "signup.html", username=form.username.data, form=form)
        else:
            return redirect("/")
    else:
        return redirect("/")
