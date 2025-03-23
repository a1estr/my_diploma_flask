FROM python:3.9-slim

WORKDIR /app

# Устанавливаем зависимости для psycopg2
RUN apt-get update && apt-get install -y \
    libpq-dev gcc curl && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

EXPOSE 5000

CMD ["flask", "run"]
