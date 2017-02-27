#!/bin/bash

PROCESSOR_COUNT=$((2 * $(nproc)))
THREAD_COUNT=4
uwsgi --http 0.0.0.0:8090 --master --processes $PROCESSOR_COUNT --threads $THREAD_COUNT --need-app --wsgi-file "$1"
