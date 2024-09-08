ARG VERSION=3.11

FROM python:${VERSION}-slim as base
WORKDIR /code
RUN pip install --no-cache-dir --upgrade poetry
COPY pyproject.toml poetry.lock ./


FROM base AS production
RUN poetry install --only main
COPY app app
CMD poetry run uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}


# FROM base AS test
# RUN poetry install
# COPY app app
# COPY tests tests
# CMD ["poetry", "run", "pytest"]
