FROM python:3.8.0-slim

RUN apt-get update \
&& apt-get install gcc -y \
&& apt-get clean

RUN mkdir -p /usr/src/app
RUN mkdir -p /usr/src/app/data
RUN mkdir -p /usr/src/app/data/app
RUN mkdir -p /usr/src/app/data/images
RUN mkdir -p /usr/src/app/data/license
RUN mkdir -p /usr/src/app/data/license/original_data
RUN mkdir -p /usr/src/app/data/license/encrypted_data

WORKDIR /usr/src/app

COPY requirements.txt /usr/src/app/

RUN pip3 install --no-cache-dir -r requirements.txt

COPY . /usr/src/app

EXPOSE 8080

CMD ["flask", "run"]
