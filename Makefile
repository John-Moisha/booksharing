SHELL := /bin/bash

manage_py := python APP/manage.py

runenv:
	source env/bin/activate

runserver:
	$(manage_py) runserver 0:8000

run_celery:
	celery -A booksharing worker -l info


makemigrations:
	$(manage_py) makemigrations

migrate:
	$(manage_py) migrate

shell_plus:
	$(manage_py) shell_plus --print-sql


flake8:
	flake8 ./APP