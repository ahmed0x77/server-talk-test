# ─────────────────────────────────────────────────────────────
# 1) Base image: Python 3.12 slim (Debian Bookworm-based)
# ─────────────────────────────────────────────────────────────
FROM python:3.12-slim

# Prevent interactive prompts during apt
ENV DEBIAN_FRONTEND=noninteractive

# ─────────────────────────────────────────────────────────────
# 2) Install system dependencies
#    • unrar-free  (for extraction)
#    • gcc + build-essential (if any Python packages need compiling)
# ─────────────────────────────────────────────────────────────
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
      unrar-free \
      gcc \
      libffi-dev \
      libpq-dev \
      build-essential \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# ─────────────────────────────────────────────────────────────
# 3) Set working directory
# ─────────────────────────────────────────────────────────────
WORKDIR /app

# ─────────────────────────────────────────────────────────────
# 4) Copy your code (including rar/ folder if you bundled the
#    official RAR binary there)
# ─────────────────────────────────────────────────────────────
COPY . /app

# ─────────────────────────────────────────────────────────────
# 5) Create and activate a Python virtual environment,
#    then install Python dependencies
# ─────────────────────────────────────────────────────────────
RUN python3 -m venv venv
RUN . venv/bin/activate && pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# ─────────────────────────────────────────────────────────────
# 6) Ensure the virtual-env’s bin/ is at the front of PATH
# ─────────────────────────────────────────────────────────────
ENV PATH="/app/venv/bin:$PATH"

# ─────────────────────────────────────────────────────────────
# 7) Expose port (adjust if you bind to a different port)
# ─────────────────────────────────────────────────────────────
EXPOSE 8000

# ─────────────────────────────────────────────────────────────
# 8) Default command: run Gunicorn on main:app
# ─────────────────────────────────────────────────────────────
CMD ["gunicorn", "main:app]
