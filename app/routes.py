from flask import render_template, request, redirect, session, Blueprint
from werkzeug.security import check_password_hash, generate_password_hash
from app import app
from os import getenv
from app.models import db
from app.form import LoginForm, RegisterForm, CheckpointCreationForm, TeamCreationForm
from app.models import Users as User, Permission, Checkpoint, Team
import logging
logging.basicConfig()
logging.getLogger(
    'sqlalchemy.engine').setLevel(logging.INFO)

mod_auth = Blueprint('auth', __name__, url_prefix='/auth')


@app.route("/")
def index():

    if session.get('permission') == 2:
        teams = Team.query.all()
        return render_template("checkpoint-manage.html", teams=teams)
    else:
        form = LoginForm()
        return render_template(
            "index.html", form=form)


@app.route("/permissions", methods=["GET", "POST"])
def permissions_manage():

    if session.get('permission') == 1000:
        if request.method == "GET":
            users = User.query.join(Permission).add_columns(User.id, User.name, Permission.user_id, Permission.permission).filter(
                User.id == Permission.user_id)

            for user in users:
                print(user.permission)
            return render_template("permissions.html", users=users)

    else:
        return redirect("/")


@app.route("/checkpoint", methods=["POST", "GET"])
def manage_checkpoint():
    user_permission = session["permission"]
    if(user_permission == 1000):
        if(request.method == "GET"):
            users = User.query.all()
            checkpoints = Checkpoint.query.all()
            checkpoint_form = CheckpointCreationForm()
            return render_template(
                "checkpoint-manage.html", form=checkpoint_form,
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
            "checkpoint-manage.html", form=emptyForm,
            users=users, checkpoints=checkpoints)
    else:
        return redirect("/")


@ app.route("/team", methods=["POST", "GET"])
def manage_team():
    user_permission = session["permission"]
    if(user_permission == 1000):
        users = User.query.all()
        teams = Team.query.all()
        empty_form = TeamCreationForm()
        if(request.method == "GET"):
            return render_template(
                "team-manage.html", form=empty_form,
                users=users, teams=teams)
        if(request.method == "POST"):
            form = TeamCreationForm(request.form)
            team_name = form.name.data
            if form.validate_on_submit():
                print('lol')
            else:
                return render_template(
                    "team-manage.html", form=empty_form,
                    users=users, teams=teams)
            find_team = Team.query.filter(
                (Team.name == team_name)).first()
            if find_team is None:
                new_team = Team(
                    team_name, modified_at=db.func.now(),
                    created_at=db.func.now())
                db.session.add(new_team)
                db.session.commit()
            else:
                return
        users = User.query.all()
        teams = Team.query.all()
        emptyForm = TeamCreationForm()
        return render_template(
            "team-manage.html", form=emptyForm,
            users=users, teams=teams)
    else:
        return redirect("/")


@ app.route("/logout")
def logout():
    del session["username"]
    del session["permission"]
    return redirect("/")


@ app.route("/signup", methods=["GET", "POST"])
def sign_up():
    print(getenv("SQLALCHEMY_DATABASE_URL"))
    if request.method == "POST":
        form = RegisterForm(request.form)
        username = form.username.data
        email = form.email.data
        user = User.query.filter(
            (User.email == email) | (User.name == username)).first()
        if user is None:
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
