# Wrangling Open Street Map Data

Choose any area in the world map using [Openstreetmap.org](https://www.openstreetmap.org) and implement the process of data wrangling involving the process of gathering, assessing and cleaning the data. Use python programming skills to wrangle the data programmatically. Learn SQL and apply the provided schema to the project and perform analyses on the data.

### Dataset
**Map Area :** [Chicago, IL, USA](https://en.wikipedia.org/wiki/Chicago)<br/>
> I have been living in Chicago for more than a year and a half to this day, and I am eager to see the contributions made to the map so far. Chicago being one of the information technology hubs in the United States, I am sure I would discover lot of new artifacts about the city.

Dataset extracted from [Openstreetmap.org](ps://www.openstreetmap.org).<br/>
File size : 2.14 Gigabytes <br/>

---

### Project Setup

#### **1. Sample data for Study :**
Since the dataset is huge, I took the 2% sample of the 2.14 GB dataset using [sample_osm.py](https://github.com/rzskhr/Data-Analyst-Nanodegree/blob/master/Projects/P3-Wrangle-OpenStreetMap-Data/sample_osm.py). After taking the small sample of the data, it was easy for me to have a sense of how the data was.<br/>
I performed the below steps after I took the sample:
* Open the sample file in a text editor and see the structure of the data.
* Read the [OpenStreetMap documentation](https://wiki.openstreetmap.org/wiki/OSM_XML) to get the sense of what the given data means.
* Got a sense of how to programmatically traverse through each small elements in the dataset, so that we can extract information from the raw file.

Initially the dataset looked something like this:
```xml
<?xml version="1.0" encoding="UTF-8"?>
<osm>
    <node changeset="2995174" id="235239326" lat="41.941694" lon="-88.325626" timestamp="2009-10-31T07:38:32Z" uid="147510" user="woodpeck_fixbot" version="2" />
    <node changeset="13717267" id="237483575" lat="41.5249438" lon="-88.0360975" timestamp="2012-11-02T00:40:15Z" uid="169600" user="patester24" version="5" />
    <way changeset="11573168" id="163170444" timestamp="2012-05-12T03:58:19Z" uid="674454" user="chicago-buildings" version="1">
        <nd ref="1749207953" />
        <nd ref="1749208467" />
        <nd ref="1749208483" />
        <nd ref="1749207961" />
        <nd ref="1749207953" />
        <tag k="building" v="yes" />
        <tag k="chicago:building_id" v="203624" />
    </way>
</osm>
```

#### **2. Audit the Dataset :**
Since the dataset was in raw xml format I wrote few scripts to audit the dataset so that, I can extract the meaningful information needed. I used [xml.etree.cElementTree](https://docs.python.org/2/library/xml.etree.elementtree.html) of python to traverse the data. Using this module I was able to extract the information from the nodes in the 'osm' file.

After I audited the dataset, I found that there are several problems in the information in the data, specially with phone numbers and street names. Hence I wrote three scripts to handle the problems.
* **Auditing street names :** Wrote the script [audit_street_name.py](https://github.com/rzskhr/Data-Analyst-Nanodegree/blob/master/Projects/P3-Wrangle-OpenStreetMap-Data/audit_street_name.py) which finds the unusual or overabbreviated street names and corrects them using a mapping provided in the code. <br/>
For example: "South Wacker Dr" to "South Wacker Drive"
```python
# list of expected street names
expected = ["Street", "Avenue", "Boulevard", "Drive", "Court", "Ct", "Place", "Square", "Lane", "Road",
"Trail", "Parkway", "Commons", "Park", "Broadway", "Circle", "Highway", "Trail",
"Way", "West", "North", "Terrace", "Plaza", "Market"]

# mapping the incorrect street names to the correct ones
STREET_MAPPING = {"Ave"    : "Avenue",
                  "Ave."   : "Avenue",
                  "Blvd."  : "Boulevard",
                  "Blvd"   : "Boulevard",
                  "Cir"    : "Circle",
                  "Dr"     : "Drive",
                  "Ln"     : "Lane",
                  "N."     : "North",
                  "Pkwy"   : "Parkway",
                  "Rd"     : "Road",
                  "Rd."    : "Road",
                  "St"     : "Street",
                  "St."    : "Street",
                  "Trl"    : "Trail"
                  }
```
* **Auditing Phone Numbers :** There was a huge inconsistency in the phone number format which was tough to get right at the first glance and confusion at sometimes. Using the script [audit_phone.py](https://github.com/rzskhr/Data-Analyst-Nanodegree/blob/master/Projects/P3-Wrangle-OpenStreetMap-Data/audit_phone.py), I captured all the phone numbers and verified using a [regular expression](https://github.com/rzskhr/Data-Analyst-Nanodegree/blob/e4ddd04f2b4e73992a660019bb7eb313769e23b1/Projects/P3-Wrangle-OpenStreetMap-Data/audit_phone.py#L11) and made all the phone numbers in one single format (+1-312-999-9999).<br/>
For example: '(847) 376-8014' to '+1-847-376-8014' or '630-393-9609' to '+1-630-393-9609'
```python
# precompiled regular expressions
phone_num_re = re.compile(r'\+1-\d{3}-\d{3}-\d{4}')     # matches the format +1-312-999-9999
```

* **Auditing postal-code :** Similar to above two scripts I wrote a script [audit_postcode.py](https://github.com/rzskhr/Data-Analyst-Nanodegree/blob/master/Projects/P3-Wrangle-OpenStreetMap-Data/audit_postcode.py) to find the unusual patterns in the postal-code, but fortunately there wasn't a significant number of problems in the postal-code so that we can format it for the database.


#### **3. Processing the OSM file for data base :**
After auditing the data we prepare the 4 csv files for the database, as per the provided [schema](https://github.com/rzskhr/Data-Analyst-Nanodegree/blob/master/Projects/P3-Wrangle-OpenStreetMap-Data/schema.py). We pass the raw osm datafile to the [data_wrangling.py](https://github.com/rzskhr/Data-Analyst-Nanodegree/blob/master/Projects/P3-Wrangle-OpenStreetMap-Data/data-wrangling.py) script to process the data.

This script contains two main function [```shape_element ( )```](https://github.com/rzskhr/Data-Analyst-Nanodegree/blob/99eaff92049b8f6d04cd478acc97be499d07f825/Projects/P3-Wrangle-OpenStreetMap-Data/data-wrangling.py#L55) and [```process_map ( )```](https://github.com/rzskhr/Data-Analyst-Nanodegree/blob/99eaff92049b8f6d04cd478acc97be499d07f825/Projects/P3-Wrangle-OpenStreetMap-Data/data-wrangling.py#L155) using which we prepare the csv files for the database.

* **```shape_element ( )``` :** In this function we pass one element at a time using the method [```fetch_element ()```](https://github.com/rzskhr/Data-Analyst-Nanodegree/blob/99eaff92049b8f6d04cd478acc97be499d07f825/Projects/P3-Wrangle-OpenStreetMap-Data/sample_osm.py#L23), and process the element as per the schema. There are two main tags which we process in this function, 'node' and 'way' tags. After processing the tags the fucntion returns a dictionary mapping the relevant information which matches the schema and can be written to the csv file. The dictionary returned from this function has the below format.

```python
# for node tags
{'node': node_attributes, 'node_tags': inner_tags}

# for way tags
{'way': way_attributes, 'way_nodes': way_nodes, 'way_tags': inner_tags}
```

* **```process_map ( )``` :** This function validates the dictionary obtained from the ```shape_element ( )``` function against the schema and writes them to the respective csv files. The function outputs 4 csv files in the same location as the script.
```
nodes.csv
nodes_tags.csv
ways.csv
ways_nodes.csv
ways_tags.csv
```

> After processing the entire dataset of size 2.14 GB, here are the csv files and their size I got:
```
$ ls -ls | awk '{print$10,"------" ,$6/1000000,"MB"}'
nodes.csv ------ 787.317 MB
nodes_tags.csv ------ 13.5996 MB
ways.csv ------ 82.5706 MB
ways_nodes.csv ------ 254.504 MB
ways_tags.csv ------ 227.41 MB
```

#### **4. Load the CSV files to the SQLite3 Database file :**
After obtaining the csv files as per the schema I loaded them into a sqlite3 database file using the script [create-sqlite3-database.py
](https://github.com/rzskhr/Data-Analyst-Nanodegree/blob/master/Projects/P3-Wrangle-OpenStreetMap-Data/create-sqlite3-database.py).

> After loading the files to database here are the stats for the entire dataset:
```
$ cd ..
$ ls -ls | awk '{print$10,"------" ,$6/1000000,"MB"}'
chicago_osm_sqlite3_database.db ------ 1249.36 MB
```


#### **5. Data Analysis :**
