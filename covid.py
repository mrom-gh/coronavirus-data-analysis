"""Get covid cases from the ECDC API and plot selections of the data."""
# Notes:
# - For piping to jq, use json.dumps

import requests
import json
import numpy as np
from matplotlib import pyplot as plt

# TODO: Improve data acquision time
# TODO: Get last date from file / records
# TODO Plot: Add smoothing
# TODO Plot: Plot deaths as negative numbers
# TODO: Calculate CFR
# TODO: Calculate per capita cases
# TODO API: Get data by age (RKI needed)
# TODO API: Get data by region (RKI needed)
# TODO API: Normalize to number of tests (RKI needed)


URLS = {
    'ECDC':"https://opendata.ecdc.europa.eu/covid19/casedistribution/json/"
}
FILE_FORMATS = {'ECDC':'json'}


class CovidData:

    def __init__(self, source, send_request):
        self.source = source
        self.response = None
        self.filename = 'covid_' + self.source + '.' + FILE_FORMATS[self.source]
        if send_request:
            self._get_data_from_API()
            self._save_data_to_file()
        self.records = None

    def _get_data_from_API(self):
        print(f"\nSource: {self.source}")
        self.response = requests.get(URLS[self.source])
        print(f"HTTP GET - Status-Code: {self.response.status_code}\n")

    def _save_data_to_file(self):
        print(f"Filename: {self.filename}\n")
        with open(self.filename, "w") as outfile:
            d = json.loads(self.response.text)  # {'records':[...], ...}
            self.records = d['records']
            json.dump(d, outfile)

    def get_records_from_file(self):
        with open(self.filename, "r") as infile:
            d = json.load(infile)
        self.records = d['records']  # [dict_day1, dict_day2, ...]
        print('%d Einträge vorhanden\n' % len(self.records))

    def format_records(self):
        for i, record in enumerate(self.records):
            self.records[i] = {
                "Land": record['geoId'],
                "Datum": record['dateRep'],
                "Fälle": record['cases'],
                "Todesfälle": record['deaths']
            }

    def select_records(self, criteria):
        print('Criteria: ', end='')
        for key, value in criteria.items():
            self.records = [r for r in self.records if r[key]==value]
            print(key, '=', value, end='   ')
        print('\n%d Einträge vorhanden' % (len(self.records)))

    def plot_histo_alt(self):
        #print(json.dumps(self.records[:5], indent=4))
        cases = np.array(list(reversed([r['Fälle'] for r in self.records])))
        deaths = np.array(list(reversed([r['Todesfälle'] for r in self.records])))
        deaths = (-1)*deaths
        
        _, ax1 = plt.subplots()
        ax2 = ax1.twinx()
        ax1.plot(cases, 'b')
        ax2.plot(deaths, 'g')
        
        ax1.set_xlabel('Tage seit Beginn der Aufzeichnung')
        ax1.set_ylabel('Fälle', color='b')
        ax2.set_ylabel('Todesfälle', color='g')
        
        ymin2 = ax2.get_ylim()[0]  # use default for lower ylimit
        ax2.set_ylim(ymin2, max(deaths)*3)  # scale upper ylimit by hand
        plt.show()

    def plot_histo(self):
        cases = np.array(list(reversed([r['Fälle'] for r in self.records])))
        deaths = np.array(list(reversed([r['Todesfälle'] for r in self.records])))
        deaths = (-1)*deaths
        
        plt.plot(cases)
        plt.plot(deaths)
        plt.xlabel('Tage seit Beginn der Aufzeichnung')
        plt.ylabel('Anzahl')
        plt.show()


cd = CovidData('ECDC', send_request=False)
cd.get_records_from_file()
cd.format_records()
criteria = {'Land':'DE'}
cd.select_records(criteria)
cd.plot_histo()