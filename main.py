#!/usr/bin/env/python
# -*- coding: utf-8 -*-
"""main file to be run"""

#****************************************
# main.py
# run like:
# $main.py <optional filename idx>
#****************************************

import sys
import pprint
from util import standard_procedures, get_risky_stations
from util import save_obj, readdict, data_cleanup_missing
def main():
    """main function"""
    names = ["Divvy_Stations_2017_Q3Q4.csv", "Divvy_Trips_2017_Q3.csv", "Divvy_Trips_2017_Q4.csv", "Divvy_Trips.csv", "6_26_6_30.csv", "Divvy_Stations_2017_Q1Q2.csv"]
    directory = "Divvy_Data/"
    fn = names[int(sys.argv[1])] if len(sys.argv) > 1 else "first300.csv"
    fn = directory + fn
    print("doing operations on " + fn)
    data = readdict(fn)
    # data = data_cleanup_missing(data)
    save_obj(data, "full_array_of_entries")

    # dictionary, most_common = standard_procedures(fn)
    # most_common, totals = get_risky_stations(fn)
    # pp = pprint.PrettyPrinter(indent=4)
    # pp.pprint(most_common)
    # save_obj(most_common, "station_counter")
    # save_obj(totals, "totals")

if __name__ == "__main__":
    main()
