from flask import render_template, redirect, url_for
from app import app
from app.model import User

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

# submit page to confirm the submitting of new request

@app.route('/submit',methods=['post'])
def Submit():
    print('Submitted!')
    return redirect(location = url_for('ViewRequest'))

