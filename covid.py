import requests, json
import numpy as np
from matplotlib import pyplot as plt

# Notes:
# - For piping to jq, use json.dumps

# with open("covid.json", "w") as outfile:
#     response = requests.get("https://opendata.ecdc.europa.eu/covid19/casedistribution/json/")
#     response.raise_for_status()
#     d = json.loads(response.text)
#     json.dump(d, outfile)

with open("covid.json", "r") as infile:
    d = json.load(infile)
records = d['records']
print('%d Einträge vorhanden' % len(records))

def nice(r):
    return {
        "Land": r['geoId'], 
        "Datum": r['dateRep'], 
        "Fälle": r['cases'],
        "Todesfälle": r['deaths']
    }

records = [ nice(r) for r in records ]
print('%d Einträge für vorhanden' % len(records))
records = [ r for r in records if r['Land']=='DE' ]
print('%d Einträge für DE vorhanden' % len(records))
#print(json.dumps(records[:5], indent=4))
cases = [ records[i]['Fälle'] for i in range(len(records))]
deaths = [ records[i]['Todesfälle'] for i in range(len(records))]
cases = list(reversed(cases))
deaths = list(reversed(deaths))
#print(cases[-5:len(cases)])

plt.plot(cases)
plt.plot(deaths)
plt.show()