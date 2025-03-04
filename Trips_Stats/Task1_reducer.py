#!/usr/bin/env python
import sys

current_taxi = None
current_count = 0
current_max = 0
current_min = 0
current_total_fare = 0

for line in sys.stdin:
    line = line.strip()
    taxi,count,taxi_max,taxi_min,total = line.split('\t')

    #convert strings to floats
    count = int(count)
    taxi_max = float(taxi_max)
    taxi_min = float(taxi_min)
    total = float(total)
    
    #if keys are the same reduce
    if current_taxi == taxi:
        current_count +=count
        current_max = max(current_max,taxi_max)
        current_min = min(current_min,taxi_min)
        current_total_fare += total
    #print result then assign new variables
    else:
        if current_taxi:
            print('%s\t%s\t%.2f\t%.2f\t%.2f' % (current_taxi,current_count,current_max,current_min,current_total_fare / current_count))
        current_count = count
        current_taxi = taxi
        current_max = taxi_max
        current_min = taxi_min
        current_total_fare = total
#print final result
if current_taxi == taxi:
    print('%s\t%s\t%.2f\t%.2f\t%.2f' % (current_taxi,current_count,current_max,current_min,current_total_fare/current_count))
    