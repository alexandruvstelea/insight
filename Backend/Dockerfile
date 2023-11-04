FROM python:latest

RUN mkdir -p /usr/feedback_backend

COPY . /usr/feedback_backend

WORKDIR /usr/feedback_backend

RUN pip install -r requirements.txt

CMD ["python3", "main.py"]