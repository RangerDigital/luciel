FROM python:3.10

RUN pip install poetry

COPY poetry.lock pyproject.toml  /
RUN poetry config virtualenvs.create false && poetry install --no-dev --no-interaction --no-ansi

COPY ./ /

EXPOSE 8080
CMD uvicorn main:app --host 0.0.0.0 --port 8080