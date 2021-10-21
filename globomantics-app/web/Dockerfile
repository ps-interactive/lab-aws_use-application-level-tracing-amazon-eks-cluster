FROM alpine:3.8

RUN apk add --no-cache py3-pip python3 && \
    pip3 install flask requests Flask-Opentracing jaeger-client

COPY . /usr/src/webapp

ENV FLASK_APP globomantics-webapp.py

WORKDIR /usr/src/webapp

CMD flask run --host=0.0.0.0 --port=8000