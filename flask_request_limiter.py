from flask import Flask, request, jsonify, Response
import requests
import psycopg2
from datetime import datetime
import socket
import time
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

app = Flask(__name__)

limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["5 per day"]
)

DB_HOST = 'localhost'
DB_PORT = '5432'
DB_NAME = 'grafana'
DB_USER = 'grafana'
DB_PASS = 'grafana'

def create_table():
    conn = psycopg2.connect(host=DB_HOST, port=DB_PORT, dbname=DB_NAME, user=DB_USER, password=DB_PASS)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS data_tools.url_requests (
            id SERIAL PRIMARY KEY,
            url TEXT NOT NULL,
            timestamp TIMESTAMP NOT NULL,
            response_code INTEGER,
            ip_address TEXT
        )
    """)
    conn.commit()
    cur.close()
    conn.close()

create_table()

def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
        return local_ip
    except Exception as e:
        return str(e)

def get_public_ip():
    try:
        response = requests.get('https://api.ipify.org?format=json')
        public_ip = response.json().get('ip')
        return public_ip
    except Exception as e:
        return str(e)

@app.route('/fetch', methods=['GET'])
@limiter.limit("5 per day")
def fetch_url():
    url = request.args.get('url')
    if not url:
        return jsonify({'error': 'URL parameter is required'}), 400

    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        time.sleep(5)
        response_code = response.status_code
        local_ip = get_local_ip()

        conn = psycopg2.connect(host=DB_HOST, port=DB_PORT, dbname=DB_NAME, user=DB_USER, password=DB_PASS)
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO data_tools.url_requests (url, timestamp, response_code, ip_address)
            VALUES (%s, %s, %s, %s)
        """, (url, datetime.now(), response_code, local_ip))
        conn.commit()
        cur.close()
        conn.close()

        content_type = response.headers.get('Content-Type', '')
        if 'application/pdf' in content_type:
            return Response(response.content, content_type='application/pdf')

        return response.text, response_code

    except requests.RequestException as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=1111)
 
