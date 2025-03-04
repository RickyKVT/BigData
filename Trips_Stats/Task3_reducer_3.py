#!/usr/bin/env python
import sys
for line in sys.stdin:
    parts= line.split("\t")
    print('%s\t%s' % (parts[0], parts[1]))