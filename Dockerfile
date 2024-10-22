FROM python:3.12-alpine

ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY pyproject.toml .
RUN pip install poetry
RUN poetry config virtualenvs.create false \
  && poetry install --no-interaction --no-ansi

COPY ./searcher /app

ENTRYPOINT python playground.py