from wtforms import StringField, validators, EmailField, PasswordField
from flask_wtf import FlaskForm


class RegisterForm(FlaskForm):
    username = StringField(
        'Username', [validators.Length(min=4, max=25)])
    email = EmailField(
        'Email',
        [validators.Email(), validators.DataRequired()])
    password = PasswordField(
        'Password',
        [validators.Length(min=8, max=26),
         validators.DataRequired(),
         validators.EqualTo(
             'confirm', message='Passwords must match')])
    confirm = PasswordField('Repeat Password')


class LoginForm(FlaskForm):
    username = StringField(
        'Username', [validators.Length(min=4, max=25)])
    password = PasswordField(
        'Password', [validators.Length(min=8, max=26)])
