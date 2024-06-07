FROM python:3.11-slim

ENV FLASK_RUN_PORT=3333
ENV FLASK_APP=app.py

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

EXPOSE 3333

# Run the application
CMD ["flask","--debug", "run", "--host=0.0.0.0", "--port=3333"]
