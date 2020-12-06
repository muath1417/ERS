# ERS
## Python and Django web app project
### Django files:
    .
        ├── ERS
        │   ├── asgi.py
        │   ├── __init__.py
        │   ├── settings.py
        │   ├── urls.py
        │   └── wsgi.py
        └── manage.py

    -   manage.py automatically generated
    -   db.sqlite3 database sqlite 
    -   ERS default app (django app)
    -   ERS/settings.py stttings files for the django application
    -   ERS/urls.py url accessable in the web app
    -   ERS/middleware.py middleware process_request which is called for every request.
        process_request process set the request.student variable to the currect student else the normal user
    -   media folder where the app stores the uploaded files
    -   static folder where we store/put the css js files
    -   Student is a small app in ERS portal
    -   Student/fixtures folder contains data for database initialization
    -   Student/migrations folder is auto generated about the models changes in db
    -   Student/admin.py file registers the all the models in the Student app
    -   Student/app.py file contains the config for Student app
    -   Student/forms.py contains the forms used in app like signup login etc.
    -   Student/models.py contains the DB Models used in the app
    -   Student/storage.py contains method to store the file and if file exist then update file.
    -   Student/urls.py contains the urls accessing by the student
    -   Student/views.py contains the view function which returns the html page and data as per request.
    -   Student/validators.py contains the file excention validation function


## Added Configuration in settings.py
    
        ```
            STATIC_URL = '/static/'
            STATICFILES_DIRS = [
                os.path.join(BASE_DIR, "static"),
            ]
            STATIC_DIR = os.path.join(BASE_DIR,'static')
            STATIC_URL = '/static/'
            STATICFILES_DIRS = [STATIC_DIR,]
            
            MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
            MEDIA_URL = '/media/'
            CRISPY_TEMPLATE_PACK = 'bootstrap4'
            LOGIN_REDIRECT_URL = '/student/home'
            
            DJANGO_SUPERUSER_USERNAME='admin'
            DJANGO_SUPERUSER_PASSWORD='admin@123'
            DJANGO_SUPERUSER_EMAIL='admin@localhost.com'
            AUTH_PASSWORD_VALIDATORS=[]
            LOGIN_URL = '/login/'
            
            LOGIN_REDIRECT_URL = '/'
            
            # Add user_unique_email to INSTALLED_APPS
            INSTALLED_APPS.append('user_unique_email')
            
            # Custom User model
            AUTH_USER_MODEL = 'user_unique_email.User'
        ```
        -    we are using AUTH_USER_MODEL as user_unique_email.User as this has unique email
    

## Models used:
       -    Student
       -    Course
       -    FileType
       -    Post
       -    PostLikes
       -    PostDislikes
## Added Files:
.
├── clear_all.sh
├── db.sqlite3
├── ERS
│   ├── asgi.py
│   ├── __init__.py
│   ├── middleware.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── manage.py
├── media
│   ├── courses
│   │   ├── course.png
│   │   └── courses.png
│   ├── posts
│   └── students
├── readme.md
├── requirements.txt
├── static
│   ├── css
│   │   └── profile.css
│   └── js
│       ├── course_search.js
│       └── jsi18.js
├── Student
│   ├── admin.py
│   ├── apps.py
│   ├── fixtures
│   │   ├── Course.json
│   │   ├── FileType.json
│   │   └── Student.json
│   ├── forms.py
│   ├── __init__.py
│   ├── migrations
│   │   ├── 0001_initial.py
│   │   ├── __init__.py
│   ├── models.py
│   ├── storage.py
│   ├── tests.py
│   ├── urls.py
│   ├── validators.py
│   └── views.py
└── templates
    └── Student
        ├── about.html
        ├── base.html
        ├── courses.html
        ├── guidelines.html
        ├── home.html
        ├── index.html
        ├── login.html
        ├── my_timeline.html
        ├── password_change_form.html
        ├── post.html
        ├── profile_card.html
        ├── profile.html
        ├── registration.html
        └── timeline.html


## Django Admin
    -    The Django admin site¶
    -    One of the most powerful parts of Django is the automatic admin interface. It reads metadata from your models to provide a quick, model-centric interface where trusted users can manage content on your site. The admin’s recommended use is limited to an organization’s internal management tool. It’s not intended for building your entire front end around.
    -    The admin has many hooks for customization, but beware of trying to use those hooks exclusively. If you need to provide a more process-centric interface that abstracts away the implementation details of database tables and fields, then it’s probably time to write your own views.
    -    https://docs.djangoproject.com/en/3.1/ref/contrib/admin/

## Forms
    -    we have used different forms for different purpose.
    -   like register, login, post etc.


## templates
    -    Templates are stored in templates/Student folder
    -   The templates are html templates for login register post etc
    

## Clear all
    - the file clear_all.sh is a bash file use to clear db and files and reset the website

## Sqlite DB
    -    We have used SQLIte DB for database to store the data.
    
## requirements.txt
    -    this file contains the python modules used in this project.
    