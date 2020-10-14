# Notes:
# - For piping to jq, use json.dumps

import requests, json
import numpy as np
from matplotlib import pyplot as plt

# TODO: Improve data acquision time
# TODO: Refactor completely into functions
# TODO: Get last date from file / records
# TODO: Add second y-axis in histogram
# TODO: Add smoothing


def save_data_to_file(filename):
    with open(filename, "w") as outfile:
        response = requests.get("https://opendata.ecdc.europa.eu/covid19/casedistribution/json/")
        print(f"HTTP GET - Status-Code: {response.status_code}")
        d = json.loads(response.text)
        json.dump(d, outfile)

def get_records_from_file(filename):
    with open("covid.json", "r") as infile:
        d = json.load(infile)
    records =  d['records']
    print('%d Einträge vorhanden' % len(records))
    return records

def nice(record):
    return {
        "Land": record['geoId'], 
        "Datum": record['dateRep'], 
        "Fälle": record['cases'],
        "Todesfälle": record['deaths']
    }

def get_nice_records_from_DE(filename):
    records = get_records_from_file(filename)
    records = [ nice(r) for r in records ]
    records = [ r for r in records if r['Land']=='DE' ]
    print('%d Einträge für DE vorhanden' % len(records))
    return records


#save_data_to_file("covid.json")
records = get_nice_records_from_DE("covid.json")

#print(json.dumps(records[:5], indent=4))
cases = [ records[i]['Fälle'] for i in range(len(records))]
deaths = [ records[i]['Todesfälle'] for i in range(len(records))]
cases = list(reversed(cases))
deaths = list(reversed(deaths))
#print(cases[-5:len(cases)])

plt.plot(cases)
plt.plot(deaths)
plt.show()
