FROM python:3.12.3-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt --no-cache-dir

RUN apt-get update && apt-get install -y netcat-openbsd

COPY . .

RUN chmod +x /app/start.sh

CMD ["/app/start.sh"]