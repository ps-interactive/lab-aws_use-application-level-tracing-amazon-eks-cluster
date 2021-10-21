FROM alpine:3.8

RUN apk add --no-cache py3-pip python3 && \
    pip3 install flask Flask-Opentracing jaeger-client

COPY . /usr/src/appsvc

ENV FLASK_APP globomantics-appsvc.py

WORKDIR /usr/src/appsvc

CMD flask run --host=0.0.0.0 --port=5000