FROM python:3
MAINTAINER Brandon Stansbury <brandonrstansbury@gmail.com>

ENV APP_DIR=/opt/drmonkeysee/async-test \
	APP=api.py

WORKDIR $APP_DIR

RUN apt-get update \
    && apt-get install -y --no-install-recommends build-essential \
    && pip install Flask uwsgi requests \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get purge -y build-essential \
    && apt-get autoremove -y

COPY . $APP_DIR

RUN chmod u+x launch.sh

EXPOSE 8000

CMD ./launch.sh "$APP"
