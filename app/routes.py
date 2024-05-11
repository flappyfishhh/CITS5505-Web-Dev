from flask import jsonify, render_template, redirect,url_for, session
from app import app,db
from app.model import User,Tag,Request
from flask import request

app.secret_key = "My Secret key"  
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
#Log in page
@app.route('/')
@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # Query the user from the database
        user = User.query.filter_by(email=email).first()

        if user and password == user.password:
            # Login successful, store the user ID in the session
            session['user_id'] = user.user_id
            return redirect(url_for('index'))
        else:
            # Login failed
            return(render_template('login.html',error='Invalid username or password'))
    return render_template('login.html')


# register page
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        # Query the user from the database
        user = User.query.filter_by(email=email).first()

        if(user):
            # user already exist
            error = 'User already exist.'
            return render_template('register.html',error=error)
        else:
            # Create a new user
            new_user = User(user_name=username, email=email, password=password)
            db.session.add(new_user)
            db.session.commit()

            return redirect(url_for('login'))
    return render_template('register.html')

#homepage
@app.route('/index')
def index():
    return render_template("index.html", title="Home", user=user,
    posts=posts)


@app.route('/requests/<int:request_id>')
def ViewRequest(request_id):
    new_request = Request.query.get_or_404(request_id)
    return render_template("view-request.html", request=new_request)

@app.route('/create-request', methods=['GET', 'POST'])
def CreateRequest():
    # Only when user has logged in 
    if 'user_id' in session:
        if request.method == 'POST':
            user_id = session['user_id']
            print(user_id)
            user = User.query.get(user_id)
            title = request.form['requestTitle']
            content = request.form['requestContent']
            tag_names = [tag.strip() for tag in request.form['tags'].split(',')]
            tags = []
            for tag_name in tag_names:
                tag = Tag.query.filter_by(tag_name=tag_name).first()
                if not tag:
                    tag = Tag(tag_name=tag_name.strip())
                    db.session.add(tag)
                tags.append(tag)
            new_request = Request(request_title=title, request_content=content, tags=tags,author=user)
            new_request.tags.extend(tags)
            db.session.add(new_request)
            db.session.commit()
            return redirect(url_for('ViewRequest',request_id=new_request.request_id))
        return render_template('create-request.html')

    return render_template(login.html)
    

# submit page to confirm the submitting of new request
# @app.route('/submit',methods=['post'])
# def Submit():
#     print('Submitted!')
#     return redirect(location = url_for('ViewRequest'))

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

