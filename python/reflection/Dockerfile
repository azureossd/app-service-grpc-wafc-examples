FROM python:3.10.5-slim

WORKDIR /app

COPY requirements.txt /app/
RUN pip install -r requirements.txt

COPY . /app/

EXPOSE 50051

CMD [ "python", "app.py" ]