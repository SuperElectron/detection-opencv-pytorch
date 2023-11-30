# Build stage

FROM python:3.9.9-slim-bullseye as prod

WORKDIR /application/

RUN pip install 'poetry'

COPY pyproject.toml .

RUN --mount=type=cache,target=/var/cache/apt apt-get update -yqq && \
    apt-get install -yqq --no-install-recommends \
    build-essential \
    libgl1 \
    libaio1 \
    libglib2.0-0 \
    libsm6 \
    libxrender1 \
    libxext6 \
    curl && \
    rm -rf /var/lib/apt/lists/*

RUN poetry install --no-interaction --no-root

RUN poetry run poe install-deps

RUN poetry run poe install

COPY . .

CMD ["poetry", "run", "python", "./src/main.py"]