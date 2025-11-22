PYTHON=python3
ENV_FILE?=infra/.env.example

.PHONY: dev test-unit test-integration lint seed

dev:
	docker compose -f infra/docker-compose.yml --env-file $(ENV_FILE) up --build

test-unit:
	$(PYTHON) -m pytest tests/unit

test-integration:
	$(PYTHON) -m pytest tests/integration

lint:
	ruff check .
	black --check .
	mypy .

seed:
	$(PYTHON) infra/seed.py
