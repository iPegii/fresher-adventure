from wtforms import StringField, RadioField
from wtforms import EmailField, PasswordField, SelectField
from wtforms.validators import DataRequired, ValidationError
from wtforms.validators import Length, Email, EqualTo
from flask_wtf import FlaskForm
from app.models import Team, Users as User


class RegisterForm(FlaskForm):
    """Register form for the website"""
    username = StringField(
        'Käyttäjätunnus',
        [Length(min=4, max=25)])
    email = EmailField(
        'Sähköposti',
        [Email(), DataRequired()])
    password = PasswordField(
        'Salasana',
        [Length(min=8, max=26),
         DataRequired(),
         EqualTo(
             'confirm',
             message='Salasanojen pitää olla samat')])
    confirm = PasswordField('Toista salasana')

    def validate_user_name(form, field):
        print(form, field, "UserName")
        old_user = User.query.filter(
            (User.name == field.data.name)).first()
        if old_user is not None:
            raise ValidationError(
                'Käyttäjän nimen pitää olla uniikki')


class LoginForm(FlaskForm):
    """Login form for the website"""
    username = StringField(
        'Käyttäjätunnus',
        [Length(min=4, max=25)])
    password = PasswordField(
        'Salasana', [Length(min=8, max=26)])


class CheckpointCreationForm(FlaskForm):
    """Creation of new checkpoints"""
    name = StringField(
        'Rastin nimi',
        [Length(min=4, max=50)])


class TeamCreationForm(FlaskForm):
    """Creation of new team"""
    name = StringField(
        'Joukkueen nimi',
        [Length(min=4, max=50),
         DataRequired()])

    def validate_team_name(form, field):
        old_team = Team.query.filter(
            (Team.name == field.data.name)).first()
        if old_team is not None:
            raise ValidationError(
                'Joukkueen nimen pitää olla uniikki')


class UserPermissionToCheckpointForm(FlaskForm):
    """Select field for changing user permission to checkpoint"""

    checkpoint = SelectField('Rastit', coerce=int)


class PointsForm(FlaskForm):
    """Radio field for giving team points"""

    radio = RadioField(
        'Pisteet',
        choices=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
