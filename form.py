from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import random
import socket

app = Flask(__name__)
CORS(app)

def generate_random_ip():
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

            print(host_data)
            with open('hostnames.json', 'w') as json_file:
                json.dump(host_data, json_file, indent=4)

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
