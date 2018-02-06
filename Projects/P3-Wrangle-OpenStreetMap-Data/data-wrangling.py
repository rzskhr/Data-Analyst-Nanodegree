#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""

"""


# All the imports done here
import xml.etree.cElementTree as Et
import re

import codecs
import cerberus     # http://docs.python-cerberus.org/en/stable/

# imports from this project
from unicode_dict_writer import UnicodeDictWriter
from sample_osm import fetch_element
from validator import validate_element

# CONSTANTS

# file path
OSM_FILE = "osm-files/sample.osm"

# files to be written after processing the data
NODES_FILE_PATH = "csv-files/nodes.csv"
NODE_TAGS_FILE_PATH = "csv-files/nodes_tags.csv"
WAYS_FILE_PATH = "csv-files/ways.csv"
WAY_NODES_FILE_PATH = "csv-files/ways_nodes.csv"
WAY_TAGS_FILE_PATH = "csv-files/ways_tags.csv"

# schema as provided in the description
SCHEMA = "schema.py"

# categorize the columns for the tables to be parsed into csv as per the given schema
NODE_FIELDS = ['id', 'lat', 'lon', 'user', 'uid', 'version', 'changeset', 'timestamp']
NODE_TAGS_FIELDS = ['id', 'key', 'value', 'type']
WAY_FIELDS = ['id', 'user', 'uid', 'version', 'changeset', 'timestamp']
WAY_TAGS_FIELDS = ['id', 'key', 'value', 'type']
WAY_NODES_FIELDS = ['id', 'node_id', 'position']

# precompiled regular expressions
lower = re.compile(r'^([a-z]|_)*$')
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
PROBLEM_CHARS = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')


def shape_element(element, node_attr_fields=NODE_FIELDS, way_attr_fields=WAY_FIELDS,
                  problem_chars=PROBLEM_CHARS, default_tag_type='regular'):

    # data structures for holding the processed data
    node_attributes, way_attributes = dict(), dict()
    way_nodes, tags = list(), list()

    # condition for node tags
    if element.tag == 'node':
        print('')

    # condition for way tags
    elif element.tag == 'way':
        print(element)

    return 1


def process_map(osm_file, validate):
    """
    process each XML element and write to respective CSV files

    :return: Nothing writes the files to the specified location
    """
    with codecs.open(NODES_FILE_PATH, 'w') as nodes_file, \
         codecs.open(NODE_TAGS_FILE_PATH, 'w') as nodes_tags_file, \
         codecs.open(WAYS_FILE_PATH, 'w') as ways_file, \
         codecs.open(WAY_NODES_FILE_PATH, 'w') as way_nodes_file, \
         codecs.open(WAY_TAGS_FILE_PATH, 'w') as way_tags_file:

        # call the UnicodeDictWriter function from unicode_dict_writer to write
        nodes_writer = UnicodeDictWriter(nodes_file, NODE_FIELDS)
        node_tags_writer = UnicodeDictWriter(nodes_tags_file, NODE_TAGS_FIELDS)
        ways_writer = UnicodeDictWriter(ways_file, WAY_FIELDS)
        way_nodes_writer = UnicodeDictWriter(way_nodes_file, WAY_NODES_FIELDS)
        way_tags_writer = UnicodeDictWriter(way_tags_file, WAY_TAGS_FIELDS)

        nodes_writer.writeheader()
        node_tags_writer.writeheader()
        ways_writer.writeheader()
        way_nodes_writer.writeheader()
        way_tags_writer.writeheader()

        validator = cerberus.Validator()

        for element in fetch_element(osm_file, tags=('node', 'way')):
            shaped_element = shape_element(element)

            if shaped_element:
                if validate is True:
                    validate_element(shaped_element, validator)

                if element.tag == 'node':
                    nodes_writer.writerow(shaped_element['node'])
                    node_tags_writer.writerows(shaped_element['node_tags'])
                elif element.tag == 'way':
                    ways_writer.writerow(shaped_element['way'])
                    way_nodes_writer.writerows(shaped_element['way_nodes'])
                    way_tags_writer.writerows(shaped_element['way_tags'])


if __name__ == '__main__':
    # call the process map function
    # process_map(OSM_FILE, validate=True)

    for element in fetch_element(OSM_FILE, tags=('node', 'way')):
        shaped_element = shape_element(element)
