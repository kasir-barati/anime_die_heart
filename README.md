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
  - `req.FILES`:
    - A **dictionary-like** object containing all uploaded files.
    - Each key in `FILES` is the name from the `<input type="file" name="">`. Each value in `FILES` is an UploadedFile.
    - `FILES` will only contain data if the request method was `POST` and the `<form>` that posted to the request had `enctype="multipart/form-data"`.
      - Otherwise, `FILES` will be a blank dictionary-like object.

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
- Each model's gonna have an `objects` property which is model manager.
  ```py
  ModelName.objects.
  ```

https://github.com/gnulnx/django-mongolog

# Stream video in Django

- What is FFMPEG?
  - A complete, cross-platform solution to record, convert and stream audio and video.
  - Install it: `sudo pacman -S ffmpeg`
    - make sure to install the full version.
- Django uses request and response objects to pass state through the system.
  - Request :arrow_right: Django backend
  - An HttpRequest object - metadata about the request - is created.
  - Loads the appropriate view, passing the HttpRequest as the first argument to the view function.
  - View returns HttpResponse object :arrow_right: Client.
- [`StreamingHttpResponse`](https://docs.djangoproject.com/en/4.0/ref/request-response/#django.http.StreamingHttpResponse)
  - Stream a response from Django to the browser.
  - **Django is designed for short-lived requests**.
  - :warning:Streaming responses will tie a worker process for the entire duration of the response. maybe low performance.
  - Generally speaking, you should perform expensive tasks outside of the request-response cycle, rather than resorting to a streamed response.
- [First Reference](https://github.com/wagtail/wagtail)

# CRUD in Django:

- **Create**
  - No need to instantiate the class
    ```py
    created_move = Movie.objects.create(
        name=sent_file.name,
        description=f"File uploaded at {now}",
        active=True,
        file_name=saved_file_name
    )
    ```
  - Do instantiate the class
    ```py
    created_move = Movie(
        name=sent_file.name,
        description=f"File uploaded at {now}",
        active=True,
        file_name=saved_file_name
    )
    created_move.save()
    ```
- **Read**
  - `ModelName.objects.get()`
  - `Movie.objects.get(name="Shield hero")` amounts to `where name = "Shield hero"`
  - `Movie.objects.get(name="Shield hero", is_active=True)` amounts to `where name = "Shield hero" and is_active = true`
  - `Movie.objects.filter(name__contains="Shield hero")` amounts to `where name like "Shield hero"`
  - **Important notes**
    - With `get()` the query has to match one and only one record.
    - If there are no matching records you will get a `<model>.DoesNotExist` error.
      - Sometimes this is not what we want, we need to get the record or create it. In those scenarios we use `ModelName.objects.get_or_create()`
      - catch error:
        ```py
        try:
            menu_target = Menu.objects.get(name="Dinner")
            # If get() throws an error you need to handle it.
            # You can use either the generic ObjectDoesNotExist or
            # <model>.DoesNotExist which inherits from
            # django.core.exceptions.ObjectDoesNotExist, so you can target multiple
            # DoesNotExist exceptions
        except Menu.DoesNotExist: # or the generic "except ObjectDoesNotExist:"
            menu_target = Menu(name="Dinner")
            menu_target.save()
        ```
    - If there are multiple matching records you will get a `MultipleObjectsReturned` error.
    - `get()` calls hit the database immediately and every time. This means there's no caching on Django's part for identical or multiple calls.
- **Update**
  - You have a reference to the record:
    ```py
    airline = Airline.objects.get(name="Singapore Airlines")
    # Update the name value
    downtown_store.name = "Asia Airlines"
    # Call save() with the update_fields arg and a list of record fields to update selectively
    downtown_store.save(update_fields=['name'])
    # Or you can call save() without any argument and all record fields are updated
    downtown_store.save()
    ```
  - You do not have a reference to record:
    ```py
    Product.objects.filter(id=3).update(stock=F('stock') +100)
    ```
  - You wanted to perform upsert:
    ```py
    values_to_update = {'location':'East Asia'}
    obj_store, created = Airline.objects.update_or_create(
        name='Asia Airline',city='Singapore', defaults=values_to_update)
    ```
    - If there's already an airline record with `name='Asia Airline'` and `city='Singapore'` the record's values in `values_to_update` are updated,
    - If there is no matching airline record a new airline record with `name='Asia Airline'`, `city='Singapore'` along with the values in `values_to_update`.
    - The `update_or_create` method returns an updated or created object, as well as a boolean value to indicate if the record was newly created or not.
    - **Again, if multiple record goes into effect django will raise `MultipleObjectsReturned`**.
  - You can update the instance with database:
    ```py
    user = User.objects.get(id=1)
    user.name = 'Not sure about this name'
    # Update from db again
    user.refresh_from_db()
    # Model record name now reflects value in database again
    user.name
    # Multiple edits
    user.name = 'New store name'
    user.email = 'newemail@coffeehouse.com'
    user.address = 'To be confirmed'
    # Update from db again, but only address field
    # so store name and email remain with local values
    user.refresh_from_db(fields=['address'])
    ```
- **Delete**
  - You have a reference to it:
    ```py
    post = Post.objects.get(slug="Downtown-buddist-musics")
    post.delete()
    ```
  - You do not have a reference to the record:
    ```py
    Agency.objects.filter(id=1).delete()
    ```
    - Return type is what have been deleted and how many.
- [Reference](https://www.webforefront.com/django/singlemodelrecords.html)

# Request & Response:

- `req.methods`:
  - HTTP methods
  - Always uppercase

# Routing in Django

- [Function Based Views](https://www.django-rest-framework.org/api-guide/views/#function-based-views)
  - `path('<int:id>', update_created_movie, name='update-created-movie')`
    - First argument should be a string
    - Use the angle brackets - `<int:id>` - to capture part of the URL and send it as a keyword argument to the view.
      - A converter specification: `<int:id>`
    - Second argument is a view function or the result of `as_view()` for class-based views.
    - `name` argument is useful when:
      - `return HttpResponseRedirect(reverse('movies-list'))`
        - Here we also can pass arguments.
    - We can also pass additional arguments to the view too.
