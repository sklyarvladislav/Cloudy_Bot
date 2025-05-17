PORT:=3000
PYTHONPATH=./
RUN_PYTHON=uv run

compose:
	docker compose up -d

down:
	docker compose down

makemigrations:
	${RUN_PYTHON} alembic revision --autogenerate -m "$(MSG)"

migrate:
	${RUN_PYTHON} alembic -x data=true upgrade head

downgrade:
	${RUN_PYTHON} alembic downgrade -1

lint:
	${RUN_PYTHON} pre-commit run --all-files
