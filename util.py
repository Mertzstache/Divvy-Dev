#!/usr/bin/env/python
# -*- coding: utf-8 -*-
"""utilities and common io scripts"""

def readdict(filename):
    """reads in the csv with labels in first row"""
    rows = []
    with open(filename) as csvfile:
        labels = csvfile.readline().replace('\n','').split(',')
        print(labels)
        for row in csvfile:
            members = {}
            row = row.replace('\n','').split(',')
            for idx, lbl in enumerate(labels):
                members[lbl] = row[idx]
            rows.append(members)
    return rows
