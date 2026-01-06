# Use Python 3.10 for broad compatibility
FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . .

# Create directory for local database
RUN mkdir -p instance data/docs

# Expose port
EXPOSE 5000

# Run with Gunicorn for production-like behavior (optional, using python app.py for simplicity per prompt)
CMD ["python", "app.py"]
