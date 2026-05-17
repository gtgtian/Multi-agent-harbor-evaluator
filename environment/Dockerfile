FROM python:3.11-slim

WORKDIR /workspace

RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    curl \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy the buggy library and test cases into the workspace
COPY input_artifacts/pyreport /workspace/pyreport
COPY input_artifacts/test_cases.py /workspace/test_cases.py

# No extra PyPI dependencies needed — pyreport uses only stdlib.
# Install pytest for agent convenience (agent may run tests interactively).
RUN pip install --no-cache-dir pytest

# Ensure /logs directories exist
RUN mkdir -p /logs/agent /logs/verifier
