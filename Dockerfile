FROM python:3.11-slim

# Install necessary packages (including Chrome)
RUN apt-get update && apt-get install -y wget gnupg
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -

RUN sh -c 'echo "deb [arch=amd64] https://dl.google.com/linux/chrome/deb/stable main" >> /etc/apt/sources.list.d/google.list'

RUN apt-get install -y google-chrome-stable

# Set working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Copy the rest of the application files
COPY . .

# Expose the port
EXPOSE 5000

# Run the application
CMD ["python", "main.py"]