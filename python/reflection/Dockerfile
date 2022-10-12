FROM python:3.9.14-slim

WORKDIR /app

COPY requirements.txt /app/
RUN pip install -r requirements.txt

COPY . /app/

EXPOSE 50051 8000

CMD [ "python", "app.py" ]