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
  - Class base view
- Read `watch_list_app/views.py` for more information
- As you realized this is too much effort to do a simple task, Besides it is numbness routing and a sterile repetitive task, I guess we would become heartless after a while. So if you wanted to start a quest to find a better solution and get rid of this miserable degradation situation probably you should try Django REST framework. It inspires you.

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
- Deserialization: JSON -> Python Dictionary -> Complex data

# Django + MongoDB

- Django includes an ORM, `django.db`.
- **No** official MongoDB backend for Django.
- [Django MongoDB Engine](https://django-mongodb-engine.readthedocs.io/en/latest/) is an unofficial MongoDB backend that supports:
  - Django aggregations
  - (Atomic) updates
  - Embedded objects
  - Map/Reduce and GridFS
  - ORM
  - Admin
  - Authentication
  - Session
  - Caching
- [Installation](https://django-mongodb-engine.readthedocs.io/en/latest/topics/setup.html)
  - pip install git+https://github.com/django-nonrel/django@nonrel-1.5
    - A fork of Django that adds support for non-relational databases
    - Here it showed this error:
    ```cmd
    pip install git+https://github.com/django-nonrel/django@nonrel-1.5
    Collecting git+https://github.com/django-nonrel/django@nonrel-1.5
      Cloning https://github.com/django-nonrel/django (to revision nonrel-1.5) to /tmp/pip-req-build-59sh2rzt
      Running command git clone --filter=blob:none --quiet https://github.com/django-nonrel/django /tmp/pip-req-build-59sh2rzt
      Running command git checkout -b nonrel-1.5 --track origin/nonrel-1.5
      Switched to a new branch 'nonrel-1.5'
      branch 'nonrel-1.5' set up to track 'origin/nonrel-1.5'.
      Resolved https://github.com/django-nonrel/django to commit 36089805701ad6175641b90fcb91423c88d9e002
      Preparing metadata (setup.py) ... done
    Building wheels for collected packages: Django
      Building wheel for Django (setup.py) ... done
      Created wheel for Django: filename=Django-1.5.11-py2.py3-none-any.whl size=8316625 sha256=042cd5caddda5954ccbc1a0a4b1f70f2279fc411a808c947c3fcd3987ced1f61
      Stored in directory: /tmp/pip-ephem-wheel-cache-ri3__skw/wheels/52/76/df/1766942ac5a1eb3acd956f5e5013cddd20c4e0d6c9c07bf2c2
    Successfully built Django
    Installing collected packages: Django
      Attempting uninstall: Django
        Found existing installation: Django 4.0.5
        Uninstalling Django-4.0.5:
          Successfully uninstalled Django-4.0.5
    ERROR: pip's dependency resolver does not currently take into account all the packages that are installed. This behaviour is the source of the following dependency conflicts.
    djangorestframework 3.13.1 requires django>=2.2, but you have django 1.5.11 which is incompatible.
    ```
    So I did `pip3 uninstall django` and then I respond `y` to the next question where ask us to remove some related files. At last I did `pip3 install django`
  - pip install git+https://github.com/django-nonrel/djangotoolbox
    - A bunch of utilities for non-relational Django applications and backends
  - pip install git+https://github.com/django-nonrel/mongodb-engine
  - Now we need to configure database setup:
    - A dictionary containing the settings for **all** databases to be used with Django
    - In these Dictionaries we pass connection parameters to our app.
      - IDK how we should keep our secrets - username/password - safe.
    - Open your `settings.py` and add this:
      ```py
      DATABASES = {
          'default': {
              'ENGINE': 'django_mongodb_engine',
              'NAME': 'anime_die_heart',
          }
      }
      ```
- Failed. If you wanna use python3 this package cannot help you.
  - Read more in this [Stackoverflow Q&A](https://stackoverflow.com/questions/29874628/)

# Models in Django

- [Fields](https://docs.djangoproject.com/en/4.0/ref/models/fields/)
