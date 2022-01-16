from flask import render_template, request
from flask_sqlalchemy import SQLAlchemy
from fresher_adventure_app import app

app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///user"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/manage")
def page1():
    return render_template("manage.html")


@app.route("/checkpoint")
def page2():
    return render_template("checkpoint.html")


@app.route("/login", methods=["POST"])
def login():
    if request.method == 'POST':
        if request.form["submit"] == "signIn":
            username = request.form["username"]
            password = request.form["password"]
            # login and redirect to page
            return render_template(
                "index.html", username=username, password=password)
        elif request.form["submit"] == "signUp":
            username = request.form["username"]
            password = request.form["password"]
            return render_template(
                "signup.html", username=username, password=password)
