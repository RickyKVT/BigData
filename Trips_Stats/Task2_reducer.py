#!/usr/bin/env python

import sys
from collections import defaultdict
from math import sqrt

#dict of key,value, where key is medoid coordinates and value is points
#associated with medoid
def medoid_listing():
    for line in sys.stdin:
        try:
            line.replace('\\n',"")
            medoid, x, y = line.strip().split("\t")
            medoid_x, medoid_y = medoid.strip("[]'").split(",")
            medoid_y = medoid_y.replace(" ","")
            mytuple = (medoid_x,medoid_y)
        except:
            continue
        medoid_list[mytuple].append((x,y))

        


def calculateNewMedoids(medoid_list):
    new_medoid_list = []
    best_medoid = None
    best_cost = 0.0
    previous_medoid = None
    for medoid, points in medoid_list.items():
        # find initial cost with initial medoid and set it as the best cost and best medoid
        for point in points:
            try:
                best_cost += sqrt((float(medoid[0]) - float(point[0]))**2 + (float(medoid[1]) - float(point[1]))**2)
                best_medoid = medoid
                
            except:
                continue
        

        #find new cost with a different medoid
        for new_medoid in points:
            #check if previous medoid == current one as cost would be the same
            if new_medoid == previous_medoid:
                continue
            new_cost = 0.0
            # for every point associated with a medoid calcuate total cost
            for point in points:
                new_cost += sqrt((float(new_medoid[0]) - float(point[0]))**2 + (float(new_medoid[1]) - float(point[1]))**2)
            
            # swap medoid and cost if new medoid is better
            if new_cost < best_cost:
                best_cost = new_cost
                best_medoid = new_medoid
            previous_medoid = new_medoid
        # append best medoid to list
        new_medoid_list.append((best_medoid[0],best_medoid[1]))
    return new_medoid_list # list of new medoids with lowest cost

        

            



if __name__ == "__main__":
    medoid_list = defaultdict(list)
    medoid_listing()
    new_medoid = calculateNewMedoids(medoid_list)
    # final output
    for medoid in new_medoid:
        print('%s\t%s' % (medoid[0], medoid[1]))
    
