"""Website routing."""

from frontend import app, db, load_user
from frontend.models import User
from frontend.forms import SignUpForm, SignInForm
from flask import render_template, redirect, url_for, redirect
from flask_login import login_required, login_user, logout_user, current_user
import bcrypt
from sqlalchemy import cast, Integer, desc, asc, func
from datetime import date


@app.route('/')
@app.route('/index')
@app.route('/index.html')
def index():
    return render_template('index.html',user=current_user)


###########################################################################################################
# Start of sign in/ sign-up/ sign out 

@app.route('/users/signup', methods=['GET', 'POST'])
def users_signup():
    """User signup functionality."""

    form = SignUpForm()
    if form.validate_on_submit():
        passwd = form.passwd.data
        passwd_confirm = form.passwd_confirm.data
        if passwd == passwd_confirm:
            hashed = bcrypt.hashpw(passwd.encode('utf-8'), bcrypt.gensalt())
        else:
            return '<p>Passwords do not match!</p>'
        
        new_user = User(
            id = form.id.data,
            student_id = form.student_id.data,
            email = form.email.data,
            passwd = hashed
        )
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('index'))
    else:
        return render_template('users_signup.html', title=app.config['USER SIGNUP'], form=form,user=current_user)
    

@app.route('/users/signin', methods=['GET', 'POST'])
def users_signin():
    """User sign in functionality."""

    form = SignInForm()
    if form.validate_on_submit():
        id = form.id.data
        passwd = form.passwd.data
        hashed_passwd = passwd.encode('utf-8')

        user = load_user(id)

        if user:
            if bcrypt.checkpw(hashed_passwd, user.passwd):
                login_user(user)
            else:
                return '<p>Incorrect Password!</p>'

            if user.id == "admin":
                return redirect(url_for('index_admin'))
            else:
                return redirect(url_for('index'))
        else:
            return '<p>Username not recognized!</p>'
    else:
        return render_template('users_signin.html', title=app.config['USER SIGNIN'], form=form,user=current_user)


@app.route('/users/signout', methods=['GET', 'POST'])
def users_signout():
    """User signout functionality."""
    logout_user()
    return redirect(url_for('index'))

# End of sign in/ sign-up/ sign out 
###########################################################################################################


###########################################################################################################
# Start of user-facing routes

# End of user-facing routes 
###########################################################################################################


###########################################################################################################
# Start of admin-facing routes

# users listing page
@app.route('/users')
@login_required     
def list_users(): 
    users = User.query.all()
    return render_template('users.html', users=users, user=current_user)

@app.route('/events')
@login_required     
def list_events(): 
    events= Event.query.all()
    return render_template('events.html', events=events, user=current_user)

# End of admin-facing routes 
###########################################################################################################
