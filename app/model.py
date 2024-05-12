from datetime import datetime
from app import db

class User(db.Model):
    user_id = db.Column(db.Integer, primary_key = True)
    user_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    request = db.relationship('Request', backref='author', lazy=True)
    avatar_filename = db.Column(db.String(60), nullable=True)
    response_contributor = db.relationship('Response', backref='contributor', lazy=True)

    #print the user if and user name
    def __repr__(self) -> str:
        return f'User {self.user_id},{self.user_name},{self.avatar_filename }'

class Tag(db.Model):
    tag_id = db.Column(db.Integer, primary_key = True)
    tag_name = db.Column(db.String(30), nullable=False)

class Request(db.Model):
    request_id = db.Column(db.Integer, primary_key = True)
    request_title = db.Column(db.String(100), nullable=False)
    request_content = db.Column(db.String(1000))
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey(User.user_id), nullable=False)
    tags = db.relationship('Tag', secondary='post_tag', backref='posts', lazy='dynamic')
    response = db.relationship('Response', backref='response', lazy=True)

    #print the request detail
    def __repr__(self) -> str:
        return f'User {self.request_id},{self.date_posted}'
    
class Response(db.Model):
    response_id = db.Column(db.Integer, primary_key = True)
    response_content = db.Column(db.String(1000))
    date_responded = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey(User.user_id), nullable=False)
    request_id = db.Column(db.Integer, db.ForeignKey(Request.request_id), nullable=False)

    #print the response detail
    def __repr__(self) -> str:
        return f'Response id: {self.response_id},Request id:{self.request_id}, Response content:{self.response_content}'
    

# Many-to-Many association table for requests and tags
post_tag = db.Table('post_tag',
    db.Column('request_id', db.Integer, db.ForeignKey(Request.request_id), primary_key=True),
    db.Column('tag_id', db.Integer, db.ForeignKey(Tag.tag_id), primary_key=True)
)


