from flask import render_template, redirect,url_for, session, flash, request,jsonify
from app import app,db
from app.model import User,Tag,Request,Response
from app.forms import LoginForm, RegistrationForm,CreateRequestForm
from flask_login import current_user, login_user, logout_user
import sqlalchemy as sa
from urllib.parse import urlsplit
import os


#Log in page
@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.scalar(
            sa.select(User).where(User.email == form.email.data))
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user)
        return redirect(url_for('index'))
    return render_template('login.html', title='Log In', form=form)

# register page
@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(user_name=form.username.data, email=form.email.data,avatar_filename = 'default.png')
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

# logout
@app.route('/logout')
def Logout():
    logout_user()
    return redirect(url_for('login'))

#homepage
@app.route('/index')
def index():
    # Query the top 5 latest posts
    requests = Request.query.order_by(Request.date_posted.desc()).limit(5).all()
    return render_template("index.html", title="Home", current_user=current_user,
    posts=requests)

# View the request and upload a response
@app.route('/requests/<int:request_id>', methods=['GET', 'POST'])
def ViewRequest(request_id):
    new_request = Request.query.get_or_404(request_id)
    if request.method == 'POST':
        if current_user.is_authenticated:
            user_id = current_user.user_id
            response_content = request.form['response']
            new_response = Response(response_content=response_content, user_id=user_id, request_id=request_id)
            db.session.add(new_response)
            db.session.commit()
            return redirect(url_for('ViewRequest', request_id=request_id))
        else:
            return redirect(url_for('login'))
    return render_template("view-request.html", request=new_request)

# display requests having the same tag
@app.route('/tag_requests/<tag>', methods=['GET'])
def tag_requests(tag):
    requests = Request.query.join(Tag, Request.tags).filter(Tag.tag_name.contains(tag)).all()
    return render_template('tag-requests.html', tag=tag, results=requests)

# create a request with title, content and tags
@app.route('/create-request', methods=['GET', 'POST'])
def CreateRequest():
    # Only when user has logged in 
    form = CreateRequestForm()
    if current_user.is_authenticated:
        if request.method == 'POST':
            user_id = current_user.user_id
            user = User.query.get(user_id)
            title = form.request_title.data
            content = form.request_content.data
            tag_names = [tag.strip() for tag in (form.tags.data).split(',')]
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
        return render_template('create-request.html',form=form)
    return redirect(url_for('login'))
    


# Search function. Can search by title, user name and tags.
@app.route('/search')
def search():
    query = request.args.get('query')
    # search by requst title, content and user name
    results = Request.query.join(User).join(Tag, Request.tags).filter(
        (Request.request_title.contains(query)) |
        (User.user_name.contains(query)) |
        (Tag.tag_name.contains(query))
    ).all()
    return render_template('search.html', results=results)

# my profile page
@app.route('/my-profile')
def myProfile():
    # Only when user has logged in 
    if current_user.is_authenticated:
        user_id = current_user.user_id
        user = User.query.get_or_404(user_id)
        posts = Request.query.filter_by(user_id=user_id).all()
        responses = Response.query.filter_by(user_id=user_id).all()
        if(user.avatar_filename):
            image = "/static/user-account-image/"+user.avatar_filename
        else:
            image = "/static/user-account-image/default.png"
        return render_template('my-profile.html', user=user, posts=posts, responses=responses,user_image=image)
    return redirect(url_for('login'))

# change user name
@app.route('/update_user', methods=['POST'])
def update_user():
    new_username = request.form['username']
    user = User.query.get(current_user.user_id)
    user.user_name = new_username
    db.session.commit()
    return redirect(url_for('myProfile'))

# change user password
@app.route('/update_password',methods=['POST'])
def update_password():
    password_old = request.json['password_old']
    password_new = request.json['password_new']
    # verify password
    user = User.query.get(current_user.user_id)
    if user is None or not user.check_password(password_old):
        return jsonify(code=1,msg="wrong password!")
    user.set_password(password_new)
    db.session.commit()
    return jsonify(code=0,msg="Password reset complete")

# delete request
@app.route('/delete_post/<int:post_id>', methods=['POST'])
def delete_post(post_id):
    post = Request.query.get_or_404(post_id)
    if post.author.user_id == current_user.user_id:
        # Delete all the responses first
        responses = Response.query.filter_by(request_id=post_id).all()
        for response in responses:
            db.session.delete(response)
        db.session.delete(post)
        db.session.commit()
    return redirect(url_for('myProfile'))

# delete response 
@app.route('/delete_response/<int:response_id>', methods=['POST'])
def delete_response(response_id):   
    response = Response.query.get_or_404(response_id)
    if response.contributor.user_id == current_user.user_id:
        db.session.delete(response)
        db.session.commit()
    return redirect(url_for('myProfile'))

# allow users to upload image for their account and store in the following folder
UPLOAD_FOLDER = './app/static/user-account-image'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/upload_avatar', methods=['POST'])
def upload_avatar():
    if 'file' not in request.files:
        print('file not found')
        # Handle error
    file = request.files['file']
    if file.filename == '':
        print('file not found')
        # Handle error
    if file:
        user_id = str(current_user.user_id)
        filename = user_id+'.jpg'
        os.makedirs(UPLOAD_FOLDER, exist_ok=True)
        print('Saving file to:', os.path.join(app.config['UPLOAD_FOLDER'], filename))
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        # Update the user's avatar_filename in the database
        user = User.query.get(current_user.user_id)
        user.avatar_filename = filename
        db.session.commit()
    return redirect(url_for('myProfile'))