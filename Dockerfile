FROM python:3.6
WORKDIR /srv
RUN apt-get update && apt-get install
RUN pip install --upgrade pip

ADD requirements/base.txt /srv/requirements/base.txt
RUN pip install -r requirements/base.txt
ADD . /srv
ENV PATH /srv:$PATH
