# Use the official Python image as a base image
FROM python:3.11-slim

# So logs will show right away
ENV PYTHONUNBUFFERED 1

# Copy files
COPY ./app/requirements.txt /tmp/requirements.txt
COPY ./app/requirements.dev.txt /tmp/requirements.dev.txt

WORKDIR /app

# Update package index and install required packages in a single command
RUN apt-get update && \
    apt-get install -y \
    # Your dependencies here \
    && rm -rf /var/lib/apt/lists/*

# deafult environment. set DEV to false
ARG DEV=false

# Set up env and install dependencies
RUN python -m venv /py && \
    # upgrade pip
    /py/bin/pip install --upgrade pip && \
    # install requirements.txt
    /py/bin/pip install -r /tmp/requirements.txt && \
    # install requirements.dev.txt to install dev dependencies, only when $DEV is true
    if [ $DEV = "true" ]; \
        then /py/bin/pip install -r /tmp/requirements.dev.txt ; \
    fi && \
    # delete /tmp dir for cleanup
    rm -rf /tmp

COPY ./app /app

# update PATH env variable so when we run a command in docker, we dont need to specify the full path of our environment
ENV PATH="/py/bin:$PATH"
