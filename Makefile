SHELL := /bin/bash

manage_py := python APP/manage.py

runenv:
	source env/bin/activate

runserver:
	$(manage_py) runserver 127.0.0.1:8001

run_celery:
	celery -A booksharing worker -l info


makemigrations:
	$(manage_py) makemigrations

migrate:
	$(manage_py) migrate

shell_plus:
	$(manage_py) shell


flake8:
	flake8 ./APP