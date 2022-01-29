from wtforms import StringField, validators, EmailField, PasswordField
from flask_wtf import FlaskForm


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
