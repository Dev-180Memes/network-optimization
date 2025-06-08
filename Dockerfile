# Use official Python base image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV FLASK_ENV=production

# Install dependencies
RUN apt-get update && \
    apt-get install -y iperf3 net-tools speedtest-cli curl && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Set work directory
WORKDIR /app

# Copy project files
COPY . /app

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose all ports (use 0.0.0.0 binding in app)
EXPOSE 0-65535

# Default command using gunicorn (Render requires this for Flask)
CMD ["python", "app.py"]
