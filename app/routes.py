from flask import render_template, redirect,url_for, session, flash, request
from app import app,db
from app.model import User,Tag,Request,Response
from app.forms import LoginForm, RegistrationForm
from flask_login import current_user, login_user, login_required, logout_user
import sqlalchemy as sa
from urllib.parse import urlsplit


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
        # next_page = request.args.get('next')
        # if not next_page or urlsplit(next_page).netloc != '':
        #     next_page = url_for('index')
        return redirect(url_for('index'))
    return render_template('login.html', title='Log In', form=form)

# register page
@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(user_name=form.username.data, email=form.email.data)
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


@app.route('/requests/<int:request_id>', methods=['GET', 'POST'])
@login_required
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
@login_required
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
@login_required
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
@login_required
def myProfile():
    # Only when user has logged in 
    if 'user_id' in session:
        user_id = session['user_id']
        user = User.query.get_or_404(user_id)
        posts = Request.query.filter_by(user_id=user_id).all()
        responses = Response.query.filter_by(user_id=user_id).all()
        if(user.avatar_filename):
            image = "/static/user-account-image/"+user.avatar_filename
        else:
            image = "/static/user-account-image/default.png"
        return render_template('my-profile.html', user=user, posts=posts, responses=responses,user_image=image)
    return render_template('login.html')

# change user name
@app.route('/update_user', methods=['POST'])
@login_required
def update_user():
    new_username = request.form['username']
    user = User.query.get(session['user_id'])
    user.user_name = new_username
    db.session.commit()
    return redirect(url_for('myProfile'))

# delete request
@app.route('/delete_post/<int:post_id>', methods=['POST'])
@login_required
def delete_post(post_id):
    post = Request.query.get_or_404(post_id)
    if post.author.user_id == session['user_id']:
        db.session.delete(post)
        db.session.commit()
    return redirect(url_for('myProfile'))

# delete response 
@app.route('/delete_response/<int:response_id>', methods=['POST'])
@login_required
def delete_response(response_id):
    response = Response.query.get_or_404(response_id)
    if response.contributor.user_id == session['user_id']:
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
        user_id = str(session['user_id'])
        filename = user_id+'.jpg'
        os.makedirs(UPLOAD_FOLDER, exist_ok=True)
        print('Saving file to:', os.path.join(app.config['UPLOAD_FOLDER'], filename))
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        # Update the user's avatar_filename in the database
        user = User.query.get(session['user_id'])
        user.avatar_filename = filename
        db.session.commit()
    return redirect(url_for('myProfile'))