from flask import jsonify, render_template, redirect,url_for
from app import app
from app.model import User,Tag,Request
from flask import request

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

@app.route('/')
@app.route('/index')
def index():
    
    return render_template("index.html", title="Home", user=user,
    posts=posts)


@app.route('/view-request')
def ViewRequest():
    return render_template("view-request.html", title="View the request")

@app.route('/create-request')
def CreateRequest():
    return render_template("create-request.html", title="Create the request",Request=[])

# submit page to confirm the submitting of new request
@app.route('/submit',methods=['post'])
def Submit():
    print('Submitted!')
    return redirect(location = url_for('ViewRequest'))

@app.route('/search', methods=['POST'])
def search():
    data = request.get_json()
    query = data.get('query', '').strip()
    if query != '':
        results = search_posts(query)
        return render_template('search-results.html', posts=results, empty=False)
    else:
        return render_template('search-results.html', posts=posts, empty=True)

def search_posts(query):
    matching_posts = [post for post in posts if query.lower() in post['body'].lower()]
    return matching_posts

