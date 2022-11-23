# Data_Mining_F22
## Group Members
- Yang Liu
- You Xu
- Tianheng Zhou

## ArdGIS Online data
https://services6.arcgis.com/OO2s4OoyCZkYJ6oE/arcgis/rest/services/2109_STIB_MIVB_Network/FeatureServer

## Work Plan
### Schedule Example
- line 25 at ULB, 08/23-27
- Punctuality: count: <= 5
- Regularity: count: >= 6

### Puncturality
- Option 1: track train timetable. Assmption1: total number of car match; 2: we can identify each car at each station. tram/metro/bus
- Option 2: only consider station/stop
- Standard: +-30s

### Regularity
- Formula
- Find schedule waiting
- Calculate actural waiting time
- EWT

### Big Delay
- Based on station

- From schedule, get peak/off-peak hours -> Punctuality/Regularity
- Punctuality per line, stop, date

## Data
- Static locations for all stops and lines
- Schedules
- Car location per 30s: direction, last stop, distance from last stop

# Problems
- Time +2hrs?
- Duplicate train/bus?
- Missing train/bus?
- Stop ID?

# Notes from lecture
- Estimate arrival time by speed and distance from the map
- Transform schedule time for clustering, and do models like DB Scan
- No report, presentation and a brief description
