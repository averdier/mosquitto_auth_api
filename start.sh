#!/bin/sh

python create_database.py
uwsgi --ini app.ini