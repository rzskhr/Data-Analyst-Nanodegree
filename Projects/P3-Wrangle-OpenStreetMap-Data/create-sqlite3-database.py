#!/usr/bin/env python
# -*- coding: utf-8 -*-


# All the imports done here
import sqlite3
import csv
from sample_osm import take_every_nth_element


# file locations
raw_file_path = "/Users/Raj/Root/GitHub/__Datasets__/OSM/processed-osm/"    # If file is big, send to raw file path
# database file location
if take_every_nth_element > 49:
    DATABASE_FILE = "chicago_osm_sqlite3_database.db"
else:
    DATABASE_FILE = raw_file_path+"chicago_osm_sqlite3_database.db"

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
    # cur.execute("CREATE TABLE nodes (id, lat, lon, user, uid, version, changeset, timestamp);")
    cur.execute("CREATE TABLE Nodes(id INTEGER PRIMARY KEY, lat REAL, lon REAL, user TEXT, uid INTEGER, version INTEGER, changeset INTEGER, timestamp DATETIME);")
    with open(nodes_file_path, 'r') as f:
        dr = csv.DictReader(f)
        to_db = [(i['id'], i['lat'], i['lon'], i['user'], i['uid'], i['version'], i['changeset'], i['timestamp']) \
                 for i in dr]

    cur.executemany("INSERT INTO Nodes (id, lat, lon, user, uid, version, changeset, timestamp) \
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?);", to_db)
    con.commit()
    f.close()


def create_node_tags_table(node_tags_file_path):
    # cur.execute("CREATE TABLE nodes_tags (id, key, value, type);")
    cur.execute("CREATE TABLE nodesTags(id INTEGER, key TEXT, value TEXT, type TEXT, FOREIGN KEY (id) REFERENCES Nodes (id));")
    with open(node_tags_file_path, 'r') as f:
        dr = csv.DictReader(f)
        to_db = [(i['id'], i['key'], i['value'], i['type']) for i in dr]

    cur.executemany("INSERT INTO nodesTags (id, key, value, type) VALUES (?, ?, ?, ?);", to_db)
    con.commit()
    f.close()


def create_ways_table(ways_file_path):
    # cur.execute("CREATE TABLE ways (id, user, uid, version, changeset, timestamp);")
    cur.execute("CREATE TABLE Ways(id INTEGER PRIMARY KEY, user TEXT, uid INTEGER, version INTEGER, changeset INTEGER, timestamp DATETIME);")
    with open(ways_file_path, 'r') as f:
        dr = csv.DictReader(f)
        to_db = [(i['id'], i['user'], i['uid'], i['version'], i['changeset'], i['timestamp']) for i in dr]

    cur.executemany("INSERT INTO Ways (id, user, uid, version, changeset, timestamp) VALUES (?, ?, ?, ?, ?, ?);", to_db)
    con.commit()
    f.close()


def create_ways_nodes_table(ways_nodes_file_path):
    # cur.execute("CREATE TABLE ways_nodes (id, node_id, position);")
    cur.execute("CREATE TABLE waysNodes(id INTEGER, node_id INTEGER, position INTEGER, FOREIGN KEY(id) REFERENCES Nodes(id));")
    with open(ways_nodes_file_path, 'r') as f:
        dr = csv.DictReader(f)
        to_db = [(i['id'], i['node_id'], i['position']) for i in dr]

    cur.executemany("INSERT INTO waysNodes (id, node_id, position) VALUES (?, ?, ?);", to_db)
    con.commit()
    f.close()


def create_ways_tags_table(ways_tags_file_path):
    # cur.execute("CREATE TABLE ways_tags (id, key, value, type);")
    cur.execute("CREATE TABLE waysTags(id INTEGER, key TEXT, value TEXT, type TEXT, FOREIGN KEY(id) REFERENCES Ways(id));")
    with open(ways_tags_file_path, 'r') as f:
        dr = csv.DictReader(f)
        to_db = [(i['id'], i['key'], i['value'], i['type']) for i in dr]

    cur.executemany("INSERT INTO waysTags (id, key, value, type) VALUES (?, ?, ?, ?);", to_db)
    con.commit()
    f.close()


if __name__ == '__main__':

    # using datetime module to track the time taken
    import datetime
    a = datetime.datetime.now()
    print("Start time: ", a)

    # Call database creation functions
    print("creating Database...")
    create_nodes_table(NODES_FILE_PATH)
    create_node_tags_table(NODE_TAGS_FILE_PATH)
    create_ways_table(WAYS_FILE_PATH)
    create_ways_nodes_table(WAY_NODES_FILE_PATH)
    create_ways_tags_table(WAY_TAGS_FILE_PATH)
    print("finished.")

    b = datetime.datetime.now()
    print("End time: ", b)
    print("DIFF: ", b-a)

    """
    It took around 4 minutes to process the files extracted from the raw osm file of size 2.14GB
    Database file size = 1.25 GB
    
    Log from above main function:
    Start time:  2018-02-08 13:32:04.735190
    creating Database...
    finished.
    End time:  2018-02-08 13:35:59.510423
    DIFF:  0:03:54.775233
    
    Process finished with exit code 0
    """



