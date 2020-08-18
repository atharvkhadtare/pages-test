# -*- coding: utf-8 -*-

from utils import to_json_file, progressBar, download_json_data
from datetime import datetime
from collections import OrderedDict
from os import makedirs
import argparse

version = '1.0.0'
url = "https://api.covid19india.org/states_daily.json"

def create_json_statwise(data, statecode):
	daily_json = {}
	current = {}
	state_parent_dir = '../data/json/statewise/'+statecode + '/'
	makedirs(state_parent_dir, exist_ok=True)
	current["Confirmed"] = current["Recovered"] = current["Deceased"] = current["Active"] = 0
	for record in data['states_daily']:
		record_date = datetime.strptime(record["date"], "%d-%b-%y").strftime("%Y-%m-%d")
		if record_date not in daily_json:
			daily_json[record_date] = {}
			daily_json[record_date]["delta"] = {}
		daily_json[record_date]["delta"][record["status"]] = int(record[statecode])
	daily_json = OrderedDict(sorted(daily_json.items()))
	for (date, values) in daily_json.items():
		delta = values["delta"]
		delta["Active"] = delta["Confirmed"] - delta["Recovered"] - delta["Deceased"]
		for status in ["Confirmed", "Recovered", "Deceased", "Active"]:
			values[status] = current[status] + delta[status]
			current[status] = values[status]
		to_json_file(values, state_parent_dir + date + '.json')
	to_json_file(daily_json, state_parent_dir + 'daily.json')

def main():
	parser = argparse.ArgumentParser(description='Download statewise stats for each day and create json files.', prog='COVID-stats')
	parser.add_argument('-v', '--verbose', help='verbose', action='store_true')
	# parser.add_argument('-p', '--progress_bar', help='show progress bar', action='store_true')
	parser.add_argument('--version', action='version', version='%(prog)s ' + version)
	# args = parser.parse_args()
	data = download_json_data(url)
	# print(data)
	statecodes = list(list(data.values())[0][0].keys())
	statecodes.remove('status')
	statecodes.remove('date')
	# for x in data.values():
	# 	print(x)
	for statecode in progressBar(statecodes):
		create_json_statwise(data, statecode)

if __name__ == "__main__":
    main()
