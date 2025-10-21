"""Website routing."""

from frontend import app
from flask import render_template, request, jsonify, session
import os
import time


UPLOAD_DIR = os.path.join('backend', 'uploads')
progress_dict = {}



@app.route('/')
@app.route('/index')
@app.route('/index.html')
def index():
    return render_template('index.html')


