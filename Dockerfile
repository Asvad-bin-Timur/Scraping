FROM python:3.10.8-slim
WORKDIR /app
COPY requirements.txt requirements.txt
RUN apt-get update && apt-get install -y --no-install-recommends \
    pkg-config \
    && python -m venv venv \
    && venv/bin/pip install --upgrade pip wheel setuptools \
    && venv/bin/pip install --no-cache-dir -r requirements.txt \
    && apt-get purge -y --auto-remove \
    && rm -rf /var/lib/apt/lists/*
COPY . /app
EXPOSE 8050
ENTRYPOINT [ "/app/venv/bin/python", "/app/Dashboard.py" ]
