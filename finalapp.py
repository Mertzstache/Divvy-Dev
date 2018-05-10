from flask import Flask, render_template, json, request
from flask_googlemaps import GoogleMaps, Map
from util import load_obj, get_attribute
from simulator import *
app = Flask(__name__, template_folder="templates")
# KEY = "AIzaSyAscj7Ns0L3oSRzaC5tEHzY91uT0vQkkCI"
# # you can set key as config
# app.config['GOOGLEMAPS_KEY'] = key

# # Initialize the extension
# GoogleMaps(app)

# you can also pass the key here if you prefer

columns = [
{
    "field": "id", # which is the field's name of data key 
    "title": "id", # display as the table header's name
    "sortable": True,
  },
  {
    "field": "name", # which is the field's name of data key 
    "title": "name", # display as the table header's name
    "sortable": True,
  },
  {
    "field": "dpcapacity",
    "title": "Maximum Capacity",
    "sortable": True,
  },
  {
    "field": "current_number_of_bikes",
    "title": "Current Number of Bikes",
    "sortable": True,
  },
  {
    "field": "over_capacity",
    "title": "Over Capacity",
    "sortable": True,
  },
    {
    "field": "out_of_bikes",
    "title": "Out of Bikes",
    "sortable": True,
  }
]




@app.route('/update_time', methods = ['POST', 'GET'])
def update_time():
    global start_times, end_times, stns, curr_time, end_time
    if request.method == 'POST':
        print(len(start_times))
        result = request.form
        value = result['expression']
        advance_time(curr_time, int(value)*60)
        if greater_than(end_time, curr_time):
            start_times, end_times = update_stations(curr_time, stns, start_times, end_times)
            bad_stations = check_for_errors(stns)
        else:
            curr_time = [24, 00, 00]
            start_times, end_times = update_stations(curr_time, stns, start_times, end_times)
            bad_stations = check_for_errors(stns)
    return render_template('map_and_table.html', columns=columns, json_stations=stations2, data=bad_stations, curr_time=parse_time(curr_time), formfill=value)

# @app.route('/add_data',methods = ['POST', 'GET'])
# def add_data():
#    if request.method == 'POST':
#       result = request.form
#       value = result['expression']

#       url = "https://genius.com/"
#       for word in value.split(' '):
#         url+= word+"-"
#       url += "lyrics"
#       print(url)
#       scraped = scrape(url)
#       return render_template('map_and_table.html',result=scraped)



@app.route("/")
def mapview():
    global start_times, end_times, stns, curr_time, end_time, stations2
    stns = load_obj("stationsq1q2")
    data = load_obj("4day")

    day = 27
    start_times, end_times = initialize_start_end(data, day)

    print(len(start_times))
    lat = get_attribute(stns, "latitude", float)
    lon = get_attribute(stns, "longitude", float)
    names = get_attribute(stns, "name")
    identity = get_attribute(stns, "id", int)

    stations2 = []
    for idx, l in enumerate(lat):
        stations2.append({"lat": lat[idx], "lng":lon[idx], "name": names[idx], "img": "https://maps.gstatic.com/intl/en_us/mapfiles/markers2/measle_blue.png", "id": identity[idx]})

    stations2 = json.dumps(stations2)

    stns = transform(stns)
    initialize_stations(stns)
    stationsother = [stns[key] for key in stns]
    print(stations2)
    curr_time = [int(i) for i in "00:00:00".split(":")]
    end_time = [int(i) for i in "24:00:00".split(":")]


    return render_template('map_and_table.html', columns=columns, json_stations=stations2, data=stationsother, curr_time=parse_time(curr_time), formfill="60")

def parse_time(time):
    return ':'.join([str("%02d" % (t,)) for t in time])[:-3]
if __name__ == "__main__":
    app.run(debug=True)
