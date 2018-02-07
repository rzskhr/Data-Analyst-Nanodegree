#!/usr/bin/env python
# -*- coding: utf-8 -*-

# All the imports done here
import xml.etree.cElementTree as Et
import os


# constants
OSM_FILE = "/Users/Raj/Root/GitHub/__Datasets__/OSM/chicago_illinois.osm"

# take every n-th top element
take_every_nth_element = 51

if take_every_nth_element > 49:
    SAMPLE_FILE = "osm-files/sample.osm"
else:
    SAMPLE_FILE = "/Users/Raj/Root/GitHub/__Datasets__/OSM/processed-osm/sample.osm"

DEFAULT_TAGS = ('node', 'way', 'relation')


def fetch_element(osmfile, tags=DEFAULT_TAGS):
    """
    get the element if it is right type of tag

    :param osmfile: osmfile
    :param tags: type of tags to consider
    :return: nothing, used to get the element to write in to sample file
    """
    print("fetch_element from sample_osm.py called")
    print("fetching elements from file : ", osmfile, "having tags : ", tags, ".\n")

    # iterate over start and end tags
    context = iter(Et.iterparse(osmfile, events=('start', 'end')))

    # capture the root node that is <osm> element
    _, root = next(context)

    for event, element in context:
        if event == 'end' and element.tag in tags:
            yield element   # https://docs.python.org/3/reference/expressions.html#yieldexpr
            root.clear()


def sample_file(osm_file=OSM_FILE, sample_file=SAMPLE_FILE):
    # dumping the data to sample file
    with open(sample_file, 'wb') as f:
        # write the first line in the xml
        # adding the bytes object type, as we are opening the file in bytes mode
        f.write(b'<?xml version="1.0" encoding="UTF-8"?>\n')
        f.write(b'<osm>\n ')      # opening tag

        # write every nth element using sample_element
        print("Sampling large OSM file.")
        print("Raw file size:  ", os.stat(osm_file).st_size/1000000, "Megabytes\n")
        for i, element in enumerate(fetch_element(osm_file)):
            if i % take_every_nth_element == 0:
                f.write(Et.tostring(element, encoding='utf-8'))
        # closing the osm tag
        f.write(b'</osm>')
    f.close()


if __name__ == '__main__':
    user_input = input("Type yes if you want to sample osm file, \
    \nelse type anything and hit return.... :\n")
    if user_input == 'yes':
        print("##### sampling ....")
        sample_file()
        print("##### finished sampling.\n")
        print("Sampled file at location: ", SAMPLE_FILE.upper())
        print("Sample file size: ", os.stat(SAMPLE_FILE).st_size/1000000, "Megabytes")
    else:
        exit(1)
