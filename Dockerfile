FROM python:3.4
ENV PYTHONUNBUFFERED 1
RUN mkdir -p /code
ADD webmath/requirements.txt /code/
WORKDIR /code
RUN pip install -r requirements.txt
ADD webmath /code/