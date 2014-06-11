FROM ubuntu:12.04

RUN apt-get update
RUN apt-get -y upgrade
RUN apt-get -y install python python-twisted python-beautifulsoup 
    
ADD . /sumdumbot/

ENV TEST 1

CMD ["python", "/sumdumbot/app/run.py"]