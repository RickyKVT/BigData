#!/bin/bash    
hadoop jar ./hadoop-streaming-3.1.4.jar \
-D mapred.reduce.tasks=3 \
-file ./Task1_mapper.py \
-mapper ./Task1_mapper.py \
-file ./Task1_reducer.py \
-reducer ./Task1_reducer.py \
-input /Input/Trips.txt \
-output /Output/Task1







