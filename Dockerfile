# Use uma imagem base oficial do Python
FROM python:3.12.4-slim-bullseye AS BASE

ENV PYTHONUNBUFFERED=1 \
  PYTHONDONTWRITEBYTECODE=1 \
  PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  POETRY_HOME="/opt/poetry" \
  POETRY_VIRTUALENVS_IN_PROJECT=true \
  POETRY_VERSION="1.8.2" \
  POETRY_NO_INTERACTION=1 \
  PYSETUP_PATH="/opt/service" \
  VENV_PATH="/opt/service/.venv"

ENV PATH="$POETRY_HOME/bin:$VENV_PATH/bin:$PATH"

## Build Image
# Builds our project :)
FROM base as builder-image

COPY ./scripts $PYSETUP_PATH/scripts
RUN chmod +x $PYSETUP_PATH/scripts/install-build-packages.sh
RUN $PYSETUP_PATH/scripts/install-build-packages.sh

SHELL ["/bin/bash", "-o", "pipefail", "-c"]
RUN curl -sSL https://install.python-poetry.org  | python -

WORKDIR $PYSETUP_PATH
COPY ./app $PYSETUP_PATH/app
COPY poetry.lock pyproject.toml $PYSETUP_PATH/

COPY alembic.ini  $PYSETUP_PATH/alembic.ini
COPY pre_start.py  $PYSETUP_PATH/pre_start.py
COPY ./migrations $PYSETUP_PATH/migrations
RUN chmod +x $PYSETUP_PATH/scripts/pre-start.sh

ARG POETRY_OPTIONS
RUN poetry install $POETRY_OPTIONS

## Runtine Image
# Copy the builded files to a fresh image
FROM base as runtime-image
COPY --from=builder-image $PYSETUP_PATH $PYSETUP_PATH
COPY ./tests/ $PYSETUP_PATH/tests
WORKDIR $PYSETUP_PATH

RUN useradd user -u 1000
USER user
EXPOSE 8000
CMD ["/bin/bash", "/opt/service/scripts/pre-start.sh"]
