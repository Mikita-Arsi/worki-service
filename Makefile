update:
	git pull git@github.com:Mikita-Arsi/ai-tgbot.git main

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