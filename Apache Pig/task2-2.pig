-- register udf
Register 'task2udf.py' using streaming_python as myfuncs;

-- Load in files
noc_region = load 'hdfs:///input/noc_region.csv' using PigStorage(',') as (id:int, noc:chararray, region_name:chararray);
person_region = load 'hdfs:///input/person_region.csv' using PigStorage(',') as (person_id:int, region_id:int);
person = load 'hdfs:///input/person.csv' using PigStorage(',') as (id:int, name:chararray, gender:chararray, height:int, weight:int);
competitor_event = load 'hdfs:///input/competitor_event.csv' using PigStorage(',') as (event_id:int, competitor_id:int, medal_id:int);
medal = load 'hdfs:///input/medal.csv' using PigStorage(',') as (id:int, medal_name:chararray);

-- join data
join_data = join noc_region by id, person_region by region_id;
join_data = join join_data by person_region::person_id, person by id;
join_data = join join_data by person_region::person_id, competitor_event by competitor_id;
join_data = join join_data by competitor_event::medal_id, medal by id;

-- filter gold 
filter_gold = filter join_data by medal::medal_name == 'Gold';

-- filter silver
filter_silver = filter join_data by medal::medal_name == 'Silver';

-- group each filter medal
group_region_gold = group filter_gold by noc_region::region_name;
group_region_silver  = group filter_silver by noc_region::region_name;

-- count total num in each bag for each region(group)
final_filter_gold = foreach group_region_gold generate group as Region, COUNT(filter_gold) as Gold;
final_filter_silver = foreach group_region_silver generate group as Region, COUNT(filter_silver) as Silver;

-- join the two tables into one final table
join_medal = join final_filter_gold by Region left, final_filter_silver by Region;

-- generate format
final_output = foreach join_medal generate final_filter_gold::Region, final_filter_gold::Gold, myfuncs.fill_silver_na(final_filter_silver::Silver);

-- order the final medal count
final_order = order final_output by Gold DESC, Silver DESC ,Region ASC;
store final_order into 'hdfs:///output/task2-2'; 