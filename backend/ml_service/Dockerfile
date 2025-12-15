FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --upgrade pip \
 && pip install --no-cache-dir --default-timeout=300 --retries 5 -r requirements.txt

COPY . .

CMD ["python", "app.py"]
