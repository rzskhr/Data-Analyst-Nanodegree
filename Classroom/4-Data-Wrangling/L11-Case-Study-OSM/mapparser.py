#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Your task is to use the iterative parsing to process the map file and
find out not only what tags are there, but also how many, to get the
feeling on how much of which data you can expect to have in the map.
Fill out the count_tags function. It should return a dictionary with the
tag name as the key and number of times this tag can be encountered in
the map as value.

Note that your code will be tested with a different data file than the 'example.osm'
"""
import xml.etree.cElementTree as Et
import pprint


def count_tags(filename):
    my_dict = {}
    with open(filename, 'rb') as f:
        for i, j in Et.iterparse(f):
            if j.tag in my_dict:
                my_dict[j.tag] += 1
            else:
                my_dict[j.tag] = 1
    f.close()
    return my_dict


def test():
    print(count_tags('example.xml'))
    """
    tags = count_tags('example.osm')
    pprint.pprint(tags)
    assert tags == {'bounds': 1,
                     'member': 3,
                     'nd': 4,
                     'node': 20,
                     'osm': 1,
                     'relation': 1,
                     'tag': 7,
                     'way': 1}
    """


if __name__ == "__main__":
    test()
