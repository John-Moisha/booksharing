SHELL := /bin/bash

manage_py := python APP/manage.py

runenv:
    env/bin/activate

runserver:
	$(manage_py) runserver 0:8000

makemigrations:
	$(manage_py) makemigrations

migrate:
	$(manage_py) migrate

shell_plus:
	$(manage_py) shell_plus --print-sql


flake8:
	flake8 ./APP