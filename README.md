# What is Django?

## the Python Web framework for perfectionists with deadlines.

# Run app

- python3 manage.py runserver
- I still do not know how to recreate the venv since it should be ignored by git
- endpoints:
  - http://localhost:8000/admin
  - http://localhost:8000/movies
  - http://localhost:8000/movies/:id

# Steps to create project

- mkdir anime_die_heart
- cd anime_die_heart
- virtualenv venv
- source venv/bin/activate
  - or you can follow my steps to deligate this task to VSCode
- pip3 install django
- django-admin startapp anime_die_heart
  - Our main module. Kinda AppModule
- python3 anime_die_heart/manage.py startapp watch_list_app
  - Or you can reopen vscode with anime_die_heart/anime_die_heart
    - python3 manage.py startapp watch_list_app
- python3 manage.py runserver
- We need to apply some migrations because we already have our database
  - python3 manage.py migrate
- Now we create super user:
  - python3 manage.py createsuperuser

# [Dealing with models](https://docs.djangoproject.com/en/4.0/ref/models/)

- Change the `models.py` as you wanted
- python3 manage.py makemigrations
- python3 manage.py migrate
- Then register it in the `admin.py`: `admin.site.register(Movie)`

# [Dealing with views]()

- We have 2 option:
  - Function base view
    - `@api_view(["POST"])`
      - A simple decorator that wrap your function based views to ensure they receive an instance of `Request` (rather than the usual Django `HttpRequest`)
      - Return a `Response` (instead of a Django `HttpResponse`)
      - A list of HTTP methods that your view should respond to.
  - Class base view
- Read `watch_list_app/views.py` for more information
- As you realized this is too much effort to do a simple task, Besides it is numbness routing and a sterile repetitive task, I guess we would become heartless after a while. So if you wanted to start a quest to find a better solution and get rid of this miserable degradation situation probably you should try Django REST framework. It inspires you.
- File upload:
  - MultiPartParser
    - For web-based uploads, or for native clients with multipart upload support.
  - FileUploadParser
    - For native clients that can upload the file as a raw data request.
  - [Reference](https://roytuts.com/single-and-multiple-files-upload-example-in-django-rest-api/)

# Django REST framework

- pip3 install djangorestframework
- Open `settings.py` and do this:
  ```py
  INSTALLED_APPS = [
    # ...
    'rest_framework'
    # ...
  ]
  ```
- Serialization: Complex data -> Python Dictionary -> JSON
  - Serialization types
  - Convert complex data such as `querysets` and `model instances` to native Python datatypes.
- Deserialization: JSON -> Python Dictionary -> Complex data
- It includes a number of built in Parser classes, that allow you to accept requests with various media types.

# Models in Django

- [Fields](https://docs.djangoproject.com/en/4.0/ref/models/fields/)

https://github.com/gnulnx/django-mongolog
