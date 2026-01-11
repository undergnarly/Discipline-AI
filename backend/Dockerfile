FROM python:3.11-slim

WORKDIR /app

# Install poetry
RUN pip install poetry

# Copy project file and generate lock file
COPY pyproject.toml /app/

# Install dependencies
RUN poetry config virtualenvs.create false && poetry lock --no-update && poetry install --no-root --no-dev

# Copy the rest of the application
COPY . /app

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"] 