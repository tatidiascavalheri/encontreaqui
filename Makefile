dev:
	docker compose up --build

migrate:
	docker compose exec api python scripts/run_migration.py

seed:
	docker compose exec api python scripts/seed.py

test:
	docker compose exec api pytest -q
