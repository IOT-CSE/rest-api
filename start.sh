#!/usr/bin/env bash

# fresh database
dropdb test
createdb test


# set flask configurations and run
export FLASK_APP=main.py
flask run
