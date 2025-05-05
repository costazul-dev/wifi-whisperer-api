from flask import Flask, request, jsonify
import mysql.connector
import os

app = Flask(__name__)

# Database configuration (using environment variables for security)
DB_HOST = "localhost"
DB_USER = "api_user"
DB_PASSWORD = os.environ.get("DB_PASSWORD")
DB_NAME = "wifi_data"

# API Key (from environment variable)
API_KEY = os.environ.get("API_KEY")

def get_db_connection():
    """Establishes a connection to the MySQL database."""
    try:
        connection = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Error connecting to database: {err}")
        return None

def authenticate_request():
    """Authenticates the incoming request using the API key."""
    auth_header = request.headers.get('X-API-Key')  # Or request.args.get('api_key') for query parameter
    if auth_header == API_KEY:
        return True
    else:
        return False

@app.route('/ssids', methods=['POST'])
def create_ssid():
    """Handles the creation of a new SSID record."""

    if not authenticate_request():
        return jsonify({'error': 'Unauthorized'}), 401  # Unauthorized

    data = request.get_json()
    ssid = data.get('ssid')

    if not ssid:
        return jsonify({'error': 'SSID is required'}), 400

    connection = get_db_connection()
    if not connection:
        return jsonify({'error': 'Database connection failed'}), 500

    cursor = connection.cursor()
    try:
        cursor.execute("INSERT INTO ssids (ssid) VALUES (%s)", (ssid,))
        connection.commit()
        new_ssid_id = cursor.lastrowid
        cursor.close()
        connection.close()
        return jsonify({'message': 'SSID created successfully', 'id': new_ssid_id}), 201
    except mysql.connector.Error as err:
        print(f"Error inserting SSID: {err}")
        connection.rollback()
        cursor.close()
        connection.close()
        return jsonify({'error': 'Failed to create SSID'}), 500

@app.route('/ssids', methods=['GET'])
def get_ssids():
    """Retrieves all SSID records."""

    if not authenticate_request():
        return jsonify({'error': 'Unauthorized'}), 401

    connection = get_db_connection()
    if not connection:
        return jsonify({'error': 'Database connection failed'}), 500

    cursor = connection.cursor()
    try:
        cursor.execute("SELECT id, ssid, timestamp FROM ssids")
        rows = cursor.fetchall()
        cursor.close()
        connection.close()

        ssids = [{'id': row[0], 'ssid': row[1], 'timestamp': row[2]} for row in rows]
        return jsonify(ssids), 200
    except mysql.connector.Error as err:
        print(f"Error retrieving SSIDs: {err}")
        cursor.close()
        connection.close()
        return jsonify({'error': 'Failed to retrieve SSIDs'}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')