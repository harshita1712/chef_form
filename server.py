import json
import pandas as pd
import random
import socket
import time
from flask_cors import CORS
from flask import Flask, request, jsonify, render_template, send_file

app = Flask(__name__)
CORS(app)

def generate_random_ip():
    #response = requests.get(url)
    time.sleep(2)
    return ".".join(str(random.randint(0, 255)) for _ in range(4))


@app.route('/')
def index():
    return render_template('form.html') 


@app.route('/store_hostnames', methods=['POST'])
def store_hostnames():
    try:
        data = request.json 
        if 'hostnames' in data:
            hostname = data["hostnames"]
            host_data = {}
            host_data[hostname] = generate_random_ip()

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

@app.route('/download_csv')
def download_csv():
    # Define the path to the generated CSV file
    csv_file_path = 'output.csv'
    
    # Send the file for download
    return send_file(
        csv_file_path,
        as_attachment=True,
        download_name="output.csv"
    )

if __name__ == '__main__':
    app.run(debug=True)