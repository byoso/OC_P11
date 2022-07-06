#! /bin/bash

# simple shortcut that runs the flask app within its environment
# this should not work with windows

source .env/bin/activate
export FLASK_APP=src/server.py
export FLASK_DEBUG=1
flask run
