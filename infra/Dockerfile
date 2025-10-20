FROM python:3.11-slim
WORKDIR /app
# Install curl for health checks
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
COPY cache_firestore.py secrets_config.py proxy.py /app/
EXPOSE 8080
# Use 4 workers for better concurrency (adjust based on CPU cores)
# Each worker can handle multiple concurrent requests with async
CMD ["uvicorn","proxy:app","--host","0.0.0.0","--port","8080","--workers","4"]
