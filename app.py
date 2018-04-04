import requests
import json
from flask import Flask
from flask import render_template
from flask import request

app = Flask(__name__)

API_IP_ADDRESS = '127.0.0.1:5000'
HOST_IP_ADDRESS = '192.168.153.1'


@app.route('/')
def index_page():
    return "Hello, World!"

@app.route('/node/', methods=['GET', 'POST'])
def nodes_page():
    if request.method == 'POST':
        sigfox_id = request.form.get('sigfox_id')
        data = {'sigfox_id': sigfox_id}
        requests.post('http://%s/node/' % (API_IP_ADDRESS), data)
    
    response = requests.get('http://%s/node/' % (API_IP_ADDRESS))
    data = json.loads(response.text)
    return render_template('nodes_table.html', nodes=data, host_ip=HOST_IP_ADDRESS)

if __name__ == '__main__':
    app.run(host=HOST_IP_ADDRESS)
