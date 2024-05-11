from flask import jsonify, render_template, redirect,url_for, session, g
from app import app,db
from app.model import User,Tag,Request,Response
from flask import request

app.secret_key = "My Secret key"
# pass current user information to base.html
@app.before_request
def before_request():
    g.user = None
    if 'user_id' in session:
        g.user = User.query.get(session['user_id'])

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

# logout
@app.route('/logout')
def Logout():
    session.pop('user_id', None)
    return redirect(url_for('login'))

#homepage
@app.route('/index')
def index():
    # Query the top 5 latest posts
    requests = Request.query.order_by(Request.date_posted.desc()).limit(5).all()
    return render_template("index.html", title="Home",
    posts=requests)


@app.route('/requests/<int:request_id>', methods=['GET', 'POST'])
def ViewRequest(request_id):
    new_request = Request.query.get_or_404(request_id)
    if request.method == 'POST':
        if 'user_id' in session:
            response_content = request.form['response']
            user_id = session['user_id']  
            new_response = Response(response_content=response_content, user_id=user_id, request_id=request_id)
            db.session.add(new_response)
            db.session.commit()
            return redirect(url_for('ViewRequest', request_id=request_id))
        else:
            return render_template('login.html')
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

    return render_template('login.html')
    

# submit page to confirm the submitting of new request
# @app.route('/submit',methods=['post'])
# def Submit():
#     print('Submitted!')
#     return redirect(location = url_for('ViewRequest'))

@app.route('/search')
def search():
    query = request.args.get('query')
    # search by requst title, content and user name
    results = Request.query.filter(
        (Request.request_title.contains(query)) | (Request.request_content.contains(query))|
            (User.user_name.contains(query))
    ).all()
    return render_template('search.html', results=results)

# my profile page
@app.route('/my-profile')
def myProfile():
    # Only when user has logged in 
    if 'user_id' in session:
        user_id = session['user_id']
        user = User.query.get_or_404(user_id)
        posts = Request.query.filter_by(user_id=user_id).all()
        responses = Response.query.filter_by(user_id=user_id).all()
        return render_template('my-profile.html', user=user, posts=posts, responses=responses)
    return render_template('login.html')

# change user name
@app.route('/update_user', methods=['POST'])
def update_user():
    new_username = request.form['username']
    user = User.query.get(session['user_id'])
    user.user_name = new_username
    db.session.commit()
    return redirect(url_for('myProfile'))

# delete request
@app.route('/delete_post/<int:post_id>', methods=['POST'])
def delete_post(post_id):
    post = Request.query.get_or_404(post_id)
    if post.author.user_id == session['user_id']:
        db.session.delete(post)
        db.session.commit()
    return redirect(url_for('myProfile'))