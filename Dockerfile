
FROM python:3.10-slim

WORKDIR /app

COPY . /app

EXPOSE 8085

CMD ["python", "main.py"]