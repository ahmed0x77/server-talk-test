RUN apt-get update && \
    apt-get install -y \
    rar \
    unrar \
    wget \
    curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY . .
