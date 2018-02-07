#!/usr/bin/env python
# -*- coding: utf-8 -*-

# All the imports done here
import xml.etree.cElementTree as Et


def is_postcode(elem):
    """
    helper function used in audit(osm_file), to check the attribute contains phone number

    :param elem: element from node or way tag
    :return: bool
    """
    return elem.attrib['k'] == "addr:postcode"


def audit_postcode(osm_file):
    """
    this function takes the osm_file as parameter and returns a default dictionary ...
    ...mapping the correct and incorrect phone numbers as per the defined regular expression

    :usage: pass the osm_file to collect the phone num dictionary
    ex output:
    {'Correct': ['+1-312-666-4100', '+1-847-906-8685', '+1-219-947-1309'],
     'Incorrect': ['630-393-9609',
                   '(847) 376-8014',
                   '847-810-3888',
                   '(312) 744-0019',
                   '(815) 524-4391',
                   '630-ADD-PARK']}

    :param osm_file: osm_file with the map data
    :return: dictionary mapping correct and incorrect phone numbers
    """
    osm_file = open(osm_file, "r")
    postcode_list = list()
    for event, elem in Et.iterparse(osm_file, events=("start",)):

        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                # calling helper function is_street_name(elem)
                if is_postcode(tag):
                    postcode = tag.attrib['v']
                    postcode_list.append(postcode)

    osm_file.close()
    return postcode_list


def update_postcode(postcode):
    """
    Update the street names by checking the last word in the street name...
    ...if the word is abbreviated change the street name as given in the mapping dict

    :param postcode: a phone number
    :return: correctly formatted phone number as per the phone_num_re regular expression
    """
    # if the format is correct return same

    return postcode


# uncomment to run test
# OSM_FILE = "osm-files/sample.osm"
#
#
# def test():
#     postcode_list = audit_postcode(OSM_FILE)
#
#     import pprint
#     pprint.pprint(postcode_list)
#
#     # for postcode in postcode_list:
#     #     formatted_postcode = update_postcode(postcode)
#     #     print(postcode, " ==> ", formatted_postcode)
#
#
# if __name__ == '__main__':
#     test()
