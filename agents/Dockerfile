ARG AGENT_MODULE=agents.market_correlation.app
ARG AGENT_PORT=8002

FROM python:3.12-slim

WORKDIR /app

COPY agents/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY agents/ ./agents/

ARG AGENT_MODULE
ARG AGENT_PORT
ENV AGENT_MODULE=${AGENT_MODULE}
ENV AGENT_PORT=${AGENT_PORT}

EXPOSE ${AGENT_PORT}

CMD uvicorn ${AGENT_MODULE}:app --host 0.0.0.0 --port ${AGENT_PORT}
