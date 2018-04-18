#!/usr/bin/env/python
# -*- coding: utf-8 -*-
"""main file to be run"""

#****************************************
# main.py
# run like:
# $main.py <optional filename>
#****************************************


import pprint
from util import readdict
from metrics import get_trip_durations


def main():
    """main function"""
    directory = "Divvy_Trips_2017_Q3Q4/"
    # stations = readdict(directory + "Divvy_Stations_2017_Q3Q4.csv")
    # Q3_data = readdict(directory + "Divvy_Trips_2017_Q3.csv")
    # Q4_data = readdict(directory + "Divvy_Trips_2017_Q4.csv")
    first_data = readdict(directory + "first300.csv")
    # print(get_avg_trip_duration(Q4_data))

if __name__ == "__main__":
    main()
