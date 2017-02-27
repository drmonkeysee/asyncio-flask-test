# Asyncio Flask Test

An application for testing the use of Python 3's asyncio module within Flask to call multiple web apis in a single request. A web server **server.py** calls an api **api.py** either in serial or concurrently and returns timing information.

To develop locally set up a virtual environment and install the local dependencies:

```sh
> python3 -m venv venv
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
> curl -i http://asyncio-server/serial
> curl -i http://asyncio-server/concurrent
> curl -i http://asyncio-server/concurrent?timeout=1.2
```
