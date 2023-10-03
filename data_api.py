# data_api.py

# Import necessary dependencies
from flask import Blueprint, jsonify, current_app
from influxdb import InfluxDBClient

# Create a Blueprint object for the data module
api_blueprint = Blueprint('data', __name__)

@api_blueprint.route('/bulk-data', methods=['GET'])
def get_bulk_data():
    try:
        # Connect to the InfluxDB database (replace with your own database configuration)
        influx_client = InfluxDBClient(
            username=current_app.config['INFLUXDB_USERNAME'],
            password=current_app.config['INFLUXDB_PASSWORD'],
            host=current_app.config['INFLUXDB_HOST'],
            port=current_app.config['INFLUXDB_PORT'],
            database=current_app.config['INFLUXDB_DATABASE']
        )

        # Query the database to retrieve bulk data (replace with your own query)
        query = 'SELECT * FROM your_measurement_name LIMIT 100'
        result = influx_client.query(query)

        # Process the query result as needed (e.g., converting to a list of dictionaries)
        data = list(result.get_points())

        # Close the InfluxDB connection
        influx_client.close()

        # Return the data as a JSON response
        return jsonify({'data': data})

    except Exception as e:
        return jsonify({'error': str(e)}), 500
