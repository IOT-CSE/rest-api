#!/usr/bin/env bash

# fresh database
dropdb postgres
createdb postgres

# set flask configurations and run
export FLASK_APP=main.py
flask run
