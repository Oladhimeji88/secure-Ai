SHELL := /bin/sh

up:
	docker compose up --build

down:
	docker compose down -v

seed:
	docker compose exec api python /scripts/seed.py

test:
	docker compose exec api pytest -q
	docker compose exec web npm run typecheck
	docker compose exec web npm run lint

lint:
	docker compose exec api python -m compileall app
	docker compose exec web npm run lint
