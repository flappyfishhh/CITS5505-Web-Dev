from flask import render_template
# from app import app
from flask import Flask
app = Flask("__name__",template_folder="./app/templates")



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

@app.route("/login",methods=['GET'])
def Login():
    return render_template("login.html",title="User Login")