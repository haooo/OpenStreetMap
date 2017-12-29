import csv, sqlite3

def number_of_nodes():
	result = cur.execute('SELECT COUNT(*) FROM nodes')
	return result.fetchone()[0]

def number_of_ways():
	result = cur.execute('SELECT COUNT(*) FROM ways')
	return result.fetchone()[0]

def number_of_unique_users():
	result = cur.execute('SELECT COUNT(DISTINCT(e.uid)) \
            FROM (SELECT uid FROM nodes UNION ALL SELECT uid FROM ways) e')
	return result.fetchone()[0]

def number_of_users_contributing_once():
	result = cur.execute('SELECT COUNT(*) \
            FROM \
                (SELECT e.user, COUNT(*) as num \
                 FROM (SELECT user FROM nodes UNION ALL SELECT user FROM ways) e \
                 GROUP BY e.user \
                 HAVING num=1) u')
	return result.fetchone()[0]

def keys_group():
	keys = [] 
	for row in cur.execute('SELECT key, COUNT(*) AS num FROM nodes_tags GROUP BY key ORDER BY num DESC LIMIT 10'):
				keys.append(row)
	return keys

def highway_types():
	highway = [] 
	for row in cur.execute('SELECT value, COUNT(*) as num FROM ways_tags WHERE ways_tags.key = "highway" \
            GROUP BY value ORDER BY num DESC LIMIT 10'):
				highway.append(row)
	return highway

def common_ammenities():
	ammenity = []    
	for row in cur.execute('SELECT value, COUNT(*) as num \
            FROM nodes_tags \
            WHERE key="amenity" \
            GROUP BY value \
            ORDER BY num DESC \
            LIMIT 10'):
				ammenity.append(row)
	return ammenity

def most_popular_restaurant():
	for row in cur.execute('SELECT nodes_tags.value, COUNT(*) as num \
            FROM nodes_tags \
                JOIN (SELECT DISTINCT(id) FROM nodes_tags WHERE value="restaurant") i \
                ON nodes_tags.id=i.id \
            WHERE nodes_tags.key="name" \
            GROUP BY nodes_tags.value \
            ORDER BY num DESC'):
		return row

def most_popular_cuisine():
	for row in cur.execute('SELECT nodes_tags.value, COUNT(*) as num \
            FROM nodes_tags \
                JOIN (SELECT DISTINCT(id) FROM nodes_tags WHERE value="restaurant") i \
                ON nodes_tags.id=i.id \
            WHERE nodes_tags.key="cuisine" \
            GROUP BY nodes_tags.value \
            ORDER BY num DESC'):
		return row
    
def biggest_religion():
	for row in cur.execute('SELECT nodes_tags.value, COUNT(*) as num \
            FROM nodes_tags \
                JOIN (SELECT DISTINCT(id) FROM nodes_tags WHERE value="place_of_worship") i \
                ON nodes_tags.id=i.id \
            WHERE nodes_tags.key="religion" \
            GROUP BY nodes_tags.value \
            ORDER BY num DESC \
            LIMIT 1;'):
		return row

def wheelchair():
	result = cur.execute('SELECT COUNT(*) FROM nodes_tags WHERE key="wheelchair"')
	return result.fetchone()[0]

if __name__ == '__main__':
	
	con = sqlite3.connect("/Users/hao/Documents/DAND/OpenStreetMap/phoenix_arizona.db")
	cur = con.cursor()
	
	print "Number of nodes: " , number_of_nodes()
	print "Number of ways: " , number_of_ways()
	print "Number of unique users: " , number_of_unique_users()
	print "Number of users contributing once: " , number_of_users_contributing_once()
	print "Keys group" , keys_group()
	print "Highway types" , highway_types()
	print "Common ammenities: " , common_ammenities()
	print "Most Popular restaurant: " , most_popular_restaurant()
	print "Most Popular cuisine: " , most_popular_cuisine()
	print "Biggest religion: " , biggest_religion()
	print "Number of nodes with wheelchair accessibility: " , wheelchair()    
    
