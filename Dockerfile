FROM python:3.12-slim


RUN apt-get update && \
    apt-get install -y \
    rar \
    unrar \
    wget \
    curl \
    && rm -rf /var/lib/apt/lists/*

    
WORKDIR /app

# Copy project files
COPY . /app

# Create a virtual environment
RUN python3 -m venv venv

# Activate virtual environment and install dependencies
RUN . venv/bin/activate && pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Use the virtual environment for PATH
ENV PATH="/app/venv/bin:$PATH"

# Expose the port your app runs on (change if needed)
EXPOSE 8000

# Run the app with Gunicorn
CMD ["gunicorn", "main:app"]
