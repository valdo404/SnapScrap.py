# Stage 1: Build
FROM python:3.9 as builder

# Set working directory
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# Copy source code
COPY SnapScrap.py .

# Stage 2: Run
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy only the dependencies installation from the 1st stage image
COPY --from=builder /root/.local /root/.local
COPY --from=builder /app/SnapScrap.py .

# Make sure scripts in .local are usable:
ENV PATH=/root/.local/bin:$PATH

ENV DATA_DIR /data

# Command to run
ENTRYPOINT ["sh", "-c", "cd $DATA_DIR && python3 /app/SnapScrap.py \"$@\"", "--"]

