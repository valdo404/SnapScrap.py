# Stage 1: Build
FROM python:3.9 AS builder

# Set working directory
WORKDIR /app

# Install Poetry
ENV POETRY_HOME=/opt/poetry
RUN curl -sSL https://install.python-poetry.org | python3 - && \
    cd /usr/local/bin && \
    ln -s /opt/poetry/bin/poetry && \
    poetry config virtualenvs.create false

# Copy Poetry files
COPY pyproject.toml poetry.lock ./

# Install dependencies
RUN poetry install --no-root

# Copy source code
COPY SnapScrap.py .

# Stage 2: Run
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy Python packages and source code
COPY --from=builder /usr/local/lib/python3.9/site-packages/ /usr/local/lib/python3.9/site-packages/
COPY --from=builder /app/SnapScrap.py .

ENV DATA_DIR=/data

# Command to run
ENTRYPOINT ["sh", "-c", "cd $DATA_DIR && python3 /app/SnapScrap.py \"$@\"", "--"]

