update:
	git pull https://github.com/Mikita-Arsi/worki-service.git master

kill:
	docker compose kill
down:
	docker compose down
build:
	docker compose --env-file .env build
up:
	docker compose up

run: kill down build up

all: update run