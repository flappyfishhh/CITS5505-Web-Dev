from datetime import datetime
from app import db
from app.model import *


# Create users
user1 = User(user_name='john_doe', email='john@example.com', avatar_filename="1.jpg")
user1.set_password('password1')

user2 = User(user_name='jane_smith', email='jane@example.com', avatar_filename="2.jpg")
user2.set_password('password2')

user3 = User(user_name='alice_wong', email='alice@example.com', avatar_filename="3.jpg")
user3.set_password('password3')

user4 = User(user_name='bob_johnson', email='bob@example.com', avatar_filename="4.jpg")
user4.set_password('password4')

user5 = User(user_name='carol_davis', email='carol@example.com', avatar_filename="default.png")
user5.set_password('password5')

# Create requests
request1 = Request(request_title='Best Practices for Python', request_content='Can anyone share the best practices for writing clean and efficient Python code?', author=user1)
request2 = Request(request_title='Getting Started with Flask', request_content='I am new to Flask. Can someone guide me on how to get started with it?', author=user2)
request3 = Request(request_title='Database Design Tips', request_content='Looking for tips on designing a scalable database schema for a new project.', author=user3)
request4 = Request(request_title='Debugging Techniques', request_content='What are some effective debugging techniques for web applications?', author=user4)
request5 = Request(request_title='Learning SQLAlchemy', request_content='What are some good resources for learning SQLAlchemy?', author=user5)

# Create tags
tag1 = Tag(tag_name='Python')
tag2 = Tag(tag_name='Flask')
tag3 = Tag(tag_name='SQLAlchemy')
tag4 = Tag(tag_name='Database')
tag5 = Tag(tag_name='Debugging')

# Create responses
response1 = Response(response_content='Here are some best practices: use meaningful variable names, keep functions small, and write unit tests.', response=request1, contributor=user2)
response2 = Response(response_content='To get started with Flask, you should first read the official documentation and follow a few tutorials.', response=request2, contributor=user3)
response3 = Response(response_content='For a scalable database design, consider using normalization and indexing appropriately.', response=request3, contributor=user4)
response4 = Response(response_content='Effective debugging techniques include using breakpoints, logging, and reading stack traces.', response=request4, contributor=user5)
response5 = Response(response_content='The official SQLAlchemy documentation and the book "Essential SQLAlchemy" are great resources.', response=request5, contributor=user1)
response6 = Response(response_content='Another tip for Python best practices: avoid using global variables and prefer local variables instead.', response=request1, contributor=user3)
response7 = Response(response_content='For Flask, you might want to check out the Flask Mega-Tutorial by Miguel Grinberg.', response=request2, contributor=user4)
response8 = Response(response_content='Also, make sure to use ORM in your database design for easier data management.', response=request3, contributor=user5)
response9 = Response(response_content='Using a debugger tool like pdb in Python can significantly improve your debugging process.', response=request4, contributor=user1)
response10 = Response(response_content='For learning SQLAlchemy, practicing by creating small projects can be very helpful.', response=request5, contributor=user2)

# Add tags to requests
request1.tags.append(tag1)
request1.tags.append(tag2)
request2.tags.append(tag2)
request2.tags.append(tag3)
request3.tags.append(tag4)
request3.tags.append(tag1)
request4.tags.append(tag5)
request4.tags.append(tag2)
request5.tags.append(tag3)
request5.tags.append(tag5)


# Commit the records to the database
db.session.add(user1)
db.session.add(user2)
db.session.add(user3)
db.session.add(user4)
db.session.add(user5)
db.session.add(request1)
db.session.add(request2)
db.session.add(request3)
db.session.add(request4)
db.session.add(request5)
db.session.add(tag1)
db.session.add(tag2)
db.session.add(tag3)
db.session.add(tag4)
db.session.add(tag5)
db.session.add(response1)
db.session.add(response2)
db.session.add(response3)
db.session.add(response4)
db.session.add(response5)
db.session.add(response6)
db.session.add(response7)
db.session.add(response8)
db.session.add(response9)
db.session.add(response10)
# db.session.commit()

try:
    db.session.commit()
except:
    db.session.rollback()
    raise