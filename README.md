# Upload file in MongoDB

- GridFS
  - A specification for storing/retrieving files that exceed the BSON-document size limit of 16 MB.
  - Divides the file into parts, or chunks
  - GridFS uses two collections to store files.
    - One collection stores the file chunks
    - The other stores file metadata.
  - Reassemble the chunks as needed when we query the file.
    - You can perform range queries on files stored through GridFS.
    - You can also access information from arbitrary sections of files, such as to "skip" to the middle of a video or audio file.
  - Useful for:
    - Files that exceed 16 MB
    - Storing any files for which you want access without having to load the entire file into memory.
  - [When to use GridFS](https://compose.com/articles/gridfs-and-mongodb-pros-and-cons/)
  - Use GridFS if
    - Filesystem limitation on the number of files in a directory to store limitlessly
    - Access information from portions of large files without having to load whole files into memory
    - Keep your files and metadata automatically synced and deployed across a number of systems and facilities, you can use GridFS. When using geographically distributed replica sets, MongoDB can distribute files and their metadata automatically to a number of mongod instances and facilities.
  - Do not use GridFS if:
    - The content of the entire file should be updated atomically.
    - If your files are all smaller than the 16 MB BSON Document Size limit, consider storing each file in a single document instead of using GridFS.
  - I install djongo to work with MongoDB in django.
    - First I forced to change pymongo version.
      - `pip install pymongo==3.12.3`
        - We do not need to uninstall the previous one. Just execute the command.
      - Read more in [this stackoverflow Q&A](https://stackoverflow.com/a/70737146/8784518)

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

# `settings.py`

- `ALLOWED_HOSTS`
  - A list of strings representing the host/domain names that this Django site can serve.
  - But it is **NOT** translatable to CORS.
    - Read more in this [Stackoverflow Q&A](https://stackoverflow.com/a/47229671/8784518)
- `DATABASES`
  - A dictionary containing the settings for all databases to be used with Django.
  - Must configure a default database
  - Valid values for `ENGINE`:
    - `'django.db.backends.sqlite3'`
    - `'django.db.backends.postgresql'`
    - `'django.db.backends.mysql'`
    - `'django.db.backends.oracle'`
  - [**Multiple databases**](https://docs.djangoproject.com/en/4.0/topics/db/multi-db/)
    - Tell Django about the database servers you’ll be using.
      - We've done it in `settings.py` in `DATABASES` section.
    - Aliases are used to refer to a specific database throughout Django application
      - You can choose any name.
      - The alias `default` has special significance.
        - Django uses the database with the alias of `default` when no other database has been selected (I guess it means `.using('alias')`).
        - If the concept of a `default` database doesn’t make sense in the context of your project, you need to be careful to always specify the database that you want to use.
    - `python3 manage.py migrate --database=mongodb`
      - :warning:**Wrong usage**:exclamation: `python3 manage.py makemigrations --database=mongodb`

# Error: Authentication failed.

- What I've tried to find the problem:
  - Googling: I reached [this Stackoverflow Q&A](https://stackoverflow.com/questions/60394290) and followed this steps:
    - Clean state
      - `docker volume prune`
      - `docker-compose down --remove-orphans`
      - Then exec into container: `docker exec -it anime_die_heart_mongodb bash`
        - `mongo -u python -p student`
        - `mongo -u python -p student --authenticationDatabase anime_videos`
        - `mongo -u python -p student --authenticationDatabase admin`
      - **FAILED**
        - Passed env:
          - `MONGODB_USERNAME=docker`
          - `MONGODB_PASSWORD=student`
          - `MONGODB_DATABASE=learning`
    - Used both different way to pass env to the container:
      - `env_file`
      - `environment`
      - Then exec into container: `docker exec -it anime_die_heart_mongodb bash`
        - `mongo -u python -p student`
        - `mongo -u python -p student --authenticationDatabase anime_videos`
      - **FAILED**
        - Passed env:
          - `MONGODB_USERNAME=docker`
          - `MONGODB_PASSWORD=student`
          - `MONGODB_DATABASE=learning`
    - Use different env set:
      - First set:
        - `MONGO_INITDB_ROOT_USERNAME=python`
        - `MONGO_INITDB_ROOT_PASSWORD=student`
        - `MONGO_INITDB_DATABASE=anime_videos`
      - Then exec into container: `docker exec -it anime_die_heart_mongodb bash`
        - `mongo -u python -p student`
        - `mongo -u python -p student --authenticationDatabase anime_videos`
      - **FAILED**
      - Second set:
        - `MONGODB_USERNAME=docker`
        - `MONGODB_PASSWORD=student`
        - `MONGODB_DATABASE=learning`
      - Then exec into container: `docker exec -it anime_die_heart_mongodb bash`
        - `mongo -u python -p student`
        - `mongo -u python -p student --authenticationDatabase anime_videos`
        - `mongo -u python -p student --authenticationDatabase admin`
      - **FAILED**
    - Finally I put these envs in `.mongodb.env` and remove `environment` instruction from the compose file.
      - `MONGO_INITDB_ROOT_USERNAME=python`
      - `MONGO_INITDB_ROOT_PASSWORD=student`
      - `MONGO_INITDB_DATABASE=anime_videos`
      - Then exec into container: `docker exec -it anime_die_heart_mongodb bash`
      - `mongo -u python -p student --authenticationDatabase admin`
      - **Worked**

# Start app in dev env:

1. `cp .mongodb.env.example .mongodb.env`
2. `docker-compose up -d`
3. `virtualenv venv`
4. `source ./venv/bin/activate`
5. `pip3 install -r ./requirements.txt`
6. `python3 manage.py migrate`
7. `python3 manage.py runserver`

- To deactivate virtual env: `deactivate`
- To remove docker container:
  - `docker-compose down --remove-orphans`
  - `docker volume rm anime_die_heart_mongodb_volume`
