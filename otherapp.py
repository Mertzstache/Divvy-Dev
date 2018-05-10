from flask import Flask, render_template, json
from flask_googlemaps import GoogleMaps, Map
from util import readdict, get_attribute, data_cleanup_missing, get_frequency_dictionaries, load_obj, standard_procedures

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
    otherfn = "Divvy_Trips_2017_Q3Q4/Divvy_Trips_2017_Q3.csv"
    data = readdict(fn)
    # other_data = readdict(otherfn)
    # other_data = data_cleanup_missing(other_data)
    # frequency_dictionary, most_common = get_frequency_dictionaries(other_data, other_data[0].keys())
    # print(frequency_dictionary['gender'])

    frequency_dictionary = load_obj('frequency_dictionary')
    # frequency_dictionary, most_common = standard_procedures(otherfn)

    lat = get_attribute(data, "latitude", float)
    lon = get_attribute(data, "longitude", float)
    names = get_attribute(data, "name")
    stations = []
    stations2 = []
    for idx, l in enumerate(lat):
        stations.append((lat[idx], lon[idx], names[idx], "https://maps.gstatic.com/intl/en_us/mapfiles/markers2/measle_blue.png"))
        stations2.append({"lat": lat[idx], "lng":lon[idx], "name": names[idx], "img": "https://maps.gstatic.com/intl/en_us/mapfiles/markers2/measle_blue.png"})

    mymap = Map(
        scale=2,
        identifier="view-side",
        lat=41.8781,
        lng=-87.6298,
        markers=stations,
        fit_markers_to_bounds=True,
        style="height:500px;width:100%;"
    )
    # bikeLayer = GoogleMaps.BicyclingLayer
    # BicyclingLayer.setMap(mymap)
    stations2 = json.dumps(stations2)
    # stations2 = stations2.replace("\"","")
    # print(stations2)

    # stations2 = json.loads(stations2)
    # print(stations2)

    # print(stations)
    
    return render_template('example.html', mymap=mymap, json_stations=stations2, frequencies=json.dumps(frequency_dictionary))
# mkers = [(37.4419, -122.1419), (37.4300, -122.1400)]


if __name__ == "__main__":
    app.run(debug=True)
