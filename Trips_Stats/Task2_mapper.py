#!/usr/bin/env python

import sys
from math import sqrt

# get initial medoids from a txt file and add them in an array
def getMedoids(filepath):
    medoids = []

    with open(filepath) as fp:
        line = fp.readline()
        while line:
            if line:
                try: #for first iteration as first line is number of iteration and not a medoid
                    line = line.strip()
                    cord = line.split('\t')
                    medoids.append([float(cord[0]), float(cord[1])])
                except:# read next line
                    line = fp.readline()
                    continue
            else:
                break
            line = fp.readline()

    fp.close()
    return medoids


def createClusters(medoids):
    for line in sys.stdin:
        line = line.strip().split(",")

        x_cord = line[-1]
        y_cord = line[-2]
        min_dist = 100000000000000
        index = -1

        for medoid in medoids:
            try:
                x_cord = float(x_cord)
                y_cord = float(y_cord)
            except ValueError:
                # float was not a number, so silently
                # ignore/discard this line
                continue

            # euclidian distance from every point of dataset
            # to every medoid
            cur_dist = sqrt(pow(x_cord - medoid[0], 2) + pow(y_cord - medoid[1], 2))

            # find the medoid which is closer to the point
            if cur_dist <= min_dist:
                min_dist = cur_dist
                index = medoids.index(medoid)
                
        print('%s\t%s\t%s' % (medoids[index], x_cord, y_cord))


if __name__ == "__main__":
    medoids = getMedoids('initialization.txt')
    createClusters(medoids)
    