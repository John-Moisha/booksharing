SHELL := /bin/bash

manage_py := docker exec -it backend python3 APP/manage.py

runenv:
	source env/bin/activate

runserver:
	$(manage_py) runserver 0:8000

collectstatic:
	$(manage_py) collectstatic --noinput && \
	docker cp backend:/tmp/static /tmp/static && \
	docker cp /tmp/static web:/etc/nginx/static

run_celery:
	celery -A booksharing worker -l info

makemigrations:
	$(manage_py) makemigrations

pytest:
	pytest APP/ --cov=app --cov-report html

flake8:
	flake8 ./APP

gunicorn:
	gunicorn booksharing.wsgi -b:8081 --workers=4 --chdir=/home/clz/PycharmProjects/booksharing/APP --max-requests=10000

uwsgi:
	 uwsgi --http :8001 --chdir=/home/clz/PycharmProjects/booksharing/APP --module booksharing.wsgi --master --processes 4 --threads 2

build-dev:
	docker-compose -f docker-compose.yml -f docker-compose.dev.yml up -d --build

build: build-dev collectstatic

build_down:
	docker-compose down