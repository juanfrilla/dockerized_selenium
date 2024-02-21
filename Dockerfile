FROM python:3.11-slim

# Set Flask environment variables
ENV FLASK_RUN_PORT=3333
ENV FLASK_APP=app.py

# Install system dependencies
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install NVM (Node Version Manager)
RUN curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.3/install.sh | bash

# Set NVM environment variables
ENV NVM_DIR="/root/.nvm"
ENV SH_ENV="/root/.bashrc"

# Install Node.js using NVM
RUN /bin/bash -c "source $NVM_DIR/nvm.sh \
    && nvm install 16.13.1 \
    && nvm alias default 16.13.1"

# Update PATH to include Node.js binaries
ENV PATH="/root/.nvm/versions/node/v16.13.1/bin:$PATH"

# Install Google Chrome
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && echo "deb http://dl.google.com/linux/chrome/deb/ stable main" | tee /etc/apt/sources.list.d/google.list \
    && apt-get update && apt-get install -y google-chrome-stable

# Set the working directory
WORKDIR /app

# Copy requirements and install Python dependencies
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Copy the application files
COPY . .

# Expose the port
EXPOSE 3333

# Run the application
CMD ["flask","--debug", "run", "--host=0.0.0.0", "--port=3333"]
