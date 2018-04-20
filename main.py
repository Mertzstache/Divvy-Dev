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
from util import standard_procedures
from util import save_obj
def main():
    """main function"""
    names = ["Divvy_Stations_2017_Q3Q4.csv", "Divvy_Trips_2017_Q3.csv", "Divvy_Trips_2017_Q4.csv"]
    directory = "Divvy_Trips_2017_Q3Q4/"
    fn = names[int(sys.argv[1])] if len(sys.argv) > 1 else "first300.csv"
    fn = directory + fn
    print("doing operations on " + fn)

    dictionary, most_common = standard_procedures(fn)

    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(most_common)
    save_obj(dictionary, "frequency_dictionary")

if __name__ == "__main__":
    main()
