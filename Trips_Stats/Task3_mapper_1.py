#!/usr/bin/env python
import sys
for line in sys.stdin:
    taxi = '-'
    company = '-'
    trip = '-'

    line = line.strip()
    parts = line.split(',')
    if len(parts) == 4: #company record (taxi#, -, company)
        taxi = parts[0]
        company = parts[1]
    elif len(parts) == 8: # trip record( taxi#, 1, -)
        taxi = parts[1]
        trip = 1
    print('%s\t%s\t%s' % (taxi, trip, company))