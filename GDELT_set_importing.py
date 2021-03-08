import csv, json

csvFilePath = 'GDELT.MASTERREDUCEDV2.TXT'
csvfile = open(csvFilePath, 'r')

jsonFilePath = 'GDELT.MASTERREDUCEDV2.json'
jsonfile = open(jsonFilePath, 'w')

fieldnames = ("Date", "Source", "Target", "CAMEOCode", "NumEvents", "NumArts", "QuadClass", "Goldstein", "SourceGeoType", "SourceGeoLat", "SourceGeoLong", "TargetGeoType", "TargetGeoLat", "TargetGeoLong", "ActionGeoType", "ActionGeoLat", "ActionGeoLong")
reader = csv.DictReader(csvfile, fieldnames)
for row in reader:
    json.dump(row, jsonfile)
    jsonfile.write('\n')
