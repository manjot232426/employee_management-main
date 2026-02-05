# Dockerfile for FastAPI + MySQL Employee Management Backend
FROM python:3.11-slim

# Prevent interactive tzdata, speed up pip
ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Set work directory
WORKDIR /app

# Install system dependencies required by mysqlclient
RUN apt-get update && apt-get install -y --no-install-recommends \
    pkg-config \
    default-libmysqlclient-dev \
    libmariadb-dev \
    build-essential \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first to leverage Docker layer caching
COPY requirements.txt .

# Upgrade pip/setuptools/wheel then install dependencies
RUN python -m pip install --upgrade pip setuptools wheel && \
    pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

# Expose FastAPI port
EXPOSE 8000

# Start FastAPI app via Uvicorn
# IMPORTANT: Make sure "main:app" matches your actual file and app variable
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]