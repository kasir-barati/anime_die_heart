# Celery Quick start

```py
from celery import Celery

app = Celery('tasks', broker='pyamqp://guest@localhost//')

@app.task
def add(x, y):
    return x + y
```

- ### First argument to `Celery`:
  - The name of the current module.
  - This is only needed so that names can be automatically generated when the tasks are defined in the `__main__` module.
    - TBH I do not understand this part
- ### Second argument to `Celery`:
  - The broker keyword argument, specifying the URL of the message broker you want to use.
  - Here we are using RabbitMQ (**also the default option**). -
  - For RabbitMQ use `amqp://localhost`
  - For Redis use `redis://localhost`
- You defined a single task, called `add`, returning the sum of two numbers.
- # Running the Celery worker server
  - You can now run the worker by executing our program with the worker argument:
  - `celery -A tasks worker --loglevel=INFO`
    - `celery worker --help`
    - `celery --help`
  - In production you’ll wanna run the worker in the background as a daemon.
    - Use provided tools by your platform, or `supervisord`
- # Call our task
  - `delay()`
    - A handy shortcut to the `apply_async()` method that gives greater control of the task execution
      ```cmd
      $ python
      >>> from tasks import add
      >>> add.delay(4, 4)
      ```
  - Task has now been processed by the worker you started earlier.
  - It returns an `AsyncResult` instance.
    - Use it to:
      - Check the state of the task
      - Wait for the task to finish
      - Get its return value
      - Get the exception and traceback just in failure case
    - Results are not enabled by default.
      - To do:
        - Remote procedure calls
        - Keep track of task results in a database
      - You'll need to configure Celery to use a result backend.
        - Store or send the states somewhere.
        - There are several built-in result backends to choose from:
          - SQLAlchemy
          - Django ORM
          - MongoDB
          - Memcached
          - Redis
          - RPC (RabbitMQ/AMQP)
          - or your own backend.
      - [Learn more](https://docs.celeryq.dev/en/latest/userguide/tasks.html#task-result-backends)
    - RPC result backend:
      - Sends states back as transient messages.
- ### Third arguments to `Celery`:
  - The Backend
    ```py
    # In case you're using RabbitMQ as message broker
    app = Celery('tasks', broker='pyamqp://', backend='rpc://',)
    # In case you're using Redis as message broker
    app = Celery('tasks', backend='redis://localhost', broker='pyamqp://')
    ```
  - `result.ready()`
    - `ready()` returns whether the task has finished processing or not
      ```cmd
      $ python
      >>> from tasks import add
      >>> result = add.delay(4, 4)
      >>> result.ready()
      ```
  - `result.get(timeout=1)`
    - Get the result.
    - Based on my observation this code will turns async operation into a sync operation which I assume we do not want
    - `result.get(propagate=False)`
      - Calling `.get` twice raise an exception.
      - We change it via this argument
  - `result.traceback`
    - To get the error stack
  - ## :warning:**Backends use resources to store and transmit results**:warning:
    - Release resources by calling `get()` or `forget()` on **EVERY** `AsyncResult` instance returned after calling a task

# Configuration

- Like a consumer appliance, doesn’t need much configuration to operate.
- It has an input and an output.
  - The input must be connected to a broker
  - The output can be optionally connected to a result backend.
  - However, if you look closely at the back, there’s a lid revealing loads of sliders, dials, and buttons: this is the configuration.
    - ## **IDK what does this mean**
- Default configuration should be good enough for most use cases
- Setup conf:
  - Directly on the app
  - Use a dedicated configuration module.
