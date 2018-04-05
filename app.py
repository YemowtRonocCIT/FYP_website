import requests
import json
from flask import Flask
from flask import render_template
from flask import request

app = Flask(__name__)

API_IP_ADDRESS = '127.0.0.1:5000'
HOST_IP_ADDRESS = '192.168.153.1'

NODE_SUFFIX = '/node/'
LOCATION_SUFFIX = '/location/'

HTTP_PREFIX = 'http://'

SIGFOX_ID_KEY = 'sigfox_id'
LOCATION_NAME_KEY = 'location_name'
LOCATION_TYPE_KEY = 'location_type'

@app.route('/')
def index_page():
    return "Hello, World!"

@app.route(NODE_SUFFIX, methods=['GET', 'POST'])
def nodes_page():
    url = '%s%s%s' % (HTTP_PREFIX, API_IP_ADDRESS, NODE_SUFFIX)
    if request.method == 'POST':
        sigfox_id = request.form.get(SIGFOX_ID_KEY)
        data = {SIGFOX_ID_KEY: sigfox_id}
        requests.post(url, data)
    
    response = requests.get(url)
    data = json.loads(response.text)
    return render_template('nodes_table.html', nodes=data, host_ip=HOST_IP_ADDRESS)

@app.route(LOCATION_SUFFIX, methods=['GET', 'POST'])
def locations_pages():
    url = '%s%s%s' % (HTTP_PREFIX, API_IP_ADDRESS, LOCATION_SUFFIX)
    if request.method == 'POST':
        location_name = request.form.get(LOCATION_NAME_KEY)
        location_type = request.form.get(LOCATION_TYPE_KEY)
        data = {
            LOCATION_NAME_KEY: location_name,
            LOCATION_TYPE_KEY: location_type
        }
        requests.post(url, data)
    
    response = requests.get(url)
    data = json.loads(response.text)
    return render_template('locations_table.html', locations=data, host_ip=HOST_IP_ADDRESS)

if __name__ == '__main__':
    app.run(host=HOST_IP_ADDRESS)
