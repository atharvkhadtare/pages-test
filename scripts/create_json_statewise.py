# -*- coding: utf-8 -*-

import requests
import json
from datetime import datetime
from collections import OrderedDict
import os
from time import sleep

url = {}
url = "https://api.covid19india.org/states_daily.json"

def progressBar(iterable, prefix='Progress: ', suffix='Complete', decimals=1, length=50, fill='█', printEnd="\r"):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    total = len(iterable)
    # Progress Bar Printing Function

    def printProgressBar(iteration):
        percent = ("{0:." + str(decimals) + "f}").format(100 *
                                                         (iteration / float(total)))
        filledLength = int(length * iteration // total)
        bar = fill * filledLength + '-' * (length - filledLength)
        print('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix), end=printEnd)

    # Initial Call
    printProgressBar(0)
    # Update Progress Bar
    for i, item in enumerate(iterable):
        yield item
        printProgressBar(i + 1)
    # Print New Line on Complete
    print()

def download_data(url):
	r = requests.get(url)
	return r.json()

def create_json_statwise(data, statecode):
	daily_json = {}
	current = {}
	state_parent_dir = '../data/json/statewise/'+statecode + '/'
	os.makedirs(state_parent_dir, exist_ok=True)
	current["Confirmed"] = 0
	current["Recovered"] = 0
	current["Deceased"] = 0
	current["Active"] = 0
	for record in data['states_daily']:
		# daily_json[i["date"]]
		record_date = datetime.strptime(record["date"], "%d-%b-%y").strftime("%Y-%m-%d")
		if record_date not in daily_json:
			daily_json[record_date] = {}
			daily_json[record_date]["delta"] = {}
		daily_json[record_date]["delta"][record["status"]] = int(record[statecode])
		# print(i["date"] + "\t\t" + i["status"])
	daily_json = OrderedDict(sorted(daily_json.items()))
	for (date, values) in daily_json.items():
		delta = values["delta"]
		delta["Active"] = delta["Confirmed"] - delta["Recovered"] - delta["Deceased"]
		for status in ["Confirmed", "Recovered", "Deceased", "Active"]:
			values[status] = current[status] + delta[status]
			current[status] = values[status]
		with open(state_parent_dir + date +'.json', 'w', encoding='utf-8') as f:
			json.dump(values, f, ensure_ascii=False, indent=4)
	with open('../data/json/statewise/'+statecode+'/daily.json', 'w', encoding='utf-8') as f:
		json.dump(daily_json, f, ensure_ascii=False, indent=4)

data = download_data(url)
statecodes = list(list(data.values())[0][0].keys())
statecodes.remove('status')
statecodes.remove('date')
# for x in data.values():
# 	print(x)
for statecode in progressBar(statecodes):
	create_json_statwise(data, statecode)
# for statecode in statecodes:
# 	create_json_statwise(data, statecode)
# print( date.date()) 
