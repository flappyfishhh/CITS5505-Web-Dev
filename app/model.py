from datetime import datetime
from app import db

class User(db.Model):
    user_id = db.Colum(db.Integer, primary_key = True)
    user_name = db.Colum(db.string(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    request = db.relationship('Request', backref='author', lazy=True)

class Tag(db.Model):
    tag_id = db.Colum(db.Integer, primary_key = True)
    tag_name = db.Colum(db.string(30), nullable=False)

class Request(db.Model):
    requst_id = db.Colum(db.Integer, primary_key = True)
    Request_title = db.Colum(db.string(100), nullable=False)
    Request_content = db.Colum(db.string(1000))
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.UTC)
    user_id = db.Column(db.Integer, db.ForeignKey(User.user_id), nullable=False)
    tags = db.relationship('Tag', secondary='post_tag', backref='posts', lazy='dynamic')
    

# Many-to-Many association table for requests and tags
post_tag = db.Table('post_tag',
    db.Column('requst_id', db.Integer, db.ForeignKey(Request.requst_id), primary_key=True),
    db.Column('tag_id', db.Integer, db.ForeignKey(Tag.tag_id), primary_key=True)
)


