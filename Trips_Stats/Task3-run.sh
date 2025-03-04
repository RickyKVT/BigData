#!/bin/bash    
hadoop jar ./hadoop-streaming-3.1.4.jar \
-D stream.num.map.output.key.fields=2 \
-D mapred.text.key.partitioner.options=-k1,1 \
-D mapred.reduce.tasks=3 \
-file ./Task3_mapper_1.py \
-mapper ./Task3_mapper_1.py \
-file ./Task3_reducer_1.py \
-reducer ./Task3_reducer_1.py \
-input /Input/Trips.txt  /Input/Taxis.txt \
-output /Output/subTask3_1 \
-partitioner org.apache.hadoop.mapred.lib.KeyFieldBasedPartitioner

hadoop jar ./hadoop-streaming-3.1.4.jar \
-D mapred.reduce.tasks=3 \
-file ./Task3_mapper_2.py \
-mapper ./Task3_mapper_2.py \
-file ./Task3_reducer_2.py \
-reducer ./Task3_reducer_2.py \
-input /Output/subTask3_1/part* \
-output /Output/subTask3_2 

hadoop jar ./hadoop-streaming-3.1.4.jar \
-D mapred.output.key.comparator.class=org.apache.hadoop.mapred.lib.KeyFieldBasedComparator \
-D stream.num.map.output.key.fields=2 \
-D mapred.text.key.partitioner.options=-k1,1 \
-D mapred.text.key.comparator.options=-k2,2n \
-D mapred.reduce.tasks=3 \
-file ./Task3_mapper_3.py \
-mapper ./Task3_mapper_3.py \
-file ./Task3_reducer_3.py \
-reducer ./Task3_reducer_3.py \
-input /Output/subTask3_2/part* \
-output /Output/Task3 \
-partitioner org.apache.hadoop.mapred.lib.KeyFieldBasedPartitioner
