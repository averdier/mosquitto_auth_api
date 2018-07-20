FROM python:3.6

ADD ./requirements.txt /tmp/
RUN pip3 install -r /tmp/requirements.txt

RUN mkdir /auth

ADD ./app/ /auth/app/
ADD ./plugins /auth/plugins/
ADD ./app.ini /auth/
ADD ./*.py /auth/
ADD ./*.sh /auth/

WORKDIR /auth