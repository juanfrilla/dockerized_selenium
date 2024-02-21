FROM python:3.11-slim

RUN apt-get update && apt-get install -y wget gnupg curl \
    && curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.3/install.sh | bash \
    && nvm install 16.13.1

ENV FLASK_RUN_PORT=3333
ENV FLASK_APP=app.py

RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && echo "deb http://dl.google.com/linux/chrome/deb/ stable main" | tee /etc/apt/sources.list.d/google.list \
    && apt-get update && apt-get install -y google-chrome-stable

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

EXPOSE 3333

CMD ["flask", "run", "--host=0.0.0.0", "--port=3333"]
