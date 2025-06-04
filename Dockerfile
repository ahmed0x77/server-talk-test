# ─────────────────────────────────────────────────────────────
# 1) Base image: Ubuntu 24.04 LTS (glibc ≥ 2.40)
# ─────────────────────────────────────────────────────────────
FROM ubuntu:24.04

# Avoid interactive prompts during apt install
ENV DEBIAN_FRONTEND=noninteractive

# ─────────────────────────────────────────────────────────────
# 2) Install system dependencies:
#    • python3 / pip
#    • rar & unrar (if you still need binary compression)
# ─────────────────────────────────────────────────────────────
RUN apt-get update \
 && apt-get install -y \
      python3 \
      python3-pip \
      rar       \
      unrar-free \
 && rm -rf /var/lib/apt/lists/*

# ─────────────────────────────────────────────────────────────
# 3) Create application directory
# ─────────────────────────────────────────────────────────────
WORKDIR /app

# ─────────────────────────────────────────────────────────────
# 4) Copy your code (including rar/ if you still bundle it)
# ─────────────────────────────────────────────────────────────
COPY . /app

# ─────────────────────────────────────────────────────────────
# 5) Install Python requirements (including gunicorn)
# ─────────────────────────────────────────────────────────────
RUN pip3 install --no-cache-dir -r requirements.txt

# ─────────────────────────────────────────────────────────────
# 6) Expose port (optional; for documentation)
# ─────────────────────────────────────────────────────────────
#   (adjust if you bind to a different port)
EXPOSE 8000

# ─────────────────────────────────────────────────────────────
# 7) Default command: use Gunicorn to run `main:app`
#    (bind to 0.0.0.0:8000 by default)
# ─────────────────────────────────────────────────────────────
CMD ["gunicorn", "main:app"]
