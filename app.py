import requests
import json
from flask import Flask
from flask import render_template
from flask import request

from login_details import GMAPS_API_KEY

app = Flask(__name__)

API_IP_ADDRESS = '127.0.0.1:5000'
HOST_IP_ADDRESS = '192.168.153.1'

NODE_SUFFIX = '/node/'
LOCATION_SUFFIX = '/location/'
BUOY_SUFFIX = '/buoy/'
REMOVE_BUOY_SUFFIX = '/remove_buoy/'
LAST_MESSAGE_SUFFIX = '/last_message/'

LOCATION_ID = '<location_id>/'
BUOY_ID = '<buoy_id>/'
SIGFOX_ID = '<sigfox_id>/'

HTTP_PREFIX = 'http://'

SIGFOX_ID_KEY = 'sigfox_id'
BUOY_ID_KEY = 'buoy_id'
LOCATION_ID_KEY = 'location_id'
LOCATION_NAME_KEY = 'location_name'
LOCATION_TYPE_KEY = 'location_type'
BUOY_LOCATION_KEY = 'buoy_location'
LATITUDE_KEY = 'latitude'
LONGITUDE_KEY = 'longitude'
AT_LOCATION_KEY = 'at_location'

LOCATION_TYPES = ['URBAN', 'SUBURBAN', 'RURAL', 'BEACH', 'QUAY', 'RIVER']


@app.route('/')
def index_page():
    return "Hello, World!"

@app.route(NODE_SUFFIX, methods=['GET', 'POST'])
def nodes_page():
    url = '%s%s%s' % (HTTP_PREFIX, API_IP_ADDRESS, NODE_SUFFIX)
    if request.method == 'POST':
        sigfox_id = request.form.get(SIGFOX_ID_KEY)
        data = {SIGFOX_ID_KEY: sigfox_id}

        buoy_id = request.form.get(BUOY_ID_KEY)
        if buoy_id is not None and buoy_id.lower() != 'none':
            data[BUOY_ID_KEY] = buoy_id

        requests.post(url, data)
    
    response = requests.get(url)
    nodes = json.loads(response.text)

    url = '%s%s%s' % (HTTP_PREFIX, API_IP_ADDRESS, BUOY_SUFFIX)
    response = requests.get(url)
    buoys = json.loads(response.text)

    return render_template('nodes_table.html', nodes=nodes, 
                        host_ip=HOST_IP_ADDRESS, buoys=buoys, 
                        gmaps_api_key=GMAPS_API_KEY)

@app.route(NODE_SUFFIX + SIGFOX_ID, methods=['GET', 'POST'])
def node_last_message_page(sigfox_id):
    url = '%s%s%s' % (HTTP_PREFIX, API_IP_ADDRESS, LAST_MESSAGE_SUFFIX)
    url += '%s/' % (sigfox_id, )
    response = requests.get(url)
    last_message = json.loads(response.text) 

    return render_template('last_message.html', last_messages=last_message, host_ip=HOST_IP_ADDRESS)

@app.route(LOCATION_SUFFIX, methods=['GET', 'POST'])
def locations_page():
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
    return render_template('locations_table.html', locations=data, host_ip=HOST_IP_ADDRESS,
                                                location_types=LOCATION_TYPES)

@app.route(LOCATION_SUFFIX + LOCATION_ID, methods=['GET', 'POST'])
def buoys_by_location_page(location_id):
    url = '%s%s%s' % (HTTP_PREFIX, API_IP_ADDRESS, BUOY_SUFFIX)
    url += '%s/' % (location_id, )
    response = requests.get(url)
    data = json.loads(response.text)
    title = "Buoys at %s" % (data[0]['location_name'], )
    return render_template('buoys_table.html', buoys=data, host_ip=HOST_IP_ADDRESS, title=title)


@app.route(BUOY_SUFFIX, methods=['GET', 'POST'])
def buoys_page():
    url = '%s%s%s' % (HTTP_PREFIX, API_IP_ADDRESS, BUOY_SUFFIX)
    if request.method == 'POST':
        buoy_location = request.form.get(BUOY_LOCATION_KEY)
        buoy_latitude = request.form.get(LATITUDE_KEY)
        buoy_longitude = request.form.get(LONGITUDE_KEY)
        at_location = request.form.get(AT_LOCATION_KEY)
        data = {
            BUOY_LOCATION_KEY: buoy_location,
            LATITUDE_KEY: buoy_latitude,
            LONGITUDE_KEY: buoy_longitude,
            AT_LOCATION_KEY: at_location
        }

        requests.post(url, data)
    
    response = requests.get(url)
    data = json.loads(response.text)
    url = '%s%s%s' % (HTTP_PREFIX, API_IP_ADDRESS, LOCATION_SUFFIX)
    response = requests.get(url)
    locations = json.loads(response.text)
    return render_template('buoys_table.html', buoys=data, host_ip=HOST_IP_ADDRESS, locations=locations)

@app.route(REMOVE_BUOY_SUFFIX + BUOY_ID, methods=['GET'])
def remove_buoy(buoy_id):
    url = "%s%s%s" % (HTTP_PREFIX, API_IP_ADDRESS, BUOY_SUFFIX)
    url += '%s/' % (buoy_id, )
    requests.delete(url)
    return buoys_page()

if __name__ == '__main__':
    app.run(host=HOST_IP_ADDRESS)
