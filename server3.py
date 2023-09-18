import json
import pandas as pd
import random
import socket
import time
from flask_cors import CORS
from flask import Flask, request, jsonify, render_template

app = Flask(__name__, template_folder='.')
CORS(app)

def generate_random_ip():
    #response = requests.get(url)
    time.sleep(2)
    return ".".join(str(random.randint(0, 255)) for _ in range(4))


@app.route('/')
def index():
    return render_template('form3.html') 


@app.route('/store_hostnames', methods=['POST'])
def store_hostnames():
    try:
        if 'hostnames' in request.form:
            hostnames = request.form["hostnames"].split('\n')
            print(hostnames)
            host_data = {}

            for hostname in hostnames:
                if hostname.strip():
                    ip = generate_random_ip()
                    host_data[hostname.strip()] = ip

            df = pd.DataFrame.from_dict(host_data, orient='index').reset_index()
            df.columns = ["hostname","ip"]
            df.to_csv('output.csv', index=False)
            
            response = {
                'message': 'Hostnames stored in CSV file with random IPs.',
                'data': host_data
            }
            return jsonify(response), 200
        else:
            return jsonify({'message': 'No hostnames provided.'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
if __name__ == '__main__':
    app.run(debug=True)