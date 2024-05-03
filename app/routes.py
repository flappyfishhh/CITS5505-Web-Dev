from app import appFlask
from flask import render_template

@appFlask.route("/")
def index():
    return render_template('createRequest.html')