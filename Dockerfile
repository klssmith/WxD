FROM python:3

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY app/ application.py ./
ENV FLASK_APP=application.py
CMD flask run --host=0.0.0.0
