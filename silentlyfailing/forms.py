from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, validators
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    """Form class for user login."""
    username = StringField('username', [validators.Length(min=4, max=25)])
    password = PasswordField('password', validators=[DataRequired()])
