DJANGO_EXE=generator/manage.py

all:
	make python_install
	make npm_install
	make build_static
	make make_migrations
	make migrate

start:
	@docker-compose up

build:
	@docker-compose build

shell:
	@docker exec -ti playlist_generator bash

make start_server:
	@python ${DJANGO_EXE} runserver 0.0.0.0:8000

migrate:
	@python ${DJANGO_EXE} migrate

make_migrations:
	@python ${DJANGO_EXE} makemigrations

watch_js:
	@npm run watch:js

watch_css:
	@npm run watch:css

build_static:
	@npm run build:js
	@npm run build:css

python_install:
	@pip install -r requirements.txt

npm_install:
	@npm ci

npm_lock:
	@npm install

clean_data:
	@python ${DJANGO_EXE} flush
