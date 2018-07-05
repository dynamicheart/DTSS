FROM python:2.7-slim

MAINTAINER Jianbang Yang <yangjianbang112@gmail.com>

WORKDIR /rater

ADD . /rater

RUN pip install --trusted-host pypi.python.org -r requirements.txt

CMD ["python", "rater.py"]
