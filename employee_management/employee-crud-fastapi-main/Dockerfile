# Dockerfile for FastAPI + MySQL Employee Management Backend
FROM python:3.11-slim

# Prevent interactive tzdata etc.
ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Set work directory
WORKDIR /app

# Install system dependencies required by mysqlclient
# - pkg-config: for detecting mysqlclient
# - default-libmysqlclient-dev: MySQL client headers (use libmariadb-dev if you prefer)
# - build-essential: compilers, linkers, etc.
# - python3-dev: Python headers for building C extensions
RUN apt-get update && apt-get install -y --no-install-recommends \
    pkg-config \
    default-libmysqlclient-dev \
    build-essential \
    python3-dev \
  && rm -rf /var/lib/apt/lists/*

# Copy requirements first to leverage Docker layer caching
COPY requirements.txt ./

# Consider upgrading pip/wheel/setuptools for better wheel support on 3.13
RUN python -m pip install --upgrade pip setuptools wheel \
 && pip install --no-cache-dir -r requirements.txt

# Copy the rest of the app
COPY . .

# Expose port for FastAPI
EXPOSE 8000

# Start FastAPI app with uvicorn (adjust module if needed)
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]