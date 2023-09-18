import json
import pandas as pd
import random
import socket
import time
from flask_cors import CORS
from flask import Flask, request, jsonify

app = Flask(__name__)
CORS(app)

def generate_random_ip():
    #response = requests.get(url)
    time.sleep(2)
    return ".".join(str(random.randint(0, 255)) for _ in range(4))

@app.route('/', methods=['GET'])
def verify_server():
    return jsonify({'working': "true"}), 200


@app.route('/store_hostnames', methods=['POST'])
def store_hostnames():
    try:
        data = request.json
        if 'hostnames' in data:
            hostnames = data['hostnames'].split('\n')
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
                'message': 'Hostnames stored in JSON file with random IPs.',
                'data': host_data
            }
            return jsonify(response), 200
        else:
            return jsonify({'message': 'No hostnames provided.'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)