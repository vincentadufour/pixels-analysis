"""Authentication routes."""

from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_user, logout_user, current_user
from frontend.forms import SignUpForm, SignInForm
from frontend.models import User
from frontend import db, load_user
import bcrypt

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/signup", methods=["GET", "POST"])
def signup():
    form = SignUpForm()
    if form.validate_on_submit():
        hashed = bcrypt.hashpw(form.passwd.data.encode("utf-8"), bcrypt.gensalt())
        new_user = User(
            id=form.id.data,
            student_id=form.student_id.data,
            email=form.email.data,
            passwd=hashed,
        )
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for("main.index"))
    return render_template("users_signup.html", form=form, user=current_user)


@auth_bp.route("/sigin", methods=["GET", "POST"])
@app.route("/users/signup", methods=["GET", "POST"])
def users_signup():
    """User signup functionality."""
    form = SignUpForm()
    if form.validate_on_submit():
        passwd = form.passwd.data
        passwd_confirm = form.passwd_confirm.data
        if passwd == passwd_confirm:
            hashed = bcrypt.hashpw(passwd.encode("utf-8"), bcrypt.gensalt())
        else:
            return "<p>Passwords do not match!</p>"

        new_user = User(
            id=form.id.data,
            email=form.email.data,
            passwd=hashed,
        )
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for("index"))
    return render_template(
        "users_signup.html", title=frontend.config["USER SIGNUP"], form=form, user=current_user
    )


@app.route("/users/signin", methods=["GET", "POST"])
def users_signin():
    """User sign in functionality."""
    form = SignInForm()
    if form.validate_on_submit():
        id = form.id.data
        passwd = form.passwd.data
        hashed_passwd = passwd.encode("utf-8")

        user = load_user(id)

        if user:
            if bcrypt.checkpw(hashed_passwd, user.passwd):
                login_user(user)
            else:
                return "<p>Incorrect Password!</p>"

            if user.id == "admin":
                return redirect(url_for("index_admin"))
            return redirect(url_for("index"))
        return "<p>Username not recognized!</p>"
    return render_template(
        "users_signin.html", title=frontend.config["USER SIGNIN"], form=form, user=current_user
    )


@app.route("/users/signout", methods=["GET", "POST"])
def users_signout():
    """User signout functionality."""
    logout_user()
    return redirect(url_for("index"))
