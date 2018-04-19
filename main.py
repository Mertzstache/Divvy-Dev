#!/usr/bin/env/python
# -*- coding: utf-8 -*-
"""main file to be run"""

#****************************************
# main.py
# run like:
# $main.py <optional filename>
#****************************************

import sys
import pprint
from util import readdict, data_cleanup_missing, data_cleanup_enumerate_and_group, get_frequency_dictionaries

def main():
    """main function"""
    names = ["Divvy_Stations_2017_Q3Q4.csv", "Divvy_Trips_2017_Q3.csv", "Divvy_Trips_2017_Q4.csv"]
    directory = "Divvy_Trips_2017_Q3Q4/"
    fn = names[int(sys.argv[1])] if len(sys.argv) > 1 else "first300.csv"
    fn = directory + fn
    print("doing operations on " + fn)
    data = readdict(fn)

    data = data_cleanup_missing(data)
    data_cleanup_enumerate_and_group(data)

    dictionary, most_common = get_frequency_dictionaries(data, data[0].keys())

    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(most_common)

if __name__ == "__main__":
    main()
