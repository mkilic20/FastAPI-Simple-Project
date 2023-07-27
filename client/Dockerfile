FROM python:3.10-slim-buster

WORKDIR /app

COPY requirements.txt /app/requirements.txt

RUN pip install -r requirements.txt

COPY . /app

CMD ["uvicorn", "client:app", "--host", "0.0.0.0", "--port", "8000"]