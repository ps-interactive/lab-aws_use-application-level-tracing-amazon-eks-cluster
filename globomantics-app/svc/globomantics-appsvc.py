import os
from random import randint
from time import sleep
import datetime
from flask import Flask
from flask import request
import logging
from jaeger_client import Config
from flask_opentracing import FlaskTracing


app = Flask(__name__)
log_level = logging.DEBUG
logging.getLogger('').handlers = []
logging.basicConfig(format='%(asctime)s %(message)s', level=log_level)
jaeger_host = os.getenv('JAEGER_AGENT_HOST', "localhost")

# Tracer Instance Configuration Object
config = Config(
    config={
        'sampler':
        {'type': 'const',
         'param': 1},
        'logging': True,
        'local_agent': {
                'reporting_host': jaeger_host,
                'reporting_port': 6831,
            },
        'reporter_batch_size': 1,}, 
    service_name="globomantics-appsvc",
    validate=True,)

# OPENTRACING_TRACE_ALL = True
# OPENTRACING_TRACED_ATTRIBUTES = ['path', 'method', 'META', 'body', 'path_info', 'content_type', 'content_params', 'GET', 'POST', 'COOKIES', 'FILES', 'headers']
jaeger_tracer = config.initialize_tracer()
tracing = FlaskTracing(jaeger_tracer, True, app)

place = ['Chicago', 'New York', 'California']
visitorID = 1000

def getVisitor():
    return str(visitorID) + '. Your order is currently in dispatch at ' + getOrderLocation() + '. Your order will be delivered in ' + str(randint(2, 8)) + ' days.'

def setVisitor():
    global visitorID
    int(visitorID)
    sleep(randint(1,10))
    visitorID += 1
    return str(visitorID)

def getOrderLocation():
    return str(place[randint(0,2)])

@app.route('/api/order/status', methods=['GET', 'POST'])
def globomanticsSvc():
    with jaeger_tracer.start_span('Order Status Service') as span:
        span.log_kv({'event': 'Visitor Order Status', 'Current Guest ID': str(visitorID)})
        if request.method == 'GET':
            with jaeger_tracer.start_span('getOrderStatus', child_of=span) as child_span:
                child_span.log_kv({'event': 'visitor' + str(visitorID) +  'order status check at ' + str(datetime.datetime.now())})
                return getVisitor()
        elif request.method == 'POST':
            with jaeger_tracer.start_span('setVisitor', child_of=span) as child_span:
                child_span.log_kv({'event': 'New visitor' + str(visitorID) + 'set at ' + str(datetime.datetime.now())})
                return setVisitor()
    sleep(2) 
    jaeger_tracer.close() 

@app.route('/api/order/history', methods=['GET'])
def globomanticsSvcHistory():
    with jaeger_tracer.start_span('Order History Service') as span:
        span.log_kv({'event': 'Order History', 'Current Guest ID': str(visitorID)})
        if request.method == 'GET':
            with jaeger_tracer.start_span('getOrderHistory', child_of=span) as child_span:
                child_span.log_kv({'event': 'visitor' + visitorID +  'order status check at ' + str(datetime.datetime.now())})
                return "No orders available for the visitor - " + visitorID
    sleep(2) 
    jaeger_tracer.close() 