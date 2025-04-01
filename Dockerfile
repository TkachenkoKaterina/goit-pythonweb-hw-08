FROM python:3.12-slim

WORKDIR /app

COPY pyproject.toml poetry.lock ./

RUN pip install --upgrade pip && pip install poetry

RUN poetry config virtualenvs.create false \
    && poetry install --only main --no-root

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
