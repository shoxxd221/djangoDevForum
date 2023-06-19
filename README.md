# DeveloperForum

This is a forum for developers, created using the Django framework and SQLite database.

## Installation

1. Clone the repository:

   
   git clone https://github.com/shoxxd221/djangoDevForum.git
   

2. Change into the project directory:

   
   cd developerForum
   

3. Create a virtual environment:

   
   python -m venv venv
   

4. Activate the virtual environment:

   
   source venv/bin/activate
   

5. Install the dependencies:

   
   pip install Django==3.2
   

   pip install Pillow
   

6. Create the database:

   
   python manage.py migrate
   

7. Create a superuser:

   
   python manage.py createsuperuser


## Project Structure

- developerForum/ - the project root directory.
- forumFunctional/ - the forum application directory.
- templates/ - the directory containing templates.
- static/ - the directory containing static files.
- db.sqlite3 - the SQLite database file.
- manage.py - the file for managing the project.
- media/ - the directory containing post and user images.