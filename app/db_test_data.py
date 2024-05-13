from datetime import datetime
from app import db
from app.model import *


# Create users
user1 = User(user_name='john_doe', email='john@example.com',avatar_filename="1.jpg")
# will change to secure way later
user1.set_password('password1')
user2 = User(user_name='jane_smith', email='jane@example.com',avatar_filename="2.jpg")
user2.set_password('password2')

# Create requests
request1 = Request(request_title='First Request', request_content='This is the content of the first Request.', author=user1)
request2 = Request(request_title='Second Request', request_content='This is the content of the second Request.', author=user2)

# Create tags
tag1 = Tag(tag_name='Python')
tag2 = Tag(tag_name='Flask')
tag3 = Tag(tag_name='SQLAlchemy')

# Create reponses
response1 = Response(response_content='This is a response to request1',response=request1,contributor = user2)
response2 = Response(response_content='This is a response to request2',response=request2,contributor = user1)

# Add tags to posts
request1.tags.append(tag1)
request1.tags.append(tag2)
request2.tags.append(tag2)
request2.tags.append(tag3)


# Commit the records to the database
db.session.add(user1)
db.session.add(user2)
db.session.add(request1)
db.session.add(request2)
db.session.add(tag1)
db.session.add(tag2)
db.session.add(tag3)
db.session.add(response1)
db.session.add(response2)
# db.session.commit()

try:
    db.session.commit()
except:
    db.session.rollback()
    raise