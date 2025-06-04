FROM python:3.12-slim

# 1. Install helper packages
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        software-properties-common \
        gnupg \
        ca-certificates && \
    rm -rf /var/lib/apt/lists/*

# 2. Add contrib and non-free components to existing sources and install packages
RUN sed -i \
        -e 's|^\(deb http://deb.debian.org/debian bookworm main\)$|\1 contrib non-free|' \
        -e 's|^\(deb http://deb.debian.org/debian-security/ bookworm-security main\)$|\1 contrib non-free|' \
        -e 's|^\(deb http://deb.debian.org/debian bookworm-updates main\)$|\1 contrib non-free|' \
        /etc/apt/sources.list && \
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
# Activate venv and install requirements. Using /app/venv... for absolute path.
RUN . /app/venv/bin/activate && \
    pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

ENV PATH="/app/venv/bin:$PATH"
EXPOSE 8000
CMD ["gunicorn", "main:app"]
