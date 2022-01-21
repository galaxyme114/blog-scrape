FROM python:3.7

ENV PYTHONUNBUFFERED=1
ENV WEBAPP_DIR=/webapp

RUN mkdir $WEBAPP_DIR

WORKDIR $WEBAPP_DIR

ADD requirements/base.txt $WEBAPP_DIR/ 

RUN pip install -r requirements/base.txt

ADD . $WEBAPP_DIR/