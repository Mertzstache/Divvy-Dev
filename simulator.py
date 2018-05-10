#!/usr/bin/env/python
# -*- coding: utf-8 -*-
"""simulator file that identifies overloaded stations"""

#****************************************
# simulator.py
# run like:
# $python3 simulator.py
#****************************************
# import ipdb
import pprint
# from util import standard_procedures, get_risky_stations
from util import load_obj#, readdict, data_cleanup_missing
def main():
    day = 27#input("What day do you want to simulate?")
    verbose = 0#input("Verbose? (to see all stations 1, to just see overloaded ones 0)")
    
    data = load_obj("4day")
    start_times, end_times = initialize_start_end(data, day)
    stations = load_obj("stationsq1q2")
    stations = transform(stations)
    initialize_stations(stations)
    
    # pp = pprint.PrettyPrinter(indent=4)
    # pp.pprint(stations)
    # pp.pprint(end_times)
    curr_time = [int(i) for i in "00:00:00".split(":")]
    end_time = [int(i) for i in "24:00:00".split(":")]

    while greater_than(end_time, curr_time):
        # ipdb.set_trace(context=5)
        advance_time(curr_time, 60*5)
        start_times, end_times = update_stations(curr_time, stations, start_times, end_times)
        bad_stations = check_for_errors(stations)
        pp = pprint.PrettyPrinter(indent=4)
        # if verbose == 1 and bad_stations:
        #     pp.pprint(stations)
        # if verbose == 0 and bad_stations:
        #     pp.pprint(bad_stations)
        #     input()
    pp.pprint(bad_stations)

def transform(stations):
    transformed_stations = {}
    for station in stations:
        # new_station = {}
        # for s in station.keys():
        #     if s == "dpcapacity":
        #         new_station[s] = station[s]
        transformed_stations[station['id']] = {'id': int(station['id']), 'dpcapacity': int(station['dpcapacity']), 'name': station['name']}#new_station
    return transformed_stations

def initialize_stations(stations):
    for station in stations:
        stations[station]['current_number_of_bikes'] = (stations[station]['dpcapacity'])//2
        stations[station]['over_capacity'] = False
        stations[station]['out_of_bikes'] = False

def initialize_start_end(data, day):
    start_times = []
    end_times = []
    for entry in data:
        if int(entry['start_time'][2:4]) == int(day):
            start_times.append(([int(i) for i in entry['start_time'][-8:].split(":")], entry['from_station_id']))
            end_times.append(([int(i) for i in entry['end_time'][-8:].split(":")], entry['to_station_id']))
    start_times.reverse()
    end_times.sort()
    return start_times, end_times

def advance_time(current_time, seconds_to_advance):
    # curr_hours = int(current_time[:2])*60*60 
    # curr_minutes = int(current_time[3:5])*60
    # curr_seconds = int(current_time[-2:])    
    current_time[2] += seconds_to_advance
    current_time[1] += current_time[2]//60
    current_time[2] %= 60
    current_time[0] += current_time[1]//60
    current_time[1] %= 60

    # return str(curr_hours) + ":" + str(curr_minutes) + ":" + str(curr_seconds)

def greater_than(time1, time2):
    # print(time2[:2])
    # seconds1 = int(time1[:2])*60*60 + int(time1[3:5])*60 + int(time1[-2:])
    # seconds2 = int(time2[:2])*60*60 + int(time2[3:5])*60 + int(time2[-2:])
    seconds1 = sum([t*60**(2-i) for i, t in enumerate(time1)])
    seconds2 = sum([t*60**(2-i) for i, t in enumerate(time2)])
    return seconds1 > seconds2


def update_stations(curr_time, stations, start_times, end_times):
    new_start_times = []
    new_end_times = []
    for idx, s in enumerate(start_times):
        if greater_than(s[0], curr_time):
            for key in [k[1] for k in start_times[:idx-1]]:
                stations[key]['current_number_of_bikes'] -= 1
            new_start_times = start_times[idx-1:]
            break
    for idx, e in enumerate(end_times):
        if greater_than(e[0], curr_time):
            for key in [k[1] for k in end_times[:idx-1]]:
                stations[key]['current_number_of_bikes'] += 1
            new_end_times = end_times[idx-1:]
            break

    for key in stations:
        stations[key]['over_capacity'] = stations[key]['current_number_of_bikes'] > stations[key]['dpcapacity']
        stations[key]['out_of_bikes'] = stations[key]['current_number_of_bikes'] < 0

    return new_start_times, new_end_times


def check_for_errors(stations):
    bad_stations = []
    for key in stations:
        if stations[key]['over_capacity'] or stations[key]['out_of_bikes']:
            bad_stations.append(stations[key])
    return bad_stations

if __name__ == "__main__":
    main()
