FROM python:3.12-slim
WORKDIR /app
COPY requirements-server.txt .
RUN pip install --no-cache-dir -r requirements-server.txt && useradd -m appuser
COPY --chown=appuser:appuser . .
USER appuser
EXPOSE 8080
HEALTHCHECK CMD python -c "from urllib.request import urlopen; urlopen('http://127.0.0.1:8080/health')"
CMD ["sh","-c","uvicorn remote_api:app --host 0.0.0.0 --port ${PORT:-8080}"]
