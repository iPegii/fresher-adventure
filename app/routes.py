from flask import render_template, request, redirect, session, Blueprint
from werkzeug.security import check_password_hash, generate_password_hash
from app import app
from os import getenv
from app.models import db
from app.form import LoginForm, RegisterForm, CheckpointCreationForm
from app.models import Users as User, Permission, Checkpoint
import logging
logging.basicConfig()
logging.getLogger(
    'sqlalchemy.engine').setLevel(logging.INFO)


mod_auth = Blueprint('auth', __name__, url_prefix='/auth')


@app.route("/")
def index():
    #
    #    if session["permission"] == 1000:
    #        return render_template("checkpoint.html", )
    #
    form = LoginForm()
    return render_template(
        "index.html", form=form)


@app.route("/manage", methods=["POST", "GET"])
def manage():
    user_permission = session["permission"]
    if(user_permission == 1000):
        if(request.method == "GET"):
            users = User.query.all()
            checkpoints = Checkpoint.query.all()
            checkpoint_form = CheckpointCreationForm()
            return render_template(
                "manage.html", form=checkpoint_form,
                users=users, checkpoints=checkpoints)
        if(request.method == "POST"):
            form = CheckpointCreationForm(request.form)
            checkpoint_name = form.name.data
            findCheckpoint = Checkpoint.query.filter(
                (Checkpoint.name == checkpoint_name)).first()
            if findCheckpoint is None:
                new_checkpoint = Checkpoint(
                    checkpoint_name, "", False,
                    None, modified_at=db.func.now(),
                    created_at=db.func.now())
                db.session.add(new_checkpoint)
                db.session.commit()
            else:
                return
        users = User.query.all()
        checkpoints = Checkpoint.query.all()
        emptyForm = CheckpointCreationForm()
        return render_template(
            "manage.html", form=emptyForm,
            users=users, checkpoints=checkpoints)
    else:
        return redirect("/")


@ app.route("/checkpoint")
def checkpoint():
    return render_template("checkpoint.html")


@ app.route("/logout")
def logout():
    del session["username"]
    del session["permission"]
    return redirect("/")


@ app.route("/signup", methods=["GET", "POST"])
def sign_up():
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
            db.session.flush()
            new_permission = Permission(
                new_user.id, 1, None,
                modified_at=db.func.now(),
                created_at=db.func.now())
            db.session.add(new_permission)
            db.session.commit()
            return redirect("/")
        return redirect("/")

    else:
        form = RegisterForm()
        return render_template(
            "signup.html", form=form)


@ app.route("/login", methods=["GET", "POST"])
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
                permission = Permission.query.filter(
                    Permission.user_id == user.id).first()
                session['permission'] = permission.permission
                return redirect("/")
            else:
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
