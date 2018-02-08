# Wrangling Open Street Map Data

Choose any area in the world map using [Openstreetmap.org](https://www.openstreetmap.org) and implement the process of data wrangling involving the process of gathering, assessing and cleaning the data. Use python programming skills to wrangle the data programmatically. Learn SQL and apply the provided schema to the project and perform analyses on the data.

### Dataset
**Map Area :** [Chicago, IL, USA](https://en.wikipedia.org/wiki/Chicago)<br/>
> I have been living in Chicago for more than a year and a half to this day, and I am eager to see the contributions made to the map so far. Chicago being one of the information technology hubs in the United States, I am sure I would discover lot of new artifacts about the city.

Dataset extracted from [Openstreetmap.org](ps://www.openstreetmap.org).<br/>
File size : 2.14 Gigabytes <br/>

### Project Setup
I divided my work in to few iterative chunks.
#### **Sample data for Study :**
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

#### Audit the Dataset
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
