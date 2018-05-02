import requests
import json
from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for

from handler.api_handler import ApiHandler

from login_details import GMAPS_API_KEY

app = Flask(__name__)
API = ApiHandler()

API_IP_ADDRESS = '127.0.0.1:5000'
HOST_IP_ADDRESS = '192.168.153.1'

NODE_SUFFIX = '/node/'
LOCATION_SUFFIX = '/location/'
BUOY_SUFFIX = '/buoy/'
REMOVE_BUOY_SUFFIX = '/remove_buoy/'
REMOVE_NODE_SUFFIX = '/remove_node/'
REMOVE_LOCATION_SUFFIX = '/remove_location/'
NODE_STATUS_SUFFIX = '/node_status/'
LAST_MESSAGE_SUFFIX = '/last_message/'
UPDATE_BUOY_SUFFIX = '/update_buoy/'
CHANGE_LOCATION_SUFFIX = '/change_location/'

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
    return render_template('index.html')

@app.route(NODE_SUFFIX, methods=['GET'])
def nodes_page():
    nodes = None
    buoys = None
    
    nodes = API.get_data(NODE_SUFFIX)
    buoys = API.get_data(BUOY_SUFFIX)

    return render_template('nodes_table.html', nodes=nodes, 
                        buoys=buoys, gmaps_api_key=GMAPS_API_KEY)

@app.route(NODE_SUFFIX, methods=['POST'])
def add_node():
    sigfox_id = request.form.get(SIGFOX_ID_KEY)
    data = {SIGFOX_ID_KEY: sigfox_id}

    buoy_id = request.form.get(BUOY_ID_KEY)
    if buoy_id is not None and buoy_id.lower() != 'none':
        data[BUOY_ID_KEY] = buoy_id

    API.post_form(NODE_SUFFIX, data)
    return redirect(url_for('nodes_page'))

@app.route(NODE_SUFFIX + SIGFOX_ID, methods=['GET', 'POST'])
def node_last_message_page(sigfox_id):
    last_message = API.get_specific_data(LAST_MESSAGE_SUFFIX, sigfox_id)
    return render_template('last_message.html', last_messages=last_message)

@app.route(LOCATION_SUFFIX, methods=['GET'])
def locations_page():
    data = None
    data = API.get_data(LOCATION_SUFFIX)

    location_types = None
    if data:
        location_types = LOCATION_TYPES

    return render_template('locations_table.html', locations=data,
                                                location_types=location_types)

@app.route(LOCATION_SUFFIX, methods=['POST'])
def add_location():
    location_name = request.form.get(LOCATION_NAME_KEY)
    location_type = request.form.get(LOCATION_TYPE_KEY)
    location_id = request.form.get(LOCATION_ID_KEY)
    data = {
        LOCATION_NAME_KEY: location_name,
        LOCATION_TYPE_KEY: location_type,
        LOCATION_ID_KEY: location_id
    }
    
    API.post_form(LOCATION_SUFFIX, data)

    return redirect(url_for('locations_page'))


@app.route(LOCATION_SUFFIX + LOCATION_ID, methods=['GET', 'POST'])
def buoys_by_location_page(location_id):
    title = "Locations Page"

    data = API.get_specific_data(BUOY_SUFFIX, location_id)
    if len(data) > 0:
        title = "Buoys at %s" % (data[0]['location_name'], )

    return render_template('buoys_table.html', buoys=data, title=title)


@app.route(BUOY_SUFFIX, methods=['GET'])
def buoys_page():
    data = None
    locations = None
    try:
        data = API.get_data(BUOY_SUFFIX)
        locations = API.get_data(LOCATION_SUFFIX)
    except:
        print("Error connecting to API")

    return render_template('buoys_table.html', buoys=data, locations=locations)

@app.route(BUOY_SUFFIX, methods=['POST'])
def add_buoy():
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

    API.post_form(BUOY_SUFFIX, data)

    return redirect(url_for('buoys_page'))

@app.route(REMOVE_BUOY_SUFFIX + BUOY_ID, methods=['GET'])
def remove_buoy(buoy_id):
    API.remove_element(BUOY_SUFFIX, buoy_id)
    return redirect(url_for('buoys_page'))

@app.route(REMOVE_NODE_SUFFIX + SIGFOX_ID, methods=['GET', 'POST'])
def remove_node(sigfox_id):
    API.remove_element(NODE_SUFFIX, sigfox_id)
    return redirect(url_for('nodes_page'))

@app.route(NODE_STATUS_SUFFIX + SIGFOX_ID, methods=['GET', 'POST'])
def change_node_status(sigfox_id):
    API.patch(NODE_SUFFIX, sigfox_id)
    return redirect(url_for('nodes_page'))

@app.route(REMOVE_LOCATION_SUFFIX + LOCATION_ID, methods=['GET', 'POST'])
def remove_location(location_id):
    API.remove_element(LOCATION_SUFFIX, location_id)
    return redirect(url_for('locations_page'))

@app.route(UPDATE_BUOY_SUFFIX + BUOY_ID, methods=['GET', 'POST'])
def update_buoy_time_checked(buoy_id):
    API.patch(BUOY_SUFFIX, buoy_id)
    return redirect(url_for('buoys_page'))

@app.route(CHANGE_LOCATION_SUFFIX + LOCATION_ID, methods=['GET', 'POST'])
def change_location(location_id):
    return render_template('edit_location.html', location_id=location_id, location_types=LOCATION_TYPES)

if __name__ == '__main__':
    app.run(host=HOST_IP_ADDRESS)
