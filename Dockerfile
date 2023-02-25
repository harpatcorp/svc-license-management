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

ENV ENC_KEY=qc1Un8Utu4wapfMzVcFpo9cXWVRQv6_oFbwQexhV3PM=
ENV APP_PATH=/usr/src/app/data/app
ENV IMG_PATH=/usr/src/app/data/images
ENV ORG_DATA_PATH=/usr/src/app/data/license/original_data
ENV ENC_DATA_PATH=/usr/src/app/data/license/encrypted_data
ENV CLIENT_ID=321006c79ba794b84a59522df8600123
ENV CLIENT_SECRET=1ea7cb51ebbb80442562b5bedf891f0841f6d8d1
ENV PAYMENT_URL=https://sandbox.cashfree.com/pg/orders
ENV DB_IP=192.168.1.9
ENV DB_PORT=5432
ENV DB_NAME=license_db
ENV DB_USER=root
ENV DB_PASS=root

COPY requirements.txt /usr/src/app/

RUN pip3 install --no-cache-dir -r requirements.txt

COPY . /usr/src/app

EXPOSE 8080

CMD ["flask", "run"]