#!/usr/bin/env python
# -*- coding: utf-8 -*-

# All the imports done here
import xml.etree.cElementTree as Et
from collections import defaultdict
import re


OSM_FILE = "sample.xml"


# precompiled regular expressions
street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)


# for auditing street names
# list of expected street names
expected = ["Street", "Avenue", "Boulevard", "Drive", "Court", "Place", "Square", "Lane", "Road",
            "Trail", "Parkway", "Commons"]

# mapping the incorrect street names to the correct ones
mapping = { "St": "Street",
            "St.": "Street",
            "Ave": "Avenue",
            "Rd.": "Road",
            "N.": "North",
            "Ave.": "Avenue",
            "Blvd.": "Boulevard",
            "Blvd": "Boulevard",
            }


def audit_street_type(street_types, street_name):
    """
    helper function used in audit(osmfile), updates the dictionary mapping the street names

    :param street_types: default dictionary set
    :param street_name: street name
    :return: update steet_types mapping wrong street name keyword to street name
    """
    m = street_type_re.search(street_name)
    if m:
        street_type = m.group()
        if street_type not in expected:
            street_types[street_type].add(street_name)


def is_street_name(elem):
    """
    helper function used in audit(osmfile), to check the attribute contains street name

    :param elem: element from node or way tag
    :return: bool
    """
    return elem.attrib['k'] == "addr:street"


def audit(osmfile):
    """
    this function takes the OSMFILE as parameter and returns a default dictionary set...
    ...mapping the wrong or abbreviated street names if not present in the expected list

    :usage: pass the osmfile to collect the street types dictionary
    ex output:
    {'Ave': set(['N. Lincoln Ave', 'North Lincoln Ave']),
     'Rd.': set(['Baldwin Rd.']),
     'St.': set(['West Lexington St.'])}

    :param osmfile: OSMFILE with the map data
    :return: dictionary mapping wrong street key word to the unique incorrect street names
    """
    osm_file = open(osmfile, "r")
    street_types = defaultdict(set)
    for event, elem in Et.iterparse(osm_file, events=("start",)):

        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                # calling helper function is_street_name(elem)
                if is_street_name(tag):
                    # print(tag.attrib)     # uncomment to see the street names
                    # calling helper function audit_street_type
                    audit_street_type(street_types, tag.attrib['v'])
    osm_file.close()
    return street_types


def update_name(name, mapping):
    """
    Update the street names by checking the last word in the street name...
    ...if the word is abbreviated change the street name as given in the mapping dict

    :usage: iterate over the dictionary obtained from audit function to update the names.
    ex: for st_type, ways in st_types.iteritems():
            for name in ways:
                better_name = update_name(name, mapping)

    :param name: street name
    :param mapping: dictionary mapping the incorrect to correct street names
    :return: correct street names
    """
    name_list = []
    for i in name.split(" "):
        name_list.append(i)

    if name_list[-1] in mapping:
        name_list[-1] = mapping[name_list[-1]]

    name = " ".join(name_list)
    return name


# uncomment to run test
# def test():
#     st_types = audit(OSM_FILE)
#
#     import pprint
#     pprint.pprint(dict(st_types))
#
#     for st_type, ways in st_types.items():
#         for name in ways:
#             better_name = update_name(name, mapping)
#             print(name, "=>", better_name)
#
#
# if __name__ == '__main__':
#     test()
