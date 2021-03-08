import csv, json
from rdflib import Graph, URIRef, BNode, Literal, Namespace, XSD
from rdflib.namespace import RDFS, RDF, FOAF, SDO
import matplotlib.pyplot as plt
import matplotlib.lines as lines
from mpl_toolkits.basemap import Basemap

with open('GDELT.MASTERREDUCEDV2-1.json') as f:
    starter_data = json.load(f)

for i in starter_data:
    print(i)

# Since I am exploring the events pertaining USA, China and Russia, I filter the records having them

usa = [x for x in starter_data if x['Target'] == "USA"]
chn = [x for x in starter_data if x['Target'] == "CHN"]
rus = [x for x in starter_data if x['Target'] == "RUS"]
data = usa + chn + rus

for i in data:
    print(i)

# Filtering the attributes that I need

for i in data:
    i.pop('Date')
    i.pop('CAMEOCode')
    i.pop('NumEvents')
    i.pop('NumArts')
    i.pop('QuadClass')
    i.pop('SourceGeoType')
    i.pop('TargetGeoType')
    i.pop('TargetGeoLat')
    i.pop('TargetGeoLong')
    i.pop('ActionGeoType')

for i in data:
    print(i)

# Cleaning the data

j = 0
for i in data:
    if type(i['SourceGeoLat']) == type(None) or type(i['SourceGeoLong']) == type(None):
        del data[j]
    j += 1

# Adding URIs to the Resources

j = 0
for i in data:
    if type(i['SourceGeoLat']) == type(None) or type(i['SourceGeoLong']) == type(None):
        del data[j]
    j += 1

# Adding URIs to the Resouces
for i in data:
    if i['Target'].__contains__('USA'):
        i['Target'] = 'https://www.dbpedia.org/resource/United_States'
    elif i['Target'].__contains__('RUS'):
        i['Target'] = 'https://www.dbpedia.org/resource/Russia'
    elif i['Target'].__contains__('CHN'):
        i['Target'] = 'https://www.dbpedia.org/resource/China'

    if i['Source'].__contains__('USA'):
        i['Source'] = 'https://www.dbpedia.org/resource/United_States'
    elif i['Source'].__contains__('RUS'):
        i['Source'] = 'https://www.dbpedia.org/resource/Russia'
    elif i['Source'].__contains__('CHN'):
        i['Source'] = 'https://www.dbpedia.org/resource/China'
    elif i['Source'].__contains__('PRK'):
        i['Source'] = 'https://www.dbpedia.org/resource/North_Korea'
    elif i['Source'].__contains__('PRY'):
        i['Source'] = 'https://www.dbpedia.org/resource/Paraguay'
    elif i['Source'].__contains__('PSE'):
        i['Source'] = 'https://www.dbpedia.org/resource/Palestinian_territories'
    elif i['Source'].__contains__('PTY'):
        i['Source'] = 'https://www.dbpedia.org/resource/Israel'
    elif i['Source'].__contains__('SAU'):
        i['Source'] = 'https://www.dbpedia.org/resource/Saudi_Arabia'
    elif i['Source'].__contains__('SRB'):
        i['Source'] = 'https://www.dbpedia.org/resource/Serbia'
    elif i['Source'].__contains__('TJK'):
        i['Source'] = 'https://www.dbpedia.org/resource/Tajikistan'
    elif i['Source'].__contains__('TUR'):
        i['Source'] = 'https://www.dbpedia.org/resource/Turkey'
    elif i['Source'].__contains__('UKR'):
        i['Source'] = 'https://www.dbpedia.org/resource/Ukraine'
    elif i['Source'].__contains__('ukr'):
        i['Source'] = 'https://www.dbpedia.org/resource/Ukraine'
    elif i['Source'].__contains__('VNM'):
        i['Source'] = 'https://www.dbpedia.org/resource/Vietnam'
    elif i['Source'].__contains__('ZMB'):
        i['Source'] = 'https://www.dbpedia.org/resource/Zambia'
    elif i['Source'].__contains__('ZWE'):
        i['Source'] = 'https://www.dbpedia.org/resource/Zimbabwe'
    elif i['Source'].__contains__('REF'):
        i['Source'] = 'https://www.dbpedia.org/resource/Refugee'
    elif i['Source'].__contains__('SEP'):
        i['Source'] = 'https://www.dbpedia.org/resource/Thailand'
    elif i['Source'].__contains__('tib'):
        i['Source'] = 'https://www.dbpedia.org/resource/Tibet'
    elif i['Source'].__contains__('TWN'):
        i['Source'] = 'https://www.dbpedia.org/resource/Taiwan'
    elif i['Source'].__contains__('SPY'):
        i['Source'] = 'https://www.dbpedia.org/resource/United_States'
    elif i['Source'].__contains__('SWE'):
        i['Source'] = 'https://www.dbpedia.org/resource/Sweden'
    elif i['Source'].__contains__('TKM'):
        i['Source'] = 'https://www.dbpedia.org/resource/Turkmenistan'

for i in data:
    print(i)

# Creating the graph

g = Graph()

for i in data:
    source = URIRef(i['Source'])

    if not (g.__contains__((source, RDF.type, SDO.Thing))):
        g.add((source, RDF.type, SDO.Thing))
        sourceLat = Literal(i['SourceGeoLat'])
        g.add((source, SDO.latitude, sourceLat))
        sourceLong = Literal(i['SourceGeoLong'])
        g.add((source, SDO.longitude, sourceLong))

    target = URIRef(i['Target'])

    if not (g.__contains__((source, RDF.type, SDO.Thing))):
        g.add((target, RDF.type, SDO.Thing))
        targetLat = Literal(i['ActionGeoLat'])
        g.add((target, SDO.latitude, targetLat))
        targetLong = Literal(data[0]['ActionGeoLong'])
        g.add((target, SDO.longitude, targetLong))

    g.add((source, SDO.object, target))

print(g.serialize(format='turtle').decode('utf-8'))
g.serialize(destination='C:/Users/sciev/OneDrive/Desktop/PyCharm Projects/WBS_GDELT/GDELT-graph.ttl', format='turtle')

# SPARQL query to find the attacks pertaining to China, and extract the coordinates

resultsC = g.query("""
SELECT ?lat ?long
WHERE {
  ?s <https://schema.org/object> <https://www.dbpedia.org/resource/China> .
  ?s <https://schema.org/latitude> ?lat .
  ?s <https://schema.org/longitude> ?long .

  }
""")

# Drawing the map containing information of attacks only where China is relevant

plt.figure(figsize=(20,10))
m = Basemap()
m.shadedrelief()

latC = 35.8617
lonC = 104.1954
xptC,yptC = m(lonC,latC)
m.plot(xptC,yptC,'ro')

for row in resultsC:
  lat = float(row.asdict()['lat'])
  lon = float(row.asdict()['long'])
  xpt,ypt = m(lon,lat)
  m.plot([xpt, xptC], [ypt, yptC], 'r.') # only dots

plt.savefig('WBS_GDELT_web/chn.png', bbox_inches='tight')
plt.show()

# SPARQL query to find the attacks pertaining to Russia, and extract the coordinates

resultsR = g.query("""
SELECT ?lat ?long
WHERE {
  ?s <https://schema.org/object> <https://www.dbpedia.org/resource/Russia> .
  ?s <https://schema.org/latitude> ?lat .
  ?s <https://schema.org/longitude> ?long .
  }
""")

# Drawing the map containing information of attacks only where Russia is relevant

plt.figure(figsize=(20,10))
m = Basemap()
m.shadedrelief()

latR = 61.5240
lonR = 105.3188
xptR,yptR = m(lonR,latR)
m.plot(xptR,yptR,'ro')

for row in resultsR:
  lat = float(row.asdict()['lat'])
  lon = float(row.asdict()['long'])
  xpt,ypt = m(lon,lat)
  m.plot([xpt, xptR], [ypt, yptR], 'r.') # only dots

plt.savefig('WBS_GDELT_web/rus.png', bbox_inches='tight')
plt.show()

# SPARQL query to find the attacks pertaining to USA, and extract the coorsinates

resultsU = g.query("""
SELECT ?lat ?long
WHERE {
  ?s <https://schema.org/object> <https://www.dbpedia.org/resource/United_States> .
  ?s <https://schema.org/latitude> ?lat .
  ?s <https://schema.org/longitude> ?long .
  }
""")

# Drawing the map containing information of attacks only where USA is relevant

plt.figure(figsize=(20,10))
m = Basemap()
m.shadedrelief()

latU = 37.0902
lonU = -95.7129
xptU,yptU = m(lonU,latU)
m.plot(xptU,yptU,'ro')

for row in resultsU:
  lat = float(row.asdict()['lat'])
  lon = float(row.asdict()['long'])
  xpt,ypt = m(lon,lat)
  m.plot([xpt, xptU], [ypt, yptU], 'r.') # only dots


plt.savefig('WBS_GDELT_web/usa.png', bbox_inches='tight')
plt.show()

plt.figure(figsize=(20,10))
m = Basemap()
m.shadedrelief()
plt.savefig('WBS_GDELT_web/none.png', bbox_inches='tight')
plt.show()

plt.figure(figsize=(20,10))
m = Basemap()
m.shadedrelief()

latC = 35.8617
lonC = 104.1954
xptC,yptC = m(lonC,latC)
m.plot(xptC,yptC,'ro')

for row in resultsC:
  lat = float(row.asdict()['lat'])
  lon = float(row.asdict()['long'])
  xpt,ypt = m(lon,lat)
  m.plot([xpt, xptC], [ypt, yptC], 'r.')

latR = 61.5240
lonR = 105.3188
xptR,yptR = m(lonR,latR)
m.plot(xptR,yptR,'go')

for row in resultsR:
  lat = float(row.asdict()['lat'])
  lon = float(row.asdict()['long'])
  xpt,ypt = m(lon,lat)
  m.plot([xpt, xptR], [ypt, yptR], 'g.')

latU = 37.0902
lonU = -95.7129
xptU,yptU = m(lonU,latU)
m.plot(xptU,yptU,'bo')

for row in resultsU:
  lat = float(row.asdict()['lat'])
  lon = float(row.asdict()['long'])
  xpt,ypt = m(lon,lat)
  m.plot([xpt, xptU], [ypt, yptU], 'b.')

plt.savefig('WBS_GDELT_web/all.png', bbox_inches='tight')
plt.show()

plt.figure(figsize=(20,10))
m = Basemap()
m.shadedrelief()

latC = 35.8617
lonC = 104.1954
xptC,yptC = m(lonC,latC)
m.plot(xptC,yptC,'ro')

for row in resultsC:
  lat = float(row.asdict()['lat'])
  lon = float(row.asdict()['long'])
  xpt,ypt = m(lon,lat)
  m.plot([xpt, xptC], [ypt, yptC], 'r-', linewidth=1)

latR = 61.5240
lonR = 105.3188
xptR,yptR = m(lonR,latR)
m.plot(xptR,yptR,'go')

for row in resultsR:
  lat = float(row.asdict()['lat'])
  lon = float(row.asdict()['long'])
  xpt,ypt = m(lon,lat)
  m.plot([xpt, xptR], [ypt, yptR], 'g-', linewidth=1)

latU = 37.0902
lonU = -95.7129
xptU,yptU = m(lonU,latU)
m.plot(xptU,yptU,'bo')

for row in resultsU:
  lat = float(row.asdict()['lat'])
  lon = float(row.asdict()['long'])
  xpt,ypt = m(lon,lat)
  m.plot([xpt, xptU], [ypt, yptU], 'b-', linewidth=1)

plt.savefig('WBS_GDELT_web/all_lines.png', bbox_inches='tight')
plt.show()
