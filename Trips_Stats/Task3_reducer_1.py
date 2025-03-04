#!/usr/bin/env python
import sys
last_taxi = None
current_company = '-'
for line in sys.stdin:
    line = line.strip()
    taxi, trip, company = line.split('\t')
    #set key as a new taxi and different taxi
    if not last_taxi or last_taxi != taxi:
        last_taxi = taxi
        current_company = company
    elif taxi == last_taxi:
        company = current_company
        print('%s\t%s' % (company, trip))
