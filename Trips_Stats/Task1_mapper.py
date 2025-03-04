#!/usr/bin/env python
import sys
mylist = []
for line in sys.stdin:
    line = line.strip() #remove leading and trailing whitespaces
    trip = line.split(",") #split the line into words and returns as a list
    # assign required variables
    taxi_num = trip[1]
    fare = trip[2]
    distance_string =None
    distance = float(trip[3])
    #classification of trip
    if distance >= 200:
        distance_string = 'long'
    elif (distance >= 100) and (distance < 200):
        distance_string = 'medium'
    else:
        distance_string = 'short'
    #key= taxi# + trip type - 435_long
    key = str(taxi_num) + '_' + distance_string
    flag = False
    i = 0
    #key_pair value = [key, sum_of_trips, max_fare, min_fare, average fare]
    for trip in mylist:
        item = trip.split(',')
        k = item[0]
        if k == key: # check if key already exist
            #in mapper combiner
            total_trip = int(item[1]) + 1
            max_fare = max(fare,float(item[2]))
            min_fare = min(fare,float(item[3]))
            total_fare = float(item[4]) + float(fare)
            mylist[i] = k + "," + str(total_trip) + "," + str(max_fare) + "," + str(min_fare) + "," + str(total_fare)
            flag = True
            break
        i +=1
    if not flag:
        mylist.append(key +"," + "1" + "," + str(fare) + "," + str(fare) + ","+ str(fare))

#print in mapper combining list        
for x in mylist:
    item = x.split(",")
    print('%s\t%s\t%s\t%s\t%s' % (item[0],item[1],item[2],item[3],item[4]))
