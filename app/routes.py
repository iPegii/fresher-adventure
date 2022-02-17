from flask import render_template, request, redirect, session, Blueprint
from werkzeug.security import check_password_hash, generate_password_hash
from app import app, csrf_handler
from app.models import db
from app.form import LoginForm, RegisterForm
from app.form import CheckpointCreationForm, TeamCreationForm
from app.models import Users as User, Permission, Checkpoint, Team
import logging
logging.basicConfig()
logging.getLogger(
    'sqlalchemy.engine').setLevel(logging.INFO)

mod_auth = Blueprint('auth', __name__, url_prefix='/auth')


@app.route("/")
def index():
    permission = Permission.query.filter(
        Permission.user_id == session.get("user_id")).first()
    if permission is None:
        form = LoginForm()
        return render_template(
            "index.html", form=form)
    if permission.permission == 2:
        teams = Team.query.all()
        return render_template(
            "checkpoint-manage.html", teams=teams)
    elif permission.permission == 1000:
        return redirect("/checkpoint")
    else:
        form = LoginForm()
        return render_template(
            "index.html", form=form)


@app.route("/permissions", methods=["GET", "POST"])
def permissions_manage():

    permission = Permission.query.filter(
        Permission.user_id == session.get("user_id")).first()
    if permission is not None:
        if permission.permission == 1000:
            if request.method == "GET":
                users = User.query.join(Permission).add_columns(
                    User.id, User.name, Permission.user_id,
                    Permission.permission).filter(
                        User.id == Permission.user_id)

                for user in users:
                    print(user)
                return render_template(
                    "permissions.html", users=users)
        else:
            return redirect("/")
    else:
        session["next_url"] = request.path
        return redirect("/")


@app.route("/checkpoint", methods=["POST", "GET"])
def manage_checkpoint():
    user_permission = Permission.query.filter(
        Permission.user_id == session.get("user_id")).first()
    if(user_permission is None):
        session["next_url"] = request.path
        return redirect("/")
    if(user_permission.permission == 1000):
        if(request.method == "GET"):
            users = User.query.outerjoin(
                Permission, User.id == Permission.user_id
            ).outerjoin(
                Checkpoint, Checkpoint.id == Permission.checkpoint_id
            ).add_columns(
                User.id, User.name.label("user_name"), Permission.user_id,
                Permission.permission, Permission.checkpoint_id, Checkpoint.id,
                Checkpoint.name.label("checkpoint_name"), User.created_at
            ).order_by(User.created_at).all()
            checkpoints = Checkpoint.query.all()
            for check in users:
                print(check)
            checkpoint_adding_form = CheckpointCreationForm()
            return render_template(
                "checkpoint-manage.html",
                checkpoint_adding_form=checkpoint_adding_form,
                checkpoints=checkpoints, users=users)
        if(request.method == "POST"):
            if request.form["submit_button"] == "save_checkpoint":
                checkpoint_data = request.form.get(
                    "checkpoint_select", "")
                checkpoint_data_filtered = checkpoint_data.split(
                    ",")
                print(checkpoint_data_filtered)
                temp_user = Permission.query.filter(
                    Permission.user_id ==
                    int(checkpoint_data_filtered[0])).first()
                print(temp_user)
                temp_user.checkpoint_id = checkpoint_data_filtered[1]
                db.session.commit()
                return redirect("/checkpoint")
            else:
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
                users = User.query.all()
                checkpoints = Checkpoint.query.all()
                emptyForm = CheckpointCreationForm()
                return render_template(
                    "checkpoint-manage.html",
                    form=emptyForm, users=users,
                    checkpoints=checkpoints)
    else:
        session["next_url"] = request.path
        return redirect("/")


@ app.route("/team", methods=["POST", "GET"])
def manage_team():
    user_permission = Permission.query.filter(
        Permission.user_id == session.get("user_id")).first()
    if(user_permission is None):
        session["next_url"] = request.path
        return redirect("/")
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
        session["next_url"] = request.path
        return redirect("/")


@ app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


@ app.route("/signup", methods=["GET", "POST"])
def sign_up():
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
                session['user_id'] = user.id
                session.permanent = True
                next_url = session.get("next_url")
                if next_url is not None:
                    session.pop('next_url', default=None)
                    return redirect(next_url)
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


@app.errorhandler(csrf_handler.CSRFError)
def csrf_error(reason):
    return render_template('error.html', reason=reason)
