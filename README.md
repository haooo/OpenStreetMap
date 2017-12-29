{
 "cells": [
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# Project 3: OpenStreetMap Data Wrangling with SQL"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "Name: Hao Lan\n",
    "\n",
    "Map Area: I have choosen Phoenix Arizona because I've been spending my summer vacation there, and I really like the city.\n",
    "\n",
    "* Location: Phoenix Arizona, USA\n",
    "* [MapZen URL](https://mapzen.com/data/metro-extracts/)"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## 1. Data Audit"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "Unique Tags Looking at the XML file, I found that it uses different types of tags. So, I parse the Phoenix Arizona dataset using ElementTree and count number of the unique tags. `1_mapparser.py` is used to count the numbers of unique tags."
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "* 'bounds': 1,\n",
    "* 'member': 91990,\n",
    "* 'nd': 1014172,\n",
    "* 'node': 871912,\n",
    "* 'osm': 1,\n",
    "* 'relation': 5811,\n",
    "* 'tag': 547771,\n",
    "* 'way': 117187\n",
    "\n",
    "\n",
    "The osm file is 778 MB. The 547,771 tags in the file are name-value pair, to define multiple attributes of nodes or ways."
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "### Patterns in the Tags"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "The `\"k\"` value of each tag contain different patterns. Using `2_tags.py`, I created  3 regular expressions to check for certain patterns in the tags. I have counted each of four tag categories."
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "*  `\"lower\" : 1635966`, for tags that contain only lowercase letters and are valid,\n",
    "*  `\"lower_colon\" : 937780`, for otherwise valid tags with a colon in their names,\n",
    "*  `\"other\" : 13503`, for other tags that do not fall into the other three categories,\n",
    "*  `\"problemchars\" : 3`, for tags with problematic characters.\n",
    "\n",
    "\n",
    "Three tags contain problemtic characters:\n",
    "- Hours Of Operation\n",
    "- payments accepted\n",
    "- FR 5"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## 2. Problems Encountered in the Map"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "The main problem we encountered in the dataset is the Street name and City name inonsistencies. Below is the old name corrected with the better name. Using `3_audit.py`, we updated the names."
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "### i. Street name inconsistencies\n",
    "\n",
    "Since data is crowd sourced, there is no standard format for street names. With an expected street type list \n",
    "[\"Street\", \"Avenue\", \"Boulevard\", \"Drive\", \"Court\", \"Place\", \"Square\", \"Lane\", \"Road\", \"Way\", \"Trail\", \"Parkway\", \"Commons\", \"Circle\", \"Terrace\", \"Highway\"]\n",
    "\n",
    "We get the following dictionary of streets with unexpected types. We can see the majority of these streets ending with numbers or abbreviations like 'Rd' and 'Ave'."
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "- \"St\": \"Street\"\n",
    "- \"St.\": \"Street\"\n",
    "- \"street\": \"Street\"\n",
    "- \"Ave\": \"Avenue\"\n",
    "- \"Ave.\": \"Avenue\"\n",
    "- \"Blvd\": \"Boulevard\"\n",
    "- \"Blvd.\": \"Boulevard\"\n",
    "- \"Boulavard\": \"Boulevard\"\n",
    "- \"Rd\": \"Road\"\n",
    "- \"Rd.\": \"Road\"\n",
    "- \"RD\": \"Road\"\n",
    "- \"Pl\": \"Place\"\n",
    "- \"Pl.\": \"Place\"\n",
    "- \"PKWY\": \"Parkway\"\n",
    "- \"Pkwy\": \"Parkway\"\n",
    "- \"Ln\": \"Lane\"\n",
    "- \"Ln.\": \"Lane\"\n",
    "- \"Dr\": \"Drive\"\n",
    "- \"Dr.\": \"Drive\""
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "### ii. Phone number inconsistencies"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "Different formats of phone number are found in the data, among which are (XXX) XXX-XXXX, XXX-XXX-XXXX, +XXX-XXX-XXXX, 1XXXXXXXXXX, +1 XXX XXX XXXX, +1 XXX-XXX-XXXX, +1 XXX.XXX.XXXX, +1 (XXX) XXX-XXXX and even 'Phone number (XXX) XXX-XXXX' or a list.\n",
    "\n",
    "According to Wikipedia, common types of phone number format include (XXX) XXX-XXXX, XXX-XXX-XXXX, XXX.XXX.XXXX, or adding '1' at the beginning. To make it more consistent, I decide to change all phone numbers in the format of XXX-XXX-XXXX or 1-XXX-XXX-XXXX."
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "- (480)331-VOIP: 480-331-8647\n",
    "- 480-814-TOGO: 480-814-8646"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## 3. Data Overview"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "### File sizes:"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "- phoenix_arizona.osm: 786.4 MB\n",
    "- nodes_csv: 278.7 MB\n",
    "- nodes_tags.csv: 12.4 MB\n",
    "- ways_csv: 28 MB\n",
    "- ways_nodes.csv: 94.4 MB\n",
    "- ways_tags.csv: 77.2 MB\n",
    "- phoenix_arizona.db: 561.8 MB"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "### Number of nodes:\n",
    "``` python\n",
    "sqlite> SELECT COUNT(*) FROM nodes\n",
    "```\n",
    "**Output:**\n",
    "```\n",
    "3274275\n",
    "```"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "### Number of ways:\n",
    "```python\n",
    "sqlite> SELECT COUNT(*) FROM ways\n",
    "```\n",
    "**Output:**\n",
    "```\n",
    "453824\n",
    "```"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "### Number of unique users:\n",
    "``` python\n",
    "sqlite> SELECT COUNT(DISTINCT(e.uid))          \n",
    "FROM (SELECT uid FROM nodes UNION ALL SELECT uid FROM ways) e;\n",
    "```\n",
    "**Output:**\n",
    "```\n",
    "1551\n",
    "```"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "### Keys group:\n",
    "``` python\n",
    "sqlite> SELECT key, COUNT(*) AS num FROM nodes_tags GROUP BY key ORDER BY num DESC LIMIT 10;\n",
    "```\n",
    "**Output:**\n",
    "```\n",
    "highway         87928\n",
    "power           24895\n",
    "natural         20831\n",
    "crossing        16989\n",
    "bicycle         11288\n",
    "horse           11155\n",
    "supervised      11078\n",
    "name            10235\n",
    "traffic_calming  9926\n",
    "amenity          8268\n",
    "```"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "### Highway types:\n",
    "``` python\n",
    "sqlite> SELECT value, COUNT(*) as num FROM ways_tags WHERE ways_tags.key = \"highway\" GROUP BY value ORDER BY num DESC LIMIT 10;\n",
    "```\n",
    "**Output:**\n",
    "```\n",
    "residential    109830\n",
    "service         85842\n",
    "secondary       31225\n",
    "tertiary        17681\n",
    "footway         14589\n",
    "primary         10143\n",
    "motorway_link    3499\n",
    "unclassified     3394\n",
    "track            2879\n",
    "motorway         2412\n",
    "```"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# 4. Additional Data Exploration"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "### Common ammenities:\n",
    "```python\n",
    "sqlite> SELECT value, COUNT(*) as num\n",
    "FROM nodes_tags\n",
    "WHERE key='amenity'\n",
    "GROUP BY value\n",
    "ORDER BY num DESC\n",
    "LIMIT 10;\n",
    "\n",
    "```\n",
    "**Output:**\n",
    "```\n",
    "bench              1267\n",
    "restaurant          787\n",
    "waste_basket        750\n",
    "fast food           726\n",
    "fuel\t\t\t    685\n",
    "place of worship    613\n",
    "school  \t        431\n",
    "fountain\t\t    261\n",
    "bank\t            221\n",
    "pharmacy\t        175\n",
    "```"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "### Most popular restaurant:\n",
    "```python\n",
    "sqlite> SELECT nodes_tags.value, COUNT(*) as num \n",
    "FROM nodes_tags \n",
    "JOIN (SELECT DISTINCT(id) FROM nodes_tags WHERE value=\"restaurant\") i \n",
    "ON nodes_tags.id=i.id \n",
    "WHERE nodes_tags.key=\"name\" \n",
    "GROUP BY nodes_tags.value \n",
    "ORDER BY num DESC;\n",
    "```\n",
    "**Output:**\n",
    "```\n",
    "Denny's\n",
    "```"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "### Most popular cuisine:\n",
    "```python\n",
    "sqlite> SELECT nodes_tags.value, COUNT(*) as num \n",
    "FROM nodes_tags \n",
    "JOIN (SELECT DISTINCT(id) FROM nodes_tags WHERE value=\"restaurant\") i \n",
    "ON nodes_tags.id=i.id \n",
    "WHERE nodes_tags.key=\"cuisine\" \n",
    "GROUP BY nodes_tags.value \n",
    "ORDER BY num DESC;\n",
    "```\n",
    "**Output:**\n",
    "```\n",
    "Pizza\n",
    "```"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "### Biggest religion:\n",
    "```python\n",
    "sqlite> SELECT nodes_tags.value, COUNT(*) as num \n",
    "FROM nodes_tags \n",
    "JOIN (SELECT DISTINCT(id) FROM nodes_tags WHERE value=\"place_of_worship\") i \n",
    "ON nodes_tags.id=i.id \n",
    "WHERE nodes_tags.key=\"religion\" \n",
    "GROUP BY nodes_tags.value \n",
    "ORDER BY num DESC \n",
    "LIMIT 1;\n",
    "```\n",
    "**Output:**\n",
    "```\n",
    "Christian\n",
    "```"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# 5. Ideas for Improvement"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "### i. Additional Suggestion and Ideas: Wheelchair accessibility"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "#### Number of nodes\n",
    "```python\n",
    "sqlite> SELECT COUNT(*) FROM nodes\n",
    "```\n",
    "**Output:**\n",
    "```\n",
    "3274275\n",
    "```"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "#### Number of nodes with wheelchair accessibility information\n",
    "```python\n",
    "sqlite> SELECT COUNT(*) FROM nodes_tags WHERE key=\"wheelchair\"\n",
    "```\n",
    "**Output:**\n",
    "```\n",
    "419\n",
    "```"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "#### Percentage of nodes with wheelchair accessibility information\n",
    "419 / 3274275 = 0.013%"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "Approximately 0.01% of the nodes in the dataset contain wheelchair accessibility information. That seems like a strikingly low number, even with a large amount of nodes being private property (e.g. homes)."
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "### ii. Additional Suggestion and Ideas: Improvements "
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "Based on the above data exploration, some of the issues in the data are accuracy and consistency. In addition, the dataset would benefit from participation of larger number of users. Some ideas that could be explored to improve this dataset include:"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "#### 1. Integration with popular games or apps, such as Pokemon Go, Snap Map, and others to encourage more user participation.\n",
    "\n",
    "Benefits:\n",
    "- Engaging more users to participate\n",
    "- Some apps, like Pokemon Go encourages users to go to some places that they usually don't explore. This approach may provide more coverage of areas that don't have many nodes and ways in the dataset.\n",
    "\n",
    "Anticipated problems:\n",
    "- The accuracy of the data from this approach may not be very high as users are more likely to be focused on the game and app, rather than entering accurate data.\n",
    "- Similarly, the data entry may also not be very consistent as users are multi tasking with the games and apps."
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "#### 2. Collaboration with local shops, restaurants, hotels, etc to provide discount to users who come and help enter the data into the Openstreetmap project.\n",
    "\n",
    "Benefits:\n",
    "- Bring more business to these shops, restaurants, hotels, etc\n",
    "- Encourage more users to participate\n",
    "\n",
    "Anticipated problems:\n",
    "- This approach may be more expensive as it needs cost to provide discount and promote the program.\n",
    "- A system needs to be built such that only users who provide accurate and consistent data entry receives the discount."
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# 6. Conclusion\n",
    "The OpenStreetMap data of Phenoix, Arizona is of fairly reasonable quality but the typo errors caused by the human inputs are significant. I have cleaned a significant amount of the data which is required for this project. But, there are lots of improvement needed in the dataset. The dataset contains very less amount of additional information such as tourist attractions, popular places and other useful interest. The dataset contains very old information which is now incomparable to that of Google Maps or Bing Maps.\n",
    "\n",
    "So, I think there are still several opportunities for cleaning and validation of the data in the future. "
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python [conda env:py27]",
   "language": "python",
   "name": "conda-env-py27-py"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 2
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython2",
   "version": "2.7.13"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 2
}
