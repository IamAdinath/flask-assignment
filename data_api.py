
from flask import Blueprint, jsonify, current_app, request, render_template, url_for
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

@api_blueprint.route('/post-data', methods=['POST', 'GET'])
def post_data():
    try:
        if request.method == 'GET':
            return render_template('post_data.html')
        else:
            influx_client = create_client(current_app)
            data = request.form.to_dict()
            data_points = [
                {
                    "measurement": "test_measurement2",
                    "tags": {
                        "Job Profile": data["job_profile"],
                    },
                    "Application Timestamp": datetime.now().strftime("%m/%d/%Y, %H:%M:%S"),
                    "fields": {
                        "Name": data["name"],
                        "Experience": data["experience"],
                        "Skills": data["skills"],
                        "Role": data["role"],
                        "Salary": data["salary"],
                        "Location": data["location"],
                        "email": data["email"],
                    }
                }
            ]

            influx_client.write_points(data_points)
            influx_client.close()
            return jsonify({"message":  "Data posted successfully!"})
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