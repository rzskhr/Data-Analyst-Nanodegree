#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""

"""


# All the imports done here
import xml.etree.cElementTree as Et
from collections import defaultdict
import re


# CONSTANTS

# file path
OSM_FILE = "sample.osm"

# precompiled regular expressions
lower = re.compile(r'^([a-z]|_)*$')
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
problem_chars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')


def shape_element():
    pass


def process_map():
    pass
