"""Frontend package: Flask application and extensions."""

from flask import Flask
import os

app = Flask(__name__)

from frontend import routes
