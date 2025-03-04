#!/usr/bin/env python
import sys
last_company = None
count_trip = 0
for line in sys.stdin:
    # there are some cases where there is an empty line
    try:
        line = line.strip()
        parts = line.split("\t")
        company = parts[0]
        trip = parts[1]
        if not last_company: # if this is first iteration
            last_company = company
            count_trip = 1
        elif company == last_company:
            count_trip +=1
        else:
            print('%s\t%s' % (company, count_trip))
            last_company = company
            count_trip = 1
    except:
        continue
print('%s\t%s' % (company, count_trip))

