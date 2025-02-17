FROM python:3.12.8-bookworm
LABEL authors="Eko Indarto"


# Combine apt-get commands to reduce layers
RUN apt-get update -y && \
    apt-get upgrade -y && \
    apt-get dist-upgrade -y && \
    apt-get install -y --no-install-recommends git curl && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN useradd -ms /bin/bash akmi

ENV PYTHONPATH=/home/akmi/ras/src
ENV BASE_DIR=/home/akmi/ras

WORKDIR ${BASE_DIR}


# Install uv.
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Copy the application into the container.


# Create and activate virtual environment
RUN python -m venv .venv
ENV PATH="/home/akmi/ras/.venv/bin:$PATH"
# Copy the application into the container.
COPY src ./src
COPY pyproject.toml .
COPY README.md .
COPY uv.lock .

RUN uv venv .venv
# Install dependencies

RUN uv sync --frozen --no-cache

# Run the application.
CMD ["python", "-m", "src.main"]

#CMD ["tail", "-f", "/dev/null"]