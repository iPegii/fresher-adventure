from flask import render_template, request, redirect, session, Blueprint
from werkzeug.security import check_password_hash, generate_password_hash
from app import app, csrf_handler
from app.models import db
from app.form import LoginForm, RegisterForm, PointsForm
from app.form import CheckpointCreationForm, TeamCreationForm
from app.models import Users as User, Permission, Checkpoint, Team, Point
import logging
from os import getenv
logging.basicConfig()
logging.getLogger(
    'sqlalchemy.engine').setLevel(logging.INFO)

mod_auth = Blueprint('auth', __name__, url_prefix='/auth')


@app.route("/")
def index():
    permission = Permission.query.filter(
        Permission.user_id == session.get("user_id")).first()
    if permission is None:
        admin = getenv("ADMIN")
        checkpointer = getenv("CHECKPOINT")
        form = LoginForm()
        return render_template(
            "index.html", form=form, admin=admin,
            checkpointer=checkpointer)
    if permission.permission == 2:
        return checkpoint(permission)
    elif permission.permission == 1000:
        return redirect("/checkpoints/manage")
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
                return render_template(
                    "permissions.html", users=users,
                    permission=permission.permission)
        else:
            return redirect("/")
    else:
        session["next_url"] = request.path
        return redirect("/")


@app.route("/checkpoints/manage", methods=["POST", "GET"])
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
                Checkpoint,
                Checkpoint.id == Permission.checkpoint_id
            ).add_columns(
                User.id, User.name.label("user_name"),
                Permission.user_id,
                Permission.permission,
                Permission.checkpoint_id,
                Checkpoint.id,
                Checkpoint.name.label(
                    "checkpoint_name"), User.created_at
            ).order_by(User.created_at).all()
            checkpoints = Checkpoint.query.all()
            checkpoint_adding_form = CheckpointCreationForm()
            return render_template(
                "checkpoints-manage.html",
                checkpoint_adding_form=checkpoint_adding_form,
                checkpoints=checkpoints, users=users,
                permission=user_permission.permission)
        if(request.method == "POST"):
            if request.form.get("submit_button") == "save_checkpoint":
                checkpoint_data = request.form.get(
                    "checkpoint_select", "")
                checkpoint_data_filtered = checkpoint_data.split(
                    ",")
                user_id = int(checkpoint_data_filtered[0])
                u_permission = Permission.query.filter(
                    Permission.user_id == user_id).first()
                checkpoint_id = None
                print(checkpoint_data)
                if checkpoint_data_filtered[1] != "None":
                    checkpoint_id = int(
                        checkpoint_data_filtered[1])
                if u_permission.permission <= 1:
                    u_permission.permission = 2
                u_permission.checkpoint_id = checkpoint_id
                db.session.commit()
                return redirect("/checkpoints/manage")
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
                return redirect("/checkpoints/manage")
    else:
        session["next_url"] = request.path
        return redirect("/")


@app.route("/checkpoint/<int:id>")
def checkpoint(permission):
    user_permission = Permission.query.filter(
        Permission.user_id == session.get("user_id")).first()
    if(user_permission is None):
        session["next_url"] = request.path
        return redirect("/")
    id = permission.checkpoint_id
    checkpoint = Checkpoint.query.filter(
        Checkpoint.id == id).first()
    sql = "SELECT c.id, t.id,t.name, p.point_amount FROM checkpoint c"\
        " LEFT OUTER JOIN point p ON p.checkpoint_id = :checkpoint_id"\
        " RIGHT OUTER JOIN team t ON t.id = p.team_id and"\
        " c.id = :checkpoint_id GROUP BY"\
        " c.id, t.id, p.point_amount, p.checkpoint_id, p.team_id"\
        " ORDER BY t.modified_at"
    data = db.session.execute(
        sql, {"checkpoint_id": id}).fetchall()
    print(data)
    for r in data:
        print(r)
    return render_template(
        "checkpoint.html", checkpoint=checkpoint,
        permission=user_permission.permission, data=data)


@app.route("/checkpoints")
def checkpoints():
    user_permission = Permission.query.filter(
        Permission.user_id == session.get("user_id")).first()
    if(user_permission is None):
        session["next_url"] = request.path
        return redirect("/")
    if(user_permission.permission == 1000):
        checkpoints = Checkpoint.query.all()
        teams = Team.query.all()

        data = []
        for team in teams:
            sql = "SELECT c.id AS checkpoint_id,c.name AS checkpoint_name,"\
                " t.id AS team_id,t.name AS team_name, "\
                " p.point_amount AS points,"\
                " CASE WHEN t.name is Null THEN :team_name ELSE 'wow'"\
                " END AS team_name FROM team t"\
                " LEFT OUTER JOIN point p ON p.team_id = :team_id"\
                " RIGHT OUTER JOIN checkpoint c ON c.id = p.checkpoint_id and"\
                "  t.id = :team_id GROUP BY"\
                " c.id, t.id, p.point_amount, p.checkpoint_id, p.team_id"\
                " ORDER BY checkpoint_id"
            result = db.session.execute(
                sql, {"team_id": team.id, "team_name": team.name}).fetchall()
            data.insert(team.id, result)
        return render_template(
            "checkpoints.html", data=data,
            checkpoint_data=checkpoints, teams=teams,
            permission=user_permission.permission)
    else:
        redirect("/")


@ app.route("/teams/manage", methods=["POST", "GET"])
def team_manage():
    user_permission = Permission.query.filter(
        Permission.user_id == session.get("user_id")).first()
    if(user_permission is None):
        session["next_url"] = request.path
        return redirect("/")
    if(user_permission.permission == 1000):
        users = User.query.all()
        teams = Team.query.all()
        empty_form = TeamCreationForm()
        if(request.method == "GET"):
            return render_template(
                "teams-manage.html", form=empty_form,
                users=users, teams=teams,
                permission=user_permission.permission)
        if(request.method == "POST"):
            form = TeamCreationForm(request.form)
            team_name = form.name.data
            if form.validate_on_submit() is False:
                return redirect("/teams/manage")
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
        return redirect("/teams/manage")
    else:
        session["next_url"] = request.path
        return redirect("/")


@app.route("/team/<int:id>", methods=["POST", "GET"])
def team(id):
    permission = Permission.query.filter(
        Permission.user_id == session.get("user_id")).first()
    if permission is None:
        session["next_url"] = request.path
        return redirect("/")
    else:
        if permission.permission == 2:
            point_data = Point.query.filter(Point.team_id == id).filter(
                Point.checkpoint_id == permission.checkpoint_id
            ).first()
            if(request.method == "GET"):
                team = Team.query.filter(
                    Team.id == id).first()
                form = PointsForm()
                return render_template(
                    "team.html",
                    point_data=point_data,
                    user_id=session.get("user_id"),
                    team=team,
                    permission=permission.permission,
                    form=form)
            elif request.method == "POST":
                form = PointsForm(request.form)
                form_data = form.radio.data
                if(form_data is None):
                    return redirect("/team/" + str(id))
                if(point_data is None):
                    new_point = Point(
                        session.get("user_id"),
                        form_data, permission.checkpoint_id,
                        id, modified_at=db.func.now(),
                        created_at=db.func.now())
                    db.session.add(new_point)
                    db.session.commit()
                    return redirect("/team/" + str(id))
                else:
                    point_data.point_amount = form_data
                    db.session.add(point_data)
                    db.session.commit()
                    return redirect("/team/" + str(id))

            else:
                return redirect("/team/" + str(id))
        else:
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


'''

                sql = """UPDATE permission SET checkpoint_id =: checkpoint_id
                , permission = : permission WHERE user_id = : user_id"""
                db.session.execute(
                    sql,
                    {"checkpoint_id": checkpoint_id,
                     "permission": temp_user_permission.permission,
                     "user_id": user_id})

'''
