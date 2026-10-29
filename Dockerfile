FROM python:3.13-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY app ./app
COPY sql ./sql
COPY sample_logs ./sample_logs

CMD ["python", "-m", "app.main", "summary"]