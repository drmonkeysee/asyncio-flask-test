import time
from flask import Flask, request


application = Flask(__name__)


@application.route('/')
def call():
    sleep = int(request.args['sleep'])
    ms = sleep / 1000.0
    time.sleep(ms)
    return 'Slept for {} milliseconds'.format(ms)


if __name__ == '__main__':
    application.run(
        debug=True,
        port=8090
    )
