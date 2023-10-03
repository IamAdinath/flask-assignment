
from flask import Blueprint, jsonify, current_app, request
from influxdb import InfluxDBClient
from datetime import datetime
# Create a Blueprint object for the data module
api_blueprint = Blueprint('data', __name__)

@api_blueprint.route('/bulk-data', methods=['GET'])
def get_bulk_data():
    """
    Fetch the data from  table and return as a response in get method.
    """
    try:
        influx_client = create_client(current_app)
        result = influx_client.query('SELECT * FROM test_measurement2 LIMIT 100')
        data = list(result.get_points())
        influx_client.close()
        return jsonify(data)

    except Exception as e:
        return jsonify({'error': str(e)})

@api_blueprint.route('/post-data', methods=['GET'])
def post_data():
    try:
        influx_client = create_client(current_app)
        # data = request.get_json()  # Assuming data is posted as JSON

        # Prepare data points
        data_points = [
            {
                "measurement": "test_measurement2",
                "tags": {
                    "Job Profile": "Backend Developer",
                },
                "Application Timestamp": datetime.now().strftime("%m/%d/%Y, %H:%M:%S"),
                "fields": {
                    "Name": "John Doe",
                    "Experience": "3",
                    "Skills": "Python, Java, C#",
                    "Role": "Software Engineer",
                    "Salary": "100000",
                    "Location": "New York, USA",
                    "email": "XXXXXXXXXXXXXXXXXXX"
                }
            }
        ]

        influx_client.write_points(data_points)
        influx_client.close()
        return "Data posted successfully."

    except Exception as e:
        return f"Error: {str(e)}"

def create_client(current_app):
    influx_client = InfluxDBClient(
        username=current_app.config['INFLUXDB_USERNAME'],
        password=current_app.config['INFLUXDB_PASSWORD'],
        host=current_app.config['INFLUXDB_HOST'],
        port=current_app.config['INFLUXDB_PORT'],
        database=current_app.config['INFLUXDB_DATABASE']
    )
    return influx_client