from flask import render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from fresher_adventure_app import app
from fresher_adventure_app.components import Form
import sys
from os import getenv
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///user"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)
app.secret_key = getenv("SECRET_KEY")


@app.route("/")
def index():
    form = Form.LoginForm()
    return render_template("index.html", form=form)


@app.route("/manage")
def page1():
    return render_template("manage.html")


@app.route("/checkpoint")
def page2():
    return render_template("checkpoint.html")


@app.route("/signup")
def signUp():
    form = Form.RegisterForm()
    return render_template(
        "signup.html", form=form)


@app.route("/login", methods=["POST"])
def login():
    if request.method == 'POST':
        if request.form["submit_button"] == "signIn":
            username = request.form["username"]
            password = request.form["password"]
            # login and redirect to page
            return redirect("index.html")
        elif request.form["submit_button"] == "signUp":
            form = Form.RegisterForm()
            username = request.args.get("username", None)
            password = request.args.get("password", None)
            return render_template(
                "signup.html", username=username,
                password=password, form=form)
