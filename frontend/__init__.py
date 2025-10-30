"""Frontend package: Flask application and extensions."""

from flask import Flask
from werkzeug.utils import secure_filename
import os


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

from frontend import routes
