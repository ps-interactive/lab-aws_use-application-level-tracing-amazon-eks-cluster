import os
import requests
import logging
from time import sleep
from flask import Flask
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
                 'local_agent': {
                'reporting_host': jaeger_host,
                'reporting_port': 6831,
            },
                        'logging': True,
                        'reporter_batch_size': 1,}, 
                        service_name="globomantics-webapp")
jaeger_tracer = config.initialize_tracer()
tracing = FlaskTracing(jaeger_tracer, True, app)

def getOrderDetails(app_endpoint):
    service_response = requests.get(app_endpoint)
    return service_response.text

def newVisitor(app_endpoint):
    service_response = requests.post(app_endpoint)
    return service_response

@app.route('/')
def globomanticWeb():
    with jaeger_tracer.start_span('Globomantics OrderStatus App') as span:
        globomantics_endpoint = os.environ.get('SERVICE_ENDPOINT', default="https://localhost:5000")
        globomantics_service = f'{globomantics_endpoint}/api/order/status'
        response = getOrderDetails(globomantics_service)
        span.log_kv({'event': 'Order Details message', 'Visitor': response})
        newVisitor(globomantics_service)

        return f"""Hello, Globomantics User!

        You are visitor number {response} !\n\n"""    

