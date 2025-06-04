FROM python:3.12-slim

# 1. Install helper packages and ensure essential keyring utilities are present
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        software-properties-common \
        gnupg \
        ca-certificates \
        apt-transport-https && \
    rm -rf /var/lib/apt/lists/*

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

WORKDIR /app
COPY . /app

RUN python3 -m venv venv
# Activate venv using the absolute path for clarity
RUN . /app/venv/bin/activate && \
    pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

ENV PATH="/app/venv/bin:$PATH"
EXPOSE 8000
CMD ["gunicorn", "main:app"]
