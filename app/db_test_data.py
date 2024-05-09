from datetime import datetime
from app import db
from app.model import *

# user1 = User(user_id = 1,user_name = 'user1', email='test@testmail',password='password')

# tag1 = Tag(tag_id = 1, tag_name='test tag' )

# request1 = Request(request_id = 1, request_title = 'test request',request_content = 'test',date_posted = datetime.now(),user_id = 1)

# Create users
user1 = User(user_name='john_doe', email='john@example.com', password='password123')
user2 = User(user_name='jane_smith', email='jane@example.com', password='password456')

# Create requests
request1 = Request(request_title='First Request', request_content='This is the content of the first Request.', author=user1)
request2 = Request(request_title='Second Request', request_content='This is the content of the second Request.', author=user2)

# Create tags
tag1 = Tag(tag_name='Python')
tag2 = Tag(tag_name='Flask')
tag3 = Tag(tag_name='SQLAlchemy')

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
# db.session.commit()

try:
    db.session.commit()
except:
    db.session.rollback()
    raise