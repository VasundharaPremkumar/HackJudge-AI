
FROM python:3.12-slim

# Prevent Python from generating unnecessary files
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Create a non-root user
RUN groupadd -g 10001 runner && \
    useradd -m -u 10001 -g runner runner

# Set working directory
WORKDIR /workspace

# Run as a non-root user
USER runner

# Default execution command
ENTRYPOINT ["python"]
