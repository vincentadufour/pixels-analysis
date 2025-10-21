"""Frontend package: Flask application and extensions."""

from flask import Flask
import os

app = Flask("frontend", template_folder="templates")

# Secret key (use environment variable in production).
app.secret_key = os.environ.get("SECRET_KEY", "secret key")
app.config["USER SIGNUP"] = "User Sign Up"
app.config["USER SIGNIN"] = "User Sign In"

# Database initialization.
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()
app.config.setdefault("SQLALCHEMY_DATABASE_URI", "sqlite:///app.db")
db.init_app(app)

# Login manager.
from flask_login import LoginManager
login_manager = LoginManager()
login_manager.init_app(app)

# User loader callback.
from frontend.models import User


@login_manager.user_loader
def load_user(id):
    try:
        return db.session.query(User).filter(User.id == id).one()
    except Exception:
        return None

from frontend import routes
