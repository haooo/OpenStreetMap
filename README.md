
# Project 3: OpenStreetMap Data Wrangling with SQL

Name: Hao Lan

Map Area: I have choosen Phoenix Arizona because I've been spending my summer vacation there, and I really like the city.

* Location: Phoenix Arizona, USA
* [MapZen URL](https://mapzen.com/data/metro-extracts/)

## 1. Data Audit

Unique Tags Looking at the XML file, I found that it uses different types of tags. So, I parse the Phoenix Arizona dataset using ElementTree and count number of the unique tags. `1_mapparser.py` is used to count the numbers of unique tags.

* 'bounds': 1,
* 'member': 91990,
* 'nd': 1014172,
* 'node': 871912,
* 'osm': 1,
* 'relation': 5811,
* 'tag': 547771,
* 'way': 117187


The osm file is 778 MB. The 547,771 tags in the file are name-value pair, to define multiple attributes of nodes or ways.

### Patterns in the Tags

The `"k"` value of each tag contain different patterns. Using `2_tags.py`, I created  3 regular expressions to check for certain patterns in the tags. I have counted each of four tag categories.

*  `"lower" : 1635966`, for tags that contain only lowercase letters and are valid,
*  `"lower_colon" : 937780`, for otherwise valid tags with a colon in their names,
*  `"other" : 13503`, for other tags that do not fall into the other three categories,
*  `"problemchars" : 3`, for tags with problematic characters.


Three tags contain problemtic characters:
- Hours Of Operation
- payments accepted
- FR 5

## 2. Problems Encountered in the Map

The main problem we encountered in the dataset is the Street name and City name inonsistencies. Below is the old name corrected with the better name. Using `3_audit.py`, we updated the names.

### i. Street name inconsistencies

Since data is crowd sourced, there is no standard format for street names. With an expected street type list 
["Street", "Avenue", "Boulevard", "Drive", "Court", "Place", "Square", "Lane", "Road", "Way", "Trail", "Parkway", "Commons", "Circle", "Terrace", "Highway"]

We get the following dictionary of streets with unexpected types. We can see the majority of these streets ending with numbers or abbreviations like 'Rd' and 'Ave'.

- "St": "Street"
- "St.": "Street"
- "street": "Street"
- "Ave": "Avenue"
- "Ave.": "Avenue"
- "Blvd": "Boulevard"
- "Blvd.": "Boulevard"
- "Boulavard": "Boulevard"
- "Rd": "Road"
- "Rd.": "Road"
- "RD": "Road"
- "Pl": "Place"
- "Pl.": "Place"
- "PKWY": "Parkway"
- "Pkwy": "Parkway"
- "Ln": "Lane"
- "Ln.": "Lane"
- "Dr": "Drive"
- "Dr.": "Drive"

### ii. Phone number inconsistencies

Different formats of phone number are found in the data, among which are (XXX) XXX-XXXX, XXX-XXX-XXXX, +XXX-XXX-XXXX, 1XXXXXXXXXX, +1 XXX XXX XXXX, +1 XXX-XXX-XXXX, +1 XXX.XXX.XXXX, +1 (XXX) XXX-XXXX and even 'Phone number (XXX) XXX-XXXX' or a list.

According to Wikipedia, common types of phone number format include (XXX) XXX-XXXX, XXX-XXX-XXXX, XXX.XXX.XXXX, or adding '1' at the beginning. To make it more consistent, I decide to change all phone numbers in the format of XXX-XXX-XXXX or 1-XXX-XXX-XXXX.

- (480)331-VOIP: 480-331-8647
- 480-814-TOGO: 480-814-8646

## 3. Data Overview

### File sizes:

- phoenix_arizona.osm: 786.4 MB
- nodes_csv: 278.7 MB
- nodes_tags.csv: 12.4 MB
- ways_csv: 28 MB
- ways_nodes.csv: 94.4 MB
- ways_tags.csv: 77.2 MB
- phoenix_arizona.db: 561.8 MB

### Number of nodes:
``` python
sqlite> SELECT COUNT(*) FROM nodes
```
**Output:**
```
3274275
```

### Number of ways:
```python
sqlite> SELECT COUNT(*) FROM ways
```
**Output:**
```
453824
```

### Number of unique users:
``` python
sqlite> SELECT COUNT(DISTINCT(e.uid))          
FROM (SELECT uid FROM nodes UNION ALL SELECT uid FROM ways) e;
```
**Output:**
```
1551
```

### Keys group:
``` python
sqlite> SELECT key, COUNT(*) AS num FROM nodes_tags GROUP BY key ORDER BY num DESC LIMIT 10;
```
**Output:**
```
highway         87928
power           24895
natural         20831
crossing        16989
bicycle         11288
horse           11155
supervised      11078
name            10235
traffic_calming  9926
amenity          8268
```

### Highway types:
``` python
sqlite> SELECT value, COUNT(*) as num FROM ways_tags WHERE ways_tags.key = "highway" GROUP BY value ORDER BY num DESC LIMIT 10;
```
**Output:**
```
residential    109830
service         85842
secondary       31225
tertiary        17681
footway         14589
primary         10143
motorway_link    3499
unclassified     3394
track            2879
motorway         2412
```

# 4. Additional Data Exploration

### Common ammenities:
```python
sqlite> SELECT value, COUNT(*) as num
FROM nodes_tags
WHERE key='amenity'
GROUP BY value
ORDER BY num DESC
LIMIT 10;

```
**Output:**
```
bench              1267
restaurant          787
waste_basket        750
fast food           726
fuel			    685
place of worship    613
school  	        431
fountain		    261
bank	            221
pharmacy	        175
```

### Most popular restaurant:
```python
sqlite> SELECT nodes_tags.value, COUNT(*) as num 
FROM nodes_tags 
JOIN (SELECT DISTINCT(id) FROM nodes_tags WHERE value="restaurant") i 
ON nodes_tags.id=i.id 
WHERE nodes_tags.key="name" 
GROUP BY nodes_tags.value 
ORDER BY num DESC;
```
**Output:**
```
Denny's
```

### Most popular cuisine:
```python
sqlite> SELECT nodes_tags.value, COUNT(*) as num 
FROM nodes_tags 
JOIN (SELECT DISTINCT(id) FROM nodes_tags WHERE value="restaurant") i 
ON nodes_tags.id=i.id 
WHERE nodes_tags.key="cuisine" 
GROUP BY nodes_tags.value 
ORDER BY num DESC;
```
**Output:**
```
Pizza
```

### Biggest religion:
```python
sqlite> SELECT nodes_tags.value, COUNT(*) as num 
FROM nodes_tags 
JOIN (SELECT DISTINCT(id) FROM nodes_tags WHERE value="place_of_worship") i 
ON nodes_tags.id=i.id 
WHERE nodes_tags.key="religion" 
GROUP BY nodes_tags.value 
ORDER BY num DESC 
LIMIT 1;
```
**Output:**
```
Christian
```

# 5. Ideas for Improvement

### i. Additional Suggestion and Ideas: Wheelchair accessibility

#### Number of nodes
```python
sqlite> SELECT COUNT(*) FROM nodes
```
**Output:**
```
3274275
```

#### Number of nodes with wheelchair accessibility information
```python
sqlite> SELECT COUNT(*) FROM nodes_tags WHERE key="wheelchair"
```
**Output:**
```
419
```

#### Percentage of nodes with wheelchair accessibility information
419 / 3274275 = 0.013%

Approximately 0.01% of the nodes in the dataset contain wheelchair accessibility information. That seems like a strikingly low number, even with a large amount of nodes being private property (e.g. homes).

### ii. Additional Suggestion and Ideas: Improvements 

Based on the above data exploration, some of the issues in the data are accuracy and consistency. In addition, the dataset would benefit from participation of larger number of users. Some ideas that could be explored to improve this dataset include:

#### 1. Integration with popular games or apps, such as Pokemon Go, Snap Map, and others to encourage more user participation.

Benefits:
- Engaging more users to participate
- Some apps, like Pokemon Go encourages users to go to some places that they usually don't explore. This approach may provide more coverage of areas that don't have many nodes and ways in the dataset.

Anticipated problems:
- The accuracy of the data from this approach may not be very high as users are more likely to be focused on the game and app, rather than entering accurate data.
- Similarly, the data entry may also not be very consistent as users are multi tasking with the games and apps.

#### 2. Collaboration with local shops, restaurants, hotels, etc to provide discount to users who come and help enter the data into the Openstreetmap project.

Benefits:
- Bring more business to these shops, restaurants, hotels, etc
- Encourage more users to participate

Anticipated problems:
- This approach may be more expensive as it needs cost to provide discount and promote the program.
- A system needs to be built such that only users who provide accurate and consistent data entry receives the discount.

# 6. Conclusion
The OpenStreetMap data of Phenoix, Arizona is of fairly reasonable quality but the typo errors caused by the human inputs are significant. I have cleaned a significant amount of the data which is required for this project. But, there are lots of improvement needed in the dataset. The dataset contains very less amount of additional information such as tourist attractions, popular places and other useful interest. The dataset contains very old information which is now incomparable to that of Google Maps or Bing Maps.

So, I think there are still several opportunities for cleaning and validation of the data in the future. 
