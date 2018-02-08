#!/usr/bin/env python
# -*- coding: utf-8 -*-


# All the imports done here
import re
import codecs
import cerberus     # http://docs.python-cerberus.org/en/stable/

# imports from this project
from unicode_dict_writer import UnicodeDictWriter
from sample_osm import fetch_element, take_every_nth_element
from validator import validate_element
from audit_street_name import is_street_name, update_street_name
from audit_phone import is_phone_num, update_phone
import schema

# CONSTANTS

# file path
OSM_FILE = "/Users/Raj/Root/GitHub/__Datasets__/OSM/chicago_illinois.osm"   # WARNING! raw file - 2.14 GB
# OSM_FILE = "osm-files/sample.osm"
raw_file_path = "/Users/Raj/Root/GitHub/__Datasets__/OSM/processed-osm/"    # If file is big, send to raw file path

# files to be written after processing the data
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

# schema as provided in the description
SCHEMA = schema

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
    """
    :param element: element from fetch_element function
    :param node_attr_fields: fields array according to schema
    :param way_attr_fields: fields array according to schema
    :param problem_chars: regular expression for problematic characters
    :param default_tag_type: tag type
    :return: Dictionary mapping the values
            # for node tags
            {'node': node_attributes, 'node_tags': inner_tags}

            # for way tags
            {'way': way_attributes, 'way_nodes': way_nodes, 'way_tags': inner_tags}
    """

    # data structures for holding the processed data
    node_attributes, way_attributes = dict(), dict()
    way_nodes, inner_tags = list(), list()

    # condition for node tags
    if element.tag == 'node':
        for attr, val in element.attrib.items():
            if attr in node_attr_fields:
                # adding all the node attributes to node_attributes dictionary
                node_attributes[attr] = val

        # for inner tags = 'tag'
        for tags in element.iter('tag'):
            # ignore if problem chars
            if problem_chars.match(tags.attrib['k']) is not None:
                continue
            else:
                processed_tag = process_tags(tags, element, default_tag_type)
                if processed_tag is not None:
                    inner_tags.append(processed_tag)

        return {'node': node_attributes, 'node_tags': inner_tags}

    # condition for way tags
    elif element.tag == 'way':
        for attr, val in element.attrib.items():
            if attr in way_attr_fields:
                # adding all the node attributes to node_attributes dictionary
                way_attributes[attr] = val

        # for inner tags = 'tag' and 'nd'
        position_nd = 0   # to keep track of 'nd' tag position
        for tags in element.iter():
            # for 'tag'
            if tags.tag == 'tag':
                # ignore if problem chars
                if problem_chars.match(tags.attrib['k']) is not None:
                    continue
                else:
                    processed_tag = process_tags(tags, element, default_tag_type)
                    if processed_tag is not None:
                        inner_tags.append(processed_tag)

            # for 'nd'
            elif tags.tag == 'nd':
                nd_dict = dict()
                nd_dict['id'] = element.attrib['id']        # store id
                nd_dict['node_id'] = tags.attrib['ref']     # storing the ref as node_id
                nd_dict['position'] = position_nd           # store the position of the nd node
                position_nd += 1
                # append the nd tag values to way nodes
                way_nodes.append(nd_dict)

        return {'way': way_attributes, 'way_nodes': way_nodes, 'way_tags': inner_tags}


def process_tags(tags, element, default_tag_type):
    # print(tags.attrib,  "\n", element.attrib, "\n", default_tag_type, "\n")

    tag_dict = dict()

    # for id
    tag_dict['id'] = element.attrib['id']

    # if no semicolon in the key, store as separate key = 'key', and default_tag_type=regular
    if ':' not in tags.attrib['k']:
        tag_dict['key'] = tags.attrib['k']
        tag_dict['type'] = default_tag_type

    # else if there is a semicolon in the keys, eg: tiger:county, addr:housenumber, addr:street:name, etc. ...
    else:
        index_of_first_colon = tags.attrib['k'].index(':')
        tag_dict['key'] = tags.attrib['k'][index_of_first_colon + 1:]   # make the words after colon as new key
        tag_dict['type'] = tags.attrib['k'][:index_of_first_colon]

    # check if the tag has street name
    if is_street_name(tags):
        # update the street name if last word not in expected, from the mapping in audit.py
        street_name = update_street_name(tags.attrib['v'])
        tag_dict['value'] = street_name

    # for phone number
    if is_phone_num(tags):
        phone_number = update_phone(tags.attrib['v'])
        tag_dict['value'] = phone_number

    # for postcode
    elif tag_dict['key'] == 'postcode':
        tag_dict['value'] = tags.attrib['v']

    # add all other values to tag_dict
    else:
        tag_dict['value'] = tags.attrib['v']

    return tag_dict


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
    # using datetime module to track the time taken
    import datetime
    a = datetime.datetime.now()
    print("Start time: ", a)

    # call the process map function
    process_map(OSM_FILE, validate=True)

    b = datetime.datetime.now()
    print("End time: ", b)
    print("DIFF: ", b-a)
