FROM python:3.12-slim
WORKDIR /bot
RUN pip install --no-cache-dir --upgrade poetry
COPY pyproject.toml poetry.lock ./
RUN poetry install --only main
COPY . .
CMD ["poetry", "run", "python", "main.py"]
