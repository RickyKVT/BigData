#!/usr/bin/env python
import sys
for line in sys.stdin:
    if not line:
        continue
    line = line.replace("\n","")
    line.strip()
    company, trip = line.split("\t")
    print('%s\t%s' % (company, trip))