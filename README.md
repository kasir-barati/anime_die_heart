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
