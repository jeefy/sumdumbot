FROM ubuntu:12.04

RUN apt-get update
RUN apt-get -y upgrade
RUN apt-get -y install git python python-twisted python-beautifulsoup 
    
RUN git clone https://github.com/jeefy/sumdumbot.git /sumdumbot/

ENV TEST 1

CMD (cd /sumdumbot/ && git pull && python /sumdumbot/app/run.py)