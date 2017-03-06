# Asyncio Flask Test

This is a test application illustrating how to utilize asyncio with a Flask application to call multiple HTTP endpoints within a single request. A web application **server.py** calls a "3rd-party" service **api.py** either in serial or concurrently and returns timing information.

**server.py** provides a few endpoints to test different strategies for making multiple HTTP calls. **api.py** simulates doing work by accepting a sleep parameter and waiting for that number of milliseconds before returning. By default **server.py** will call **api.py** with delays of 1, 5, and 2 seconds.

To develop locally set up a virtual environment and install the local dependencies:

```sh
> python3 -m venv venv
> source venv/bin/activate
> pip install -r requirements.txt
```

Then run each web app:
```sh
> python3 api.py
> python3 server.py
```

However when Flask is self-hosted it only handles one request at a time so everything runs serially anyway. Hence this test hosts both web applications in docker containers to take advantage of uWSGI's multi-threading capability.

To launch the app run:

```sh
> docker-compose up
```

And test it by `curl`ing to **server.py**

```sh
> curl -i http://localhost:9090/serial
> curl -i http://localhost:9090/serial?timeout=1.2
> curl -i http://localhost:9090/gather
> curl -i http://localhost:9090/gather?timeout=1.2
> curl -i http://localhost:9090/async
> curl -i http://localhost:9090/async?timeout=1.2
```

`serial` will invoke all api requests in order, `gather` will invoke api requests using `asyncio.gather()`, and `async` will invoke api requests using the `async`/`await` pattern.

To load test **server.py** fire up the locustfile as:

```sh
>locust --host=http://localhost:9090
```

Go to `http://localhost:8089` in a browser and kick off the load test there.
