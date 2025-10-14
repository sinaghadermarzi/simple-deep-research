FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
COPY cache_firestore.py secrets_config.py proxy.py /app/
EXPOSE 8080
CMD ["uvicorn","proxy:app","--host","0.0.0.0","--port","8080"]
