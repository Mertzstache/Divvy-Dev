#!/usr/bin/env/python
# -*- coding: utf-8 -*-
"""utilities and common io scripts"""
from collections import Counter
import pickle

ROUND_TO_NEAREST = 300
IN_COMMON = 10

def readdict(filename):
    """reads in the csv with labels in first row"""
    rows = []
    with open(filename, mode='r', encoding='utf-8-sig') as csvfile:
        # print(csvfile.readline().replace('\n','').replace('\"','').split)
        labels = csvfile.readline().replace('\n','').replace('\"','').split(',')
        # labels = [ l for l in labels if l not in ('start_time', 'stop_time', 'from_station_name', 'to_station_name')]
        for row in csvfile:
            members = {}
            row = row.replace('\n','').replace('\"','').split(',')
            for idx, lbl in enumerate(labels):
                if lbl not in  ('trip_id', 'start_time', 'end_time', 'from_station_name', 'from_station_id', 'to_station_id', 'to_station_name', 'bikeid'):
                    members[lbl] = str(row[idx])
            rows.append(members)
    return rows

def get_attribute(data, attribute_name, trans=str):
    """returns values of attribute for all rows in table
    data = data to be evaluated
    attribute_name = name of the attribute to be extracted
    trans = transformation to perform on the data, such as int, default is set to string"""
    return [trans(a[attribute_name]) for a in data if a[attribute_name] != '']

def data_cleanup_missing(data):
    """cleans data up by removing entries that are missing data"""
    entries = []
    for entry in data:
        if '' in entry.values():
            for key in entry:
                entry[key] = 'Not Available' if entry[key] == '' else entry[key]
        entries.append(entry)
    return entries#[entry for entry in data if '' not in entry.values()]

def data_cleanup_enumerate_and_group(data):
    """manual cleanup and enumeration"""
    print(data[0].keys())
    for entry in data:
        entry['tripduration'] = round_down(int(entry['tripduration']), ROUND_TO_NEAREST)
        entry['tripduration'] = 9930 if entry['tripduration'] > 9930 else entry['tripduration']
        # entry['gender'] = entry['gender'] if entry['gender'] == 'Not Available' else en
        # entry['usertype'] = 1 if entry['usertype'] == 'Subscriber' else 0
        # if entry['birthyear'] == '':
            # print("ERROR: " + entry)
        # entry['birthyear'] = '1950' if int(entry['birthyear']) < 1950 else entry['birthyear']

def round_down(num, divisor):
    """simple round down function"""
    return num - (num%divisor)

def get_frequency_dictionaries(data, labels):
    """gets the frequency dictionaries of all teh data in data, labels can be data[0].keys()"""
    dictionaries = {}
    counters = {}
    for label in labels:
        dictionaries[label] = {}
        counters[label] = []
    for entry in data:
        for label in labels:
            counters[label].append(entry[label])
            if entry[label] in dictionaries[label].keys():
                dictionaries[label][entry[label]] += 1
            else:
                dictionaries[label][entry[label]] = 1

    in_common = counting(counters)

    return dictionaries, in_common

def counting(ctrs):
    """getting counters going"""
    in_common = {}
    for ctr in ctrs:
        common = Counter(ctrs[ctr])
        in_common[ctr] = common.most_common(IN_COMMON)
    return in_common

def filter(attribute, value):
    return []
    

def save_obj(obj, name ):
    with open('obj/'+ name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)
def load_obj(name ):
    with open('obj/' + name + '.pkl', 'rb') as f:
        return pickle.load(f)

def standard_procedures(fn):
    data = readdict(fn)
    data = data_cleanup_missing(data)
    data_cleanup_enumerate_and_group(data)
    return get_frequency_dictionaries(data, data[0].keys())
