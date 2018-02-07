#!/usr/bin/env python
# -*- coding: utf-8 -*-

# All the imports done here
import xml.etree.cElementTree as Et
from collections import defaultdict
import re


# precompiled regular expressions
phone_num_re = re.compile(r'\+1-\d{3}-\d{3}-\d{4}')     # matches the format +1-312-999-9999


def is_phone_num(elem):
    """
    helper function used in audit(osm_file), to check the attribute contains phone number

    :param elem: element from node or way tag
    :return: bool
    """
    return elem.attrib['k'] == "phone"


def audit_phone(osm_file):
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
    correct_phone_numbers, incorrect_phone_numbers = list(), list()
    phone_number_dict = defaultdict()
    for event, elem in Et.iterparse(osm_file, events=("start",)):

        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                # calling helper function is_street_name(elem)
                if is_phone_num(tag):
                    phone_num = tag.attrib['v']
                    if re.match(phone_num_re, phone_num):
                        correct_phone_numbers.append(phone_num)
                        phone_number_dict['Correct'] = correct_phone_numbers
                    else:
                        incorrect_phone_numbers.append(phone_num)
                        phone_number_dict['Incorrect'] = incorrect_phone_numbers

    osm_file.close()
    return phone_number_dict


def update_phone(phone_num):
    """
    Update the street names by checking the last word in the street name...
    ...if the word is abbreviated change the street name as given in the mapping dict

    :param phone_num: a phone number
    :return: correctly formatted phone number as per the phone_num_re regular expression
    """
    # if the format is correct return same
    if re.match(phone_num_re, phone_num):
        return phone_num

    else:
        # remove brackets, hyphen and spaces (), -, +, " "
        # obtain consecutive numbers/chars
        phone_num = re.sub("[-()+]", "", phone_num)
        phone_num = re.sub(" ", "", phone_num)

        # return None if phone number is less than 10 or more than 11 digits
        if len([i for i in phone_num]) < 10:
            return None
        elif len([i for i in phone_num]) > 11:
            return None

        if re.match(r'\d{11}', phone_num) and phone_num[0] == '1':
            phone_num = '+1-'+phone_num[1:4]+'-'+phone_num[4:7]+'-'+phone_num[7:]

        # check if phone number has 10 digits
        # change the format by adding country code +1, ex- '8473768014' ==> +1-847-376-8014
        elif re.match(r'\d{10}', phone_num):
            phone_num = '+1-'+phone_num[:3]+'-'+phone_num[3:6]+'-'+phone_num[6:]

        # if the phone number contains alphabets, ex- 630ADDPARK ==> +1-630-ADD-PARK
        # doing this because some time phone numbers are advertised like this
        elif re.match(r'[A-Z0-9]{10}', phone_num):
            phone_num = '+1-'+phone_num[:3]+'-'+phone_num[3:6]+'-'+phone_num[6:]

        return phone_num


# uncomment to run test
# OSM_FILE = "osm-files/sample.osm"
#
#
# def test():
#     phone_nums_dict = audit_phone(OSM_FILE)
#     import pprint
#     pprint.pprint(dict(phone_nums_dict))
#
#     for key, phone_num_list in phone_nums_dict.items():
#         if key == 'Incorrect':
#             for phone_num in phone_num_list:
#                 formatted_phone = update_phone(phone_num)
#                 print(phone_num, " ==> ", formatted_phone)
#
#
# if __name__ == '__main__':
#     test()
