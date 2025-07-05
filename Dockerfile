# Use a Python base image
FROM python:3.9-slim-buster

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file and install dependencies
COPY pyproject.toml poetry.lock ./
RUN pip install poetry
RUN poetry install --no-root

# Copy the rest of the application code
COPY . .

# Expose the port the app will run on
EXPOSE 8000

# Command to run the application
CMD ["poetry", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
