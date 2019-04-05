FROM python:3.6

COPY ./requirements.txt /var/www/

RUN pip install -r /var/www/requirements.txt

ENV PYTHON_PATH=/var/www
ENV FLASK_APP=app
ENV FLASK_ENV=development
ENV FLASK_DEBUG=1
COPY ./app.py /var/www/

WORKDIR /var/www