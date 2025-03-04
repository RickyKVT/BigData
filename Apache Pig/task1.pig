
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

-- filter by gold medals
filter_gold = filter join_data by medal::medal_name == 'Gold';

--returns group:chararray, filter_gold:bag
group_region = group filter_gold by noc_region::region_name;

-- count total num in each bag for each region(group)
final_filter = foreach group_region generate group as Region, COUNT(filter_gold) as Gold;

--order appropriately
final_order = order final_filter by Gold DESC, Region ASC;
store final_order into 'hdfs:///output/task1'; 