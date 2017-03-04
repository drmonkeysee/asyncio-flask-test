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


@application.before_request
def init_loop():
    try:
        g.loop = asyncio.get_event_loop()
        print('got event loop for', threading.current_thread().name)
    except RuntimeError:
        g.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(g.loop)
        print('created new event loop for', threading.current_thread().name)


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


@application.route('/gather')
def gather():
    return _concurrent(_gather_requests)


@application.route('/async')
def async():
    return _concurrent(_invoke_requests)


def _concurrent(async_op):
    stats = {}
    start = time.time()
    res = g.loop.run_until_complete(async_op())
    for i, result in enumerate(res):
        stats['req' + str(i)] = str(result)
    stats['total'] = time.time() - start
    return json.dumps(stats, sort_keys=True, indent=2)


def _gather_requests():
    co_requests = _wrap_requests()
    return asyncio.gather(*co_requests, return_exceptions=True)


async def _invoke_requests():
    co_requests = _wrap_requests()
    results = []
    for i, c in enumerate(co_requests):
        results.insert(i, await c)
    return results


def _wrap_requests():
    req_args = {}
    if 'timeout' in request.args:
        req_args['timeout'] = float(request.args['timeout'])
    return [g.loop.run_in_executor(None, functools.partial(_call_request, req, **req_args)) for req in reqs]


def _call_request(*args, **kwargs):
    start = time.time()
    resp = requests.get(*args, **kwargs)
    return time.time() - start


if __name__ == '__main__':
    application.run(
        debug=True,
        port=9090
    )
