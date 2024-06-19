FROM --platform=linux/amd64 python:3.9-alpine

WORKDIR /app

COPY . /app

RUN pip install --upgrade pip

RUN pip install flask requests

EXPOSE 5000

CMD ["python", "app/main.py", "--mode", "api"]