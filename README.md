# CITS5505

CITS5505 Group Project


# Community Board Web Application

This web application is designed for a community board purpose, but it is versatile enough to be used for various purposes. Its primary functions are listed below:

## Features

1. **Create a Request (Post)**

   - Users can create a request with a title, content, and tags. Tags act as categories for requests, and users have the flexibility to create any tags they like.

2. **View Requests**

   - **Home Page**: Displays the latest 5 posts.
   - **Search Result Page**: Users can search for requests by titles, usernames, and tag names. All matching requests are displayed.
   - **View Specific Request Page**: Users can view the details of a specific request by clicking on it.
   - **Tags Page**: Tags displayed on the specific request page are clickable. Clicking a tag displays a page with all requests containing the same tag.

3. **Add Response**

   - On the specific request page, users can add responses to the request.

4. **Manage Personal Profile**

   - **Username**: Can be changed.
   - **User Account Image**: Initially a default image. Users can upload and change their account image.
   - **User Password**: Can be changed after verifying the current password.

5. **Trace Requests and Responses**
   - On the profile page, users can trace all their past requests and responses. They also have the option to delete them.

## Usage

1. **Creating a Request**

   - Navigate to the "Create Request" page.
   - Fill in the title, content, and tags.
   - Submit to create the request.

2. **Viewing Requests**

   - **Home Page**: Check the latest 5 posts.
   - **Search**: Use the search bar to find requests by title, username, or tag.
   - **Specific Request**: Click on any request title to view its details.
   - **Tags**: Click on any tag within a request to see all requests with that tag.

3. **Adding a Response**

   - Navigate to a specific request page.
   - Enter your response in the provided field.
   - Submit to add your response.

4. **Managing Profile**

   - Go to the "My Profile" page.
   - Change your username, upload/change your account image, or change your password.

5. **Tracing and Managing Requests/Responses**
   - On the "My Profile" page, view all your past requests and responses.
   - Optionally delete any request or response.

## Design

- **Backend**: Implemented with Flask, managing routing, and handling database operations.
- **Frontend**: Designed with HTML, CSS, JQuery, and AJAX for dynamic interactions.
- **Database**: Uses SQLite for database interactions, supporting user authentication, request creation, tagging, and responses.
- **Websockets**: Used for real-time updates and dynamic interactions.

## Team Information

| UWA ID   | Name            | Github User Name             |
| -------- | --------------- | ---------------------------- |
| 23927347 | Nanxi Rao       | flappyfishhh                 |
| 23740033 | Zhengyuan Zhang | ivyhzyb Ivy(Zhengyuan) Zhang |
| 23829237 | Ankita Narvekar | 23829237                     |
| 24112813 | Shuyu Xie       | shuyux                       |

## Instruction to launch the app

1. Clone the repository:

   ```bash
   git clone https://github.com/your-repo/community-board-app.git
   cd community-board-app

   ```

2. Set up a virtual environment:

   ```bash
   python3 -m venv env
   source env/bin/activate # On Windows use `env\Scripts\activate`

   ```

3. Install the required dependencies:

   ```bash
   pip install -r requirements.txt

   ```

4. Upgrade the database:

   ```bash
   flask db upgrade

   ```

5. Open the Flask shell:

   ```bash
   flask shell

   ```

6. In the Flask shell, run the following commands to set up the database with test data:

   ```python
   from app import db
   import app.db_test_data

   ```

7. Exit the flask shell and run the app:

   ```bash
   flask run

   ```

8. Open your browser and navigate to:
   http://127.0.0.1:5000

## Test
1. Unit Testing
   There are 5 unit testcases in unit.py file for scenarios: delete_request, delete_response,create reqest and response and password hasing.

2. System Testing
   The selenium.py file has 3 system testcases verifying the login success, login error and registeration functionality.

Instructions to run testcases:
1. Update to latest chrome version:
   ```
      sudo apt-get install -y google-chrome-stable
   ```

2. Requirements.txt file has all requirements related to selenium.
   ```
      pip install -r requirements.txt 
   ```
  
3. Run unit tests.
   ```
      python -m unittest tests/unit.py
   ```

4. Run selenium tests.
   ```
   python -m unittest tests/selenium.py
   ```

