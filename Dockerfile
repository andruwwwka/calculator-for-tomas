FROM python:3.8.1-alpine3.11

RUN apk add postgresql-dev gcc musl-dev make

COPY requirements.txt /app/
WORKDIR /app
RUN pip install -r requirements.txt

COPY . .

EXPOSE 5000:5000

CMD ["python", "entry.py"]