import os
import time
import json
import asyncio
import functools
import threading
import requests
from flask import Flask, request, g


application = Flask(__name__)


api_host = 'http://{}:{}'.format(os.getenv('API_HOST', 'localhost'), os.getenv('API_PORT', 8090))
reqs = [
    api_host + '?sleep=1000',
    api_host + '?sleep=5000',
    api_host + '?sleep=2000',
]


@application.route('/serial')
def serial():
    stats = {}
    start = time.time()
    for i, req in enumerate(reqs):
        now = time.time()
        requests.get(req)
        stats['req' + str(i)] = time.time() - now
    stats['total'] = time.time() - start
    return json.dumps(stats, sort_keys=True, indent=2)


def _call_request(index, *args, **kwargs):
    start = time.time()
    resp = requests.get(*args, **kwargs)
    return time.time() - start


@application.before_request
def init_loop():
    try:
        g.loop = asyncio.get_event_loop()
        print('got event loop for', threading.current_thread().name)
    except RuntimeError:
        g.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(g.loop)
        print('created new event loop for', threading.current_thread().name)


@application.route('/concurrent')
def concurrent():
    req_args = {}
    if 'timeout' in request.args:
        req_args['timeout'] = float(request.args['timeout'])
    stats = {}
    start = time.time()
    futures = [g.loop.run_in_executor(None, functools.partial(_call_request, i, req, **req_args)) for i, req in enumerate(reqs)]
    res = g.loop.run_until_complete(asyncio.gather(*futures, return_exceptions=True))
    for i, result in enumerate(res):
        stats['req' + str(i)] = str(result)
    stats['total'] = time.time() - start
    return json.dumps(stats, sort_keys=True, indent=2)


if __name__ == '__main__':
    application.run(
        debug=True,
        port=9090
    )
