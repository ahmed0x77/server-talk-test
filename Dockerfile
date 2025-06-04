# ─────────────────────────────────────────────────────────────
# 1) Base image: Ubuntu 24.04 LTS (glibc ≥ 2.40)
# ─────────────────────────────────────────────────────────────
FROM ubuntu:24.04

# Avoid prompts during apt install
ENV DEBIAN_FRONTEND=noninteractive

# ─────────────────────────────────────────────────────────────
# 2) Install system dependencies:
#    • python3 / pip
#    • rar & unrar (Debian packages, glibc-compatible)
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
# 4) Copy your code (including any 'rar/' folder if you still want it)
# ─────────────────────────────────────────────────────────────
COPY . /app

# ─────────────────────────────────────────────────────────────
# 5) Install Python requirements
# ─────────────────────────────────────────────────────────────
#    (adjust this if your requirements file is named differently)
RUN pip3 install --no-cache-dir -r requirements.txt

# ─────────────────────────────────────────────────────────────
# 6) Default command: run your script
#    (replace "main.py" if your entrypoint is named differently)
# ─────────────────────────────────────────────────────────────
CMD ["python3", "main.py"]
