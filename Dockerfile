FROM python:3.11-slim AS base

# Set Flask environment variables
ENV FLASK_RUN_PORT=3333
ENV FLASK_APP=app.py

# Install system dependencies
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /app

# Copy requirements and install Python dependencies
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Copy the application files
COPY . .

# Expose the port
EXPOSE 3333

# Define entrypoint for Flask application
CMD ["flask", "run", "--host=0.0.0.0", "--port=3333"]

# Stage for installing Node.js
FROM base AS node

# Install NVM (Node Version Manager)
RUN curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.3/install.sh | bash

# Install Node.js using NVM
RUN /bin/bash -c "source /root/.nvm/nvm.sh && nvm install 16.13.1"

# Set environment variables for Node.js
ENV NVM_DIR=/root/.nvm
ENV NODE_VERSION=16.13.1

# Set Node.js in the PATH
ENV PATH=$NVM_DIR/versions/node/v$NODE_VERSION/bin:$PATH

# Stage for installing Google Chrome
FROM base AS chrome

# Install Google Chrome
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && echo "deb http://dl.google.com/linux/chrome/deb/ stable main" | tee /etc/apt/sources.list.d/google.list \
    && apt-get update && apt-get install -y google-chrome-stable
