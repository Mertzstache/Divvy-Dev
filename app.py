from flask import Flask, render_template
from flask_googlemaps import GoogleMaps, Map#, BicyclingLayer
from util import readdict, get_attribute

app = Flask(__name__, template_folder=".")
KEY = "AIzaSyAscj7Ns0L3oSRzaC5tEHzY91uT0vQkkCI"
# # you can set key as config
# app.config['GOOGLEMAPS_KEY'] = key

# # Initialize the extension
# GoogleMaps(app)

# you can also pass the key here if you prefer
GoogleMaps(app, key=KEY)

@app.route("/")
def mapview():
    # creating a map in the view
    fn = "Divvy_Trips_2017_Q3Q4/Divvy_Stations_2017_Q3Q4.csv"
    data = readdict(fn)
    lat = get_attribute(data, "latitude", float)
    lon = get_attribute(data, "longitude", float)
    names = get_attribute(data, "name")
    stations = []
    for idx, l in enumerate(lat):
        stations.append((lat[idx], lon[idx], names[idx], "https://maps.gstatic.com/intl/en_us/mapfiles/markers2/measle_blue.png"))
    stations = stations
    mymap = Map(
        identifier="view-side",
        lat=41.8781,
        lng=-87.6298,
        markers=stations,
        fit_markers_to_bounds=True,
        style="height:500px;width:100%;"
    )
    # bikeLayer = GoogleMaps.BicyclingLayer
    # BicyclingLayer.setMap(mymap)
    
    return render_template('example.html', mymap=mymap, stations=stations)
# mkers = [(37.4419, -122.1419), (37.4300, -122.1400)]


if __name__ == "__main__":
    app.run(debug=True)
