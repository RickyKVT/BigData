#!/usr/bin/env python
import sys
for line in sys.stdin:
    line.strip()
    company, trip = line.split("\t")
    print('%s\t%s' % (company, trip))
