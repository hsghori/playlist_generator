build:
	sass static/scss/base.scss static/css/main.css
	browserify static/js/main.js > static/js/bundle.js

start:
	python manage.py runserver
