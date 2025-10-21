"""Forms for users."""

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired


class SignUpForm(FlaskForm):
    """Sign up form."""

    id = StringField("Id", validators=[DataRequired()])
    email = StringField("E-mail", validators=[DataRequired()])
    passwd = PasswordField("Password", validators=[DataRequired()])
    passwd_confirm = PasswordField("Confirm Password", validators=[DataRequired()])
    submit = SubmitField("Confirm")


class SignInForm(FlaskForm):
    """Sign in form."""

    id = StringField("Id", validators=[DataRequired()])
    passwd = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Confirm")
