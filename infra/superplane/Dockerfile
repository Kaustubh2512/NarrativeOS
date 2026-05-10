FROM python:3.12-slim

WORKDIR /app

COPY pyproject.toml .
RUN pip install --no-cache-dir fastapi uvicorn httpx

COPY infra/superplane/bridge.py infra/superplane/bridge.py

EXPOSE 8765
CMD ["uvicorn", "infra.superplane.bridge:app", "--host", "0.0.0.0", "--port", "8765"]
