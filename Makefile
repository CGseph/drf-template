# Makefile utilities for docker-compose images

COMPOSE_FILE ?= docker-compose.yml
DOCKER ?= docker

.PHONY: help build-images build-images-no-cache run-images clean-images

help:
	@echo "Usage: make <target>"
	@echo "Targets:"
	@echo "  help - Show this help message"
	@echo "  build-images - Build the project images"
	@echo "  run-images - Run the project using docker"

build-images:
	docker-compose build

build-images-no-cache:
	docker-compose build --no-cache --pull

run-images:
	docker-compose up

clean-images:
	docker-compose down -v

.PHONY: run-auth-service migrate-auth-service
run-auth-service:
	cd auth-service && poetry run python src/manage.py runserver 0.0.0.0:8000

migrate-auth-service:
	cd auth-service && poetry run python src/manage.py makemigrations && poetry run python src/manage.py migrate
