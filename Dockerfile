FROM python:3.12-slim

# 1. Install helper packages
RUN apt-get update && \
    apt-get install -y software-properties-common gnupg && \
    rm -rf /var/lib/apt/lists/*

# 2. Add the non-free repo
RUN echo "deb http://deb.debian.org/debian bookworm main contrib non-free" \
    > /etc/apt/sources.list.d/non-free.list && \
    apt-get update && \
    apt-get install -y rar unrar wget curl && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY . /app

RUN python3 -m venv venv
RUN . venv/bin/activate && pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

ENV PATH="/app/venv/bin:$PATH"
EXPOSE 8000
CMD ["gunicorn", "main:app"]
