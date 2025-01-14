# Dockerfile (Model Generator)
FROM python:3.9-slim

WORKDIR /app

COPY ml_code.py .

RUN pip install fpgrowth-py

CMD ["python", "ml_code.py"]
