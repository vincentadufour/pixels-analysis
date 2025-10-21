"""Models for Flask to use."""

from frontend import db
from flask_login import UserMixin


class User(db.Model, UserMixin):
    """The User class."""

    __tablename__ = "users"
    id = db.Column(db.String, primary_key=True)
    email = db.Column(db.String)
    passwd = db.Column(db.LargeBinary)
