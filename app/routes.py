CreateHomePage
from app import appFlask
from flask import render_template

@appFlask.route("/")
def index():
    return render_template('createRequest.html')

from flask import render_template
from app import app

@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Admin'}
    posts = [
    {
        'author': {'username': 'John'},
        'body': 'Beautiful day in Portland!'
    },
    {
        'author': {'username': 'Susan'},
        'body': 'The Avengers movie was so cool!'
    }
    ]
    return render_template("index.html", title="Home", user=user,
    posts=posts)

@app.route('/view-request')
def ViewRequest():
    return render_template("view-request.html", title="View the request")

@app.route('/create-request')
def CreateRequest():
    return render_template("create-request.html", title="Create the request")

main
