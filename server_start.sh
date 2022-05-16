#!/bin/bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install django
python -m pip install psycopg2-binary
python -m pip install django_extensions
python -m pip install djangorestframework
python3 manage.py runserver
