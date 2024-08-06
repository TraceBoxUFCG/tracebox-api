install: install_python install_project install_precommit

install_python:
	pyenv install 3.12.4 --skip-existing
	pyenv local 3.12.4

install_project:
	poetry env use 3.12.4
	poetry install

start:
	poetry run uvicorn app.main:app --reload --reload-dir app

install_precommit:
	poetry run pre-commit install --install-hooks

docker-alembic-revision: ## Bootstrap an alembic migration file based on source code changes with the given message. Usage: "make docker-alembic-revision <message>" Example: "make docker-alembic-revision message="add_id_location_column_to_orders""
	docker compose run server alembic revision --autogenerate -m "${message}"

docker-upgrade-head:
	docker compose run server alembic upgrade head

docker-downgrade:
	docker compose run server alembic downgrade ${q}

test:
	poetry run pytest $(file)

lint:
	poetry run pre-commit run --all-files
