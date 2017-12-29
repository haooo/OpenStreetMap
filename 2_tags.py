import xml.etree.cElementTree as ET
import pprint
import re

from collections import defaultdict

lower = re.compile(r'^([a-z]|_)*$')
lower_colon = re.compile(r'^([a-z]|_)+:([a-z]|_)+')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')

OSMFILE = "phoenix_arizona.osm"

def key_type(element, keys):
    if element.tag == "tag":
        tag = element.attrib['k']
        if re.search(lower, tag):
            keys['lower'] += 1
        elif re.search(lower_colon, tag):
            keys['lower_colon'] +=1
        elif re.search(problemchars, tag):
            keys['problemchars']+=1
            print tag
        else:
            keys['other']+=1
            pass
    return keys

def process_map(filename):
    keys = {"lower": 0, "lower_colon": 0, "problemchars": 0, "other": 0}
    for _, element in ET.iterparse(filename):
        keys = key_type(element, keys)

    return keys

pprint.pprint(process_map(OSMFILE))
