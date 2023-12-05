# Use Ubuntu 20.04 as the base image
FROM ubuntu:20.04

# Update package lists and install Python 3.9
RUN apt-get update \
    && apt-get install -y python3.9 \
    && apt install -y python3-pip \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Create symbolic links to set Python 3.9 as the default version
RUN update-alternatives --install /usr/bin/python python /usr/bin/python3.9 1 && \
    update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.9 1

# 1. Keeps Python from generating .pyc files in the container
# 2. Turns off buffering for easier container logging
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    TZ=Australia/Melbourne \
    # poetry:
    POETRY_VERSION=1.7.1 \
    POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_CACHE_DIR='/var/cache/pypoetry' \
    PATH="$PATH:/root/.local/bin"


ARG DEBIAN_FRONTEND=noninteractive

# Install Requirements
RUN pip install --upgrade pip \
    && pip install "poetry==$POETRY_VERSION"
COPY pyproject.toml poetry.lock ./

# Unfortunately Ubuntu & poetry install aren't friends ATM so we're resorting to regular ol' pip & a requirements file :(
RUN poetry export -f requirements.txt --output requirements.txt \
    && pip install -r requirements.txt
# RUN poetry install --no-ansi --no-root --without dev


# Install browser backend
RUN playwright install chromium \
    && playwright install-deps chromium

# Copy App
COPY naplan_scraper.py ./
COPY scraper/ ./scraper

# Run the scraper
# CMD ["python", "naplan_scraper.py", "45587"]
ENTRYPOINT ["python", "naplan_scraper.py"]