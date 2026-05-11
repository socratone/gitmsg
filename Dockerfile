FROM python:3.12-slim

RUN pip install --no-cache-dir openai && \
    apt-get update && \
    apt-get install -y --no-install-recommends git && \
    rm -rf /var/lib/apt/lists/*

COPY gcm.py /usr/local/bin/gcm.py

WORKDIR /workspace

ENTRYPOINT ["python", "/usr/local/bin/gcm.py"]
