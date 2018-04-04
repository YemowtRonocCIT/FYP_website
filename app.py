import requests
import json
from flask import Flask
from flask import render_template
from flask import request

app = Flask(__name__)


@app.route('/')
def index_page():
    return "Hello, World!"

@app.route('/nodes', methods=['GET', 'POST'])
def nodes_page():
    if request.method == 'POST':
        sigfox_id = request.form.get('sigfox_id')
        data = {'sigfox_id': sigfox_id}
        requests.post('http://192.168.153.1:5000/node/', data)
    
    response = requests.get('http://192.168.153.1:5000/node')
    data = json.loads(response.text)
    return render_template('nodes_table.html', nodes=data)

if __name__ == '__main__':
    app.run()
