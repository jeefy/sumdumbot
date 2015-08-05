FROM ubuntu:14.04

RUN apt-get update && \
    apt-get -y upgrade && \
    apt-get -y install python python-twisted python-beautifulsoup 

ENV TEST 1

COPY app/ /sumdumbot/

WORKDIR /sumdumbot/

CMD python run.py