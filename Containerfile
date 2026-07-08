# OCI image build file for Podman/Buildah/OpenShift/Kubernetes.
# Free/open-source alternative to Dockerfile.
FROM docker.io/python:3.11-slim

WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends g++ curl \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
RUN bash cpp/build.sh || true

EXPOSE 8501 8000

CMD ["streamlit", "run", "app/main.py", "--server.address=0.0.0.0", "--server.port=8501", "--server.headless=true"]
