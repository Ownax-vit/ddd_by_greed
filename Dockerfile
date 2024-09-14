FROM python:3.12.1-slim-bullseye

WORKDIR /app

EXPOSE 8000

RUN apt update -y && \
    apt install -y python3-dev \
    gcc \
    musl-dev

ADD pyproject.toml /app

ENV API_PORT={$API_PORT:8000}

RUN pip install --upgrade pip
RUN pip install poetry

RUN poetry config virtualenvs.create false
RUN poetry install --no-root --no-interaction --no-ansi

COPY /app/ /app/

CMD ["uvicorn", "application.api.main:create_app", "--reload", "--host=0.0.0.0", "--port=8000"]