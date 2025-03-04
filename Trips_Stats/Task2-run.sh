#!/bin/bash
#read first line in text file and set as number of iterations
v=$(head -n 1 initialization.txt)
for ((i=1; i<=$v; i++))
do
    #remove output directory for every iteration after the first
    #if already exist code will crash
    hadoop fs -rm -r -f /Output/Task2

    hadoop jar ./hadoop-streaming-3.1.4.jar \
    -D mapred.reduce.tasks=3 \
    -D mapred.text.key.partitioner.options=-k1 \
    -file initialization.txt \
    -file ./Task2_mapper.py \
    -mapper ./Task2_mapper.py \
    -file ./Task2_reducer.py \
    -reducer ./Task2_reducer.py \
    -input /Input/Trips.txt \
    -output /Output/Task2 \
    -partitioner org.apache.hadoop.mapred.lib.KeyFieldBasedPartitioner

    rm -f initialization1.txt
    hadoop fs -cat /Output/Task2/part* > initialization1.txt
    seeiftrue=`python reader.py`
    if [ $seeiftrue = 1 ] # check if two medoid files are the same
    then
        #break out of loop if medoids converge
        break
    else
        #assign new medoids as initialization.txt
        hadoop fs -rm -f initialization.txt
        hadoop fs -cat /Output/Task2/part*  > initialization.txt
        
    fi
done
