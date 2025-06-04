FROM python:3.12-slim

# 2. Add contrib and non-free components via a new, explicitly signed sources list file.
# This assumes the standard Debian archive keyring is available at /usr/share/keyrings/debian-archive-keyring.gpg.
RUN echo "deb [signed-by=/usr/share/keyrings/debian-archive-keyring.gpg] http://deb.debian.org/debian/ bookworm contrib non-free" > /etc/apt/sources.list.d/contrib-non-free.list && \
    echo "deb [signed-by=/usr/share/keyrings/debian-archive-keyring.gpg] http://deb.debian.org/debian/ bookworm-updates contrib non-free" >> /etc/apt/sources.list.d/contrib-non-free.list && \
    echo "deb [signed-by=/usr/share/keyrings/debian-archive-keyring.gpg] http://security.debian.org/debian-security/ bookworm-security contrib non-free" >> /etc/apt/sources.list.d/contrib-non-free.list && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
        rar \
        unrar \
        wget \
        curl && \
    rm -rf /var/lib/apt/lists/* && \
    apt-get clean



# Set working directory
WORKDIR /app

# Copy project files
COPY . /app

# Create a virtual environment
RUN python3 -m venv venv

# Activate venv using the absolute path for clarity
RUN . /app/venv/bin/activate && \
    pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Use the virtual environment for PATH
ENV PATH="/app/venv/bin:$PATH"

# Expose the port your app runs on (change if needed)
EXPOSE 8000

# Run the app with Gunicorn
CMD ["gunicorn", "main:app"]






