import sqlite3
import csv
from sample_osm import take_every_nth_element


# flie locations
raw_file_path = "/Users/Raj/Root/GitHub/__Datasets__/OSM/processed-osm/"    # If file is big, send to raw file path
# database file location
if take_every_nth_element > 49:
    DATABASE_FILE = "chicago_osm.db"
else:
    DATABASE_FILE = raw_file_path+"chicago_osm.db"

# csv file location
if take_every_nth_element > 49:
    NODES_FILE_PATH = "csv-files/nodes.csv"
    NODE_TAGS_FILE_PATH = "csv-files/nodes_tags.csv"
    WAYS_FILE_PATH = "csv-files/ways.csv"
    WAY_NODES_FILE_PATH = "csv-files/ways_nodes.csv"
    WAY_TAGS_FILE_PATH = "csv-files/ways_tags.csv"
else:
    NODES_FILE_PATH = raw_file_path+"csv-files/nodes.csv"
    NODE_TAGS_FILE_PATH = raw_file_path+"csv-files/nodes_tags.csv"
    WAYS_FILE_PATH = raw_file_path+"csv-files/ways.csv"
    WAY_NODES_FILE_PATH = raw_file_path+"csv-files/ways_nodes.csv"
    WAY_TAGS_FILE_PATH = raw_file_path+"csv-files/ways_tags.csv"


# establishing sqlite3 connection
con = sqlite3.connect(DATABASE_FILE)
con.text_factory = str
cur = con.cursor()

def create_nodes_table(nodes_file_path):
    cur.execute("CREATE TABLE nodes (id, lat, lon, user, uid, version, changeset, timestamp);")
    with open(nodes_file_path, 'rb') as f:
        dr = csv.DictReader(f)
        to_db = [(i['id'], i['lat'], i['lon'], i['user'], i['uid'], i['version'], i['changeset'], i['timestamp']) \
                 for i in dr]
    
    cur.executemany("INSERT INTO nodes (id, lat, lon, user, uid, version, changeset, timestamp) \
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?);", to_db)
                    con.commit()
f.close()


def create_node_tags_table(node_tags_file_path):
    cur.execute("CREATE TABLE nodes_tags (id, key, value, type);")
    with open(node_tags_file_path, 'rb') as f:
        dr = csv.DictReader(f)
        to_db = [(i['id'], i['key'], i['value'], i['type']) for i in dr]
    
    cur.executemany("INSERT INTO nodes_tags (id, key, value, type) VALUES (?, ?, ?, ?);", to_db)
    con.commit()
    f.close()


def create_ways_table(ways_file_path):
    cur.execute("CREATE TABLE ways (id, user, uid, version, changeset, timestamp);")
    with open(ways_file_path, 'rb') as f:
        dr = csv.DictReader(f)
        to_db = [(i['id'], i['user'], i['uid'], i['version'], i['changeset'], i['timestamp']) for i in dr]
    
    cur.executemany("INSERT INTO ways (id, user, uid, version, changeset, timestamp) VALUES (?, ?, ?, ?, ?, ?);", to_db)
    con.commit()
    f.close()


def create_ways_nodes_table(ways_nodes_file_path):
    cur.execute("CREATE TABLE ways_nodes (id, node_id, position);")
    with open(ways_nodes_file_path, 'rb') as f:
        dr = csv.DictReader(f)
        to_db = [(i['id'], i['node_id'], i['position']) for i in dr]
    
    cur.executemany("INSERT INTO ways_nodes (id, node_id, position) VALUES (?, ?, ?);", to_db)
    con.commit()
    f.close()

def create_ways_tags_table(ways_tags_file_path):
    cur.execute("CREATE TABLE ways_tags (id, key, value, type);")
    with open(ways_tags_file_path, 'rb') as f:
        dr = csv.DictReader(f)
        to_db = [(i['id'], i['key'], i['value'], i['type']) for i in dr]
    
    cur.executemany("INSERT INTO ways_tags (id, key, value, type) VALUES (?, ?, ?, ?);", to_db)
    con.commit()
    f.close()


if __name__ == '__main__':
    print("creating Database...")
    create_nodes_table(NODES_FILE_PATH)
    create_node_tags_table(NODE_TAGS_FILE_PATH)
    create_ways_table(WAYS_FILE_PATH)
    create_ways_nodes_table(WAY_NODES_FILE_PATH)
    create_ways_tags_table(WAY_TAGS_FILE_PATH)
    print("finished.")

