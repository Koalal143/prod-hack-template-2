FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r /app/requirements.txt
COPY . .
EXPOSE 8000

CMD bash -c "uvicorn --host 0.0.0.0 --port 8000 src.main:app"