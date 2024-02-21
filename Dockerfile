FROM python:3.11-slim
ENV FLASK_RUN_PORT=3333
ENV FLASK_APP=app.py
RUN apt-get update && apt-get install -y wget gnupg
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
RUN echo "deb http://dl.google.com/linux/chrome/deb/ stable main" | tee /etc/apt/sources.list.d/google.list

RUN apt-get update && apt-get install -y google-chrome-stable

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

# Expose the port
EXPOSE 3333

# Run the application
CMD ["flask", "run", "--host=0.0.0.0", "--port=3333"]