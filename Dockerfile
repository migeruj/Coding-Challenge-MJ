FROM python:3.10.12-slim

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY . .

EXPOSE $PORT

CMD uvicorn main:app --host 0.0.0.0 --port $PORT --reload --proxy-headers