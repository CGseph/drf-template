# Makefile utilities for docker-compose images

COMPOSE_FILE ?= docker-compose.yaml
DOCKER ?= docker

.PHONY: help build-images build-images-no-cache run-images clean-images run-auth-service migrate-auth-service makemigrations-auth-service shell-auth-service test test-unit test-integration test-coverage test-watch

help:
	@echo "Usage: make <target>"
	@echo "Targets:"
	@echo "  help - Show this help message"
	@echo "  build-images - Build the project images"
	@echo "  build-images-no-cache - Build images without cache"
	@echo "  run-images - Run the project using docker"
	@echo "  clean-images - Stop and remove containers/volumes"
	@echo "  run-auth-service - Run auth service locally"
	@echo "  migrate-auth-service - Run database migrations"
	@echo "  makemigrations-auth-service - Create new migrations"
	@echo "  shell-auth-service - Open Django shell"

build-images:
	docker-compose build

build-images-no-cache:
	docker-compose build --no-cache --pull

run-images:
	docker-compose up

clean-images:
	docker-compose down -v

run-auth-service:
	cd auth-service && poetry run python src/manage.py runserver 0.0.0.0:8000

migrate-auth-service:
	cd auth-service && poetry run python src/manage.py migrate

makemigrations-auth-service:
	cd auth-service && poetry run python src/manage.py makemigrations

shell-auth-service:
	cd auth-service && poetry run python src/manage.py shell
