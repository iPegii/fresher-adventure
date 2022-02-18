from wtforms import StringField, validators, RadioField
from wtforms import EmailField, PasswordField, SelectField
from flask_wtf import FlaskForm
from app.models import Team, Users as User


class RegisterForm(FlaskForm):
    """Register form for the website"""
    username = StringField(
        'Käyttäjätunnus',
        [validators.Length(min=4, max=25)])
    email = EmailField(
        'Sähköposti',
        [validators.Email(), validators.DataRequired()])
    password = PasswordField(
        'Salasana',
        [validators.Length(min=8, max=26),
         validators.DataRequired(),
         validators.EqualTo(
             'confirm',
             message='Salasanojen pitää olla samat')])
    confirm = PasswordField('Toista salasana')

    def validate_user_name(form, field):
        print(form, field, "UserName")
        old_user = User.query.filter(
            (User.name == field.data.name)).first()
        if old_user is not None:
            raise validators.ValidationError(
                'Käyttäjän nimen pitää olla uniikki')


class LoginForm(FlaskForm):
    """Login form for the website"""
    username = StringField(
        'Käyttäjätunnus',
        [validators.Length(min=4, max=25)])
    password = PasswordField(
        'Salasana', [validators.Length(min=8, max=26)])


class CheckpointCreationForm(FlaskForm):
    """Creation of new checkpoints"""
    name = StringField(
        'Rastin nimi',
        [validators.Length(min=4, max=50)])


class TeamCreationForm(FlaskForm):
    """Creation of new team"""
    name = StringField(
        'Joukkueen nimi',
        [validators.Length(min=4, max=50),
         validators.DataRequired()])

    def validate_team_name(form, field):
        old_team = Team.query.filter(
            (Team.name == field.data.name)).first()
        if old_team is not None:
            raise validators.ValidationError(
                'Joukkueen nimen pitää olla uniikki')


class UserPermissionToCheckpointForm(FlaskForm):
    """Select field for changing user permission to checkpoint"""

    checkpoint = SelectField('Rastit', coerce=int)


class PointsForm(FlaskForm):
    """Radio field for giving team points"""

    radio = RadioField(
        'Pisteet',
        choices=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
