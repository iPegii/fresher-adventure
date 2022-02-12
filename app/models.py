from app import app
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy(app)


class Users(db.Model):
    """Database model for User"""

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(25), nullable=False, unique=True)
    password = db.Column(db.String(), nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True)
    modified_at = db.Column(
        db.TIMESTAMP(timezone=True),
        nullable=False, onupdate=db.func.now())
    created_at = db.Column(
        db.TIMESTAMP(timezone=True),
        nullable=False, server_default=db.func.now())

    def __init__(
            self, name, password, email,
            modified_at, created_at):
        self.name = name
        self.password = password
        self.email = email
        self.modified_at = modified_at
        self.created_at = created_at

    def __repr__(self):
        return f"<User {self.name}>"


class Permission(db.Model):
    """Database model for Permission"""

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer, db.ForeignKey('users.id'),
        nullable=False)
    permission = db.Column(
        db.Integer, nullable=False, default=0)
    checkpoint_id = db.Column(
        db.Integer, db.ForeignKey('checkpoint.id'),
        nullable=True)
    modified_at = db.Column(
        db.TIMESTAMP(timezone=True),
        nullable=False, onupdate=db.func.now())
    created_at = db.Column(
        db.TIMESTAMP(timezone=True),
        nullable=False, server_default=db.func.now())

    def __init__(
            self, user_id, permission, checkpoint_id,
            modified_at, created_at):
        self.user_id = user_id
        self.permission = permission
        self.checkpoint_id = checkpoint_id
        self.modified_at = modified_at
        self.created_at = created_at

    def __repr__(self):
        return f"<permission {self.permission}>"


class Checkpoint(db.Model):
    """Database model for Checkpoint"""

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=True, unique=True)
    description = db.Column(db.String(1000), nullable=True)
    can_be_visible = db.Column(
        db.Boolean, nullable=False, default=False)
    location_id = db.Column(
        db.Integer, db.ForeignKey('location.id'),
        nullable=False)
    modified_at = db.Column(
        db.TIMESTAMP(timezone=True),
        nullable=False, onupdate=db.func.now())
    created_at = db.Column(
        db.TIMESTAMP(timezone=True),
        nullable=False, server_default=db.func.now())

    def __init__(
            self, name, description, can_be_visible,
            location_id, modified_at, created_at):
        self.name = name
        self.description = description
        self.can_be_visible = can_be_visible
        self.location_id = location_id
        self.modified_at = modified_at
        self.created_at = created_at

    def __repr__(self):
        return f"<Checkpoint %r> % {self.name}"


class Point(db.Model):
    """Database model for Point"""

    id = db.Column(db.Integer, primary_key=True)
    point = db.Column(db.Integer, nullable=False)
    checkpoint_id = db.Column(
        db.Integer, db.ForeignKey('checkpoint.id'),
        nullable=False)
    team_id = db.Column(
        db.Integer, db.ForeignKey('team.id'),
        nullable=False)
    modified_at = db.Column(
        db.TIMESTAMP(timezone=True),
        nullable=False, onupdate=db.func.now())
    created_at = db.Column(
        db.TIMESTAMP(timezone=True),
        nullable=False, server_default=db.func.now())

    def __init__(
            self, point, checkpoint_id, team_id,
            modified_at, created_at):
        self.point = point
        self.checkpoint_id = checkpoint_id
        self.team_id = team_id
        self.modified_at = modified_at
        self.created_at = created_at

    def __repr__(self):
        return f"<Point {self.point}>"


class Team(db.Model):
    """Database model for Team"""

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    modified_at = db.Column(
        db.TIMESTAMP(timezone=True),
        nullable=False, onupdate=db.func.now())
    created_at = db.Column(
        db.TIMESTAMP(timezone=True),
        nullable=False, server_default=db.func.now())

    def __init__(
            self, name,
            modified_at, created_at):
        self.name = name
        self.modified_at = modified_at
        self.created_at = created_at

    def __repr__(self):
        return f"<Team {self.name}>"


class Location(db.Model):
    """Database model for Location"""

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    checkpoint_id = db.Column(
        db.Integer, db.ForeignKey('checkpoint.id'),
        nullable=False)
    modified_at = db.Column(
        db.TIMESTAMP(timezone=True),
        nullable=False, onupdate=db.func.now())
    created_at = db.Column(
        db.TIMESTAMP(timezone=True),
        nullable=False, server_default=db.func.now())

    def __init__(
            self, name, longitude, latitude, checkpoint_id,
            modified_at, created_at):
        self.name = name
        self.longitude = longitude
        self.latitude = latitude
        self.checkpoint_id = checkpoint_id
        self.modified_at = modified_at
        self.created_at = created_at

    def __repr__(self):
        return f"<Location {self.name}>"
