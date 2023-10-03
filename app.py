from flask import Flask
from data_api import api_blueprint  # Import the data blueprint

# Create the Flask app
app = Flask(__name__)

# Configuration for InfluxDB (replace with your own values)
app.config['INFLUXDB_HOST'] = 'localhost'
app.config['INFLUXDB_PORT'] = 8086  # Replace with your InfluxDB port
app.config['INFLUXDB_DATABASE'] = 'bulk_data'
app.config['INFLUXDB_USERNAME'] = 'admin'
app.config['INFLUXDB_PASSWORD'] = 'admin'

# Register the data blueprint with "/api" as the URL prefix
app.register_blueprint(api_blueprint, url_prefix='/api')

if __name__ == '__main__':
    app.run(debug=True)
