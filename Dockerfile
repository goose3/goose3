FROM ubuntu:20.04

LABEL maintainer="Krishna Kumar <krishsat9937@gmail.com>"

RUN apt-get clean
RUN apt-get update

RUN apt-get install -y python3
RUN apt install python3-pip -y

WORKDIR /code
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

COPY requirements.txt requirements.txt
# COPY en_core_web_lg-3.2.0.tar.gz en_core_web_lg-3.2.0.tar.gz
RUN pip3 install -r requirements.txt
# RUN python3 -m spacy download en_core_web_lg
EXPOSE 5000
COPY . .
CMD ["flask", "run"]
# CMD [ "pip3 install -r requirements.txt" ]


