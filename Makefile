DJANGO_EXE=manage.py
IMAGE_NAME=web
CONTAINER_NAME=playlist_generator

all:
	make python_install
	make npm_install
	make build_static
	make make_migrations
	make migrate

start:
	docker run -d --name ${CONTAINER_NAME} -e "PORT=8765" -e "DEBUG=1" --env-file secrets.env -p 8000:8765 ${IMAGE_NAME}:latest

build:
	docker build -t ${IMAGE_NAME}:latest .

release:
	heroku container:push ${IMAGE_NAME}
	heroku container:release -a blooming-castle-70683 ${IMAGE_NAME}

shell:
	@docker exec -ti ${IMAGE_NAME} bash

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
	@python ${DJANGO_EXE} collectstatic

python_install:
	@pip install -r requirements.txt

npm_install:
	@npm ci

npm_lock:
	@npm install

clean_data:
	@python ${DJANGO_EXE} flush
