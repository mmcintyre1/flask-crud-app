from flask_wtf import FlaskForm
from flask_ckeditor import CKEditorField
from wtforms import StringField, PasswordField, SubmitField, validators
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    username = StringField('username', [validators.Length(min=4, max=25)])
    password = PasswordField('password', validators=[DataRequired()])
    submit = SubmitField('submit')


class PostForm(FlaskForm):
    title = StringField('title', [validators.Length(min=1, max=100)])
    body = CKEditorField('body', validators=[DataRequired()])
    author = StringField('author', [validators.Length(min=1, max=15)])
    submit = SubmitField('submit')
