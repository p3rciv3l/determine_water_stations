from flask import Flask, render_template, request
import gpxpy
from gpx_parser import GPXRoute

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_gpx():
    file = request.files['gpxfile']
    mile = float(request.form['mile'])
    
    # Parse GPX file
    gpx_data = gpxpy.parse(file)
    gpx_route = GPXRoute(gpx_data)
    
    # Get coordinate at specified mile
    result = gpx_route.get_coordinate_at_mile(mile)
    
    if isinstance(result, tuple):
        lat, lon = result
        return f"The coordinate at mile {mile} is: Latitude {lat}, Longitude {lon}"
    else:
        return result  # Error message

if __name__ == '__main__':
    app.run(debug=True)
