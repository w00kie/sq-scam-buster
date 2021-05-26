.PHONY: requirements migrate run celeryworker

requirements:
	pip-compile
	pip-sync

migrate:
	python manage.py makemigrations
	python manage.py migrate

run:
	python manage.py runsslserver --certificate cert.pem --key key.pem

cert.pem:
	mkcert -cert-file cert.pem -key-file key.pem 0.0.0.0 localhost 127.0.0.1 ::1

celeryworker:
	celery -A sqscambuster worker -l INFO