# Dockerfile (REST API)
FROM python:3.9-slim

WORKDIR /app

COPY app.py .
COPY rules.pkl .  # Include the pre-generated rules file

RUN pip install flask

# Copy application code
COPY . /app/

# queremos usar porta 8000?
EXPOSE 8000

CMD ["python", "app.py"]
