FROM python:3.12-slim

# Set environment variables to avoid prompts during package installation
ENV DEBIAN_FRONTEND=noninteractive

# Set working directory
WORKDIR /app

# Install system dependencies, including unrar
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    unrar \
    gcc \
    libffi-dev \
    libpq-dev \
    build-essential \
    && apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Copy project files
COPY . /app

# Create a virtual environment
RUN python3 -m venv venv

# Activate virtual environment and install dependencies
RUN . venv/bin/activate && pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Use the virtual environment for PATH
ENV PATH="/app/venv/bin:$PATH"

# Expose the port your app runs on
EXPOSE 8000

# Run the app with Gunicorn
CMD ["gunicorn", "main:app"]
