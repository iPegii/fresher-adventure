from flask import render_template, request, redirect
from fresher_adventure_app import app
from flask_sqlalchemy import SQLAlchemy

app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///user"
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
            return render_template("result.html", username=username,
                                          password=password)