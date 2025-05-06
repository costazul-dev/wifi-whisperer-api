# WiFi SSID API

A simple RESTful API for storing and retrieving WiFi SSID information, built with Flask and MySQL, designed to run on an EC2 instance.

## Overview

This application provides a lightweight API that allows for:
- Creating new SSID records in a MySQL database
- Retrieving all stored SSID records

The API is secured with an API key authentication mechanism and uses environment variables for sensitive configuration.

## Requirements

- Python 3.6+
- Flask
- mysql-connector-python
- MySQL database server
- EC2 instance (or any server with Python support)

## Installation

1. Clone this repository to your EC2 instance:
   ```
   git clone <repository-url>
   cd wifi-ssid-api
   ```

2. Install required dependencies:
   ```
   pip install flask mysql-connector-python
   ```

3. Set up your MySQL database:
   ```sql
   CREATE DATABASE wifi_data;
   USE wifi_data;
   
   CREATE TABLE ssids (
     id INT AUTO_INCREMENT PRIMARY KEY,
     ssid VARCHAR(255) NOT NULL,
     timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
   );
   
   CREATE USER 'api_user'@'localhost' IDENTIFIED BY 'your_secure_password';
   GRANT ALL PRIVILEGES ON wifi_data.* TO 'api_user'@'localhost';
   FLUSH PRIVILEGES;
   ```

4. Set environment variables for security:
   ```
   export DB_PASSWORD="your_secure_password"
   export API_KEY="your_secret_api_key"
   ```

## Running the Application

Start the Flask application:
```
python app.py
```

The server will run on port 5000 and will be accessible from any network interface (0.0.0.0).

For production use, consider:
- Setting `debug=False` in the app.run() call
- Using a production WSGI server like Gunicorn
- Setting up a reverse proxy with Nginx or Apache

## API Endpoints

### Create a new SSID

**Endpoint:** `/ssids`  
**Method:** `POST`  
**Authentication:** API Key (X-API-Key header)  
**Content-Type:** application/json

**Request Body:**
```json
{
  "ssid": "Your WiFi Name"
}
```

**Example Request:**
```bash
curl -X POST -H "Content-Type: application/json" -H "X-API-Key: YOUR_SECRET_API_KEY" -d "{\"ssid\": \"Test SSID\"}" http://your_ec2_instance_ip:5000/ssids
```

**Successful Response (201 Created):**
```json
{
  "message": "SSID created successfully",
  "id": 1
}
```

### Get all SSIDs

**Endpoint:** `/ssids`  
**Method:** `GET`  
**Authentication:** API Key (X-API-Key header)

**Example Request:**
```bash
curl -H "X-API-Key: YOUR_SECRET_API_KEY" http://your_ec2_instance_ip:5000/ssids
```

**Successful Response (200 OK):**
```json
[
  {
    "id": 1,
    "ssid": "Test SSID",
    "timestamp": "2025-05-06T12:34:56"
  },
  {
    "id": 2,
    "ssid": "Another WiFi",
    "timestamp": "2025-05-06T13:45:23"
  }
]
```

## Security Considerations

1. **API Key Authentication**: All requests must include a valid API key in the X-API-Key header.
2. **Environment Variables**: Sensitive information like database password and API key are stored as environment variables.
3. **Error Handling**: The application includes basic error handling to prevent information leakage.

## Production Deployment Tips

For a production environment:

1. Use a proper WSGI server (Gunicorn, uWSGI) instead of the built-in Flask server
2. Set up a reverse proxy with Nginx or Apache
3. Configure SSL/TLS for secure HTTPS connections
4. Use a proper firewall to restrict access to only necessary ports
5. Set up proper logging and monitoring
6. Use a more robust authentication mechanism for production use

## Troubleshooting

If you encounter connection issues:

1. Ensure the MySQL service is running
2. Verify that the database user has proper permissions
3. Check that environment variables are set correctly
4. Make sure port 5000 is open in your security group/firewall
5. Check application logs for specific error messages