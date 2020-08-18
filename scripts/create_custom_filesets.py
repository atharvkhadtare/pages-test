import json
from datetime import datetime, timedelta
from os import makedirs, path
from utils import to_json_file
from copy import deepcopy

custom_parent_dir = '../data/static-data/custom_sets/'
custom_set = '/mumbai_thane'

def list_source_dirs(custom_path):
	with open(custom_path + '.json', "r") as custom_json_file:
		sources =  json.load(custom_json_file)
	sources_list = set()
	if "districts" in sources:
		for state, values in sources["districts"].items():
			for district in values:
				sources_list.add("../data/json/districtwise/" + state + "/" + district + "/")
	return sources_list


def create_daily_files(custom_set, sources_list, custom_template_json):
	date = datetime.today()
	force_refresh = 5
	max_days = (date - datetime.strptime("2020-02-29", "%Y-%m-%d")).days
	for i in range(max_days):
		print(date.strftime("../data/json/custom_sets/" + custom_set + "/%Y-%m-%d.json"), end=" = ")
		current_day_report = deepcopy(custom_template_json)
		for source in sources_list:
			if path.exists(date.strftime(source + '%Y-%m-%d.json')):
				with open(date.strftime(source + '%Y-%m-%d.json'), "r") as custom_json_file:
					source_report = json.load(custom_json_file)
				current_day_report = add_daily_reports(current_day_report, source_report)
				print(date.strftime(' + ' + source + '%Y-%m-%d.json'), end="")
			to_json_file(current_day_report, date.strftime("../data/json/custom_sets" + custom_set + "/%Y-%m-%d.json"))
		print()
		# try:
		# 	if os.path.exists()
		# 	data = download_json_data(date.strftime("https://api.covid19india.org/v4/data-%Y-%m-%d.json"))
		# 	to_json_file(data, date.strftime("../data/raw/daily/%Y-%m-%d.json"))
		# except:
		# 	pass
		date = date - timedelta(days=1)

def add_daily_reports(json1, json2):
	for count_type in ['total', 'delta']:
		for status in ['confirmed', 'deceased', 'recovered', 'active']:
			json1[count_type][status] += json2[count_type][status]
	return json1


def main():
	with open('../data/static-data/custom.json', "r") as custom_template_file:
		custom_template_json = json.load(custom_template_file)
	sources_list = list_source_dirs(custom_parent_dir + custom_set)
	makedirs("../data/json/custom_sets/" + custom_set, exist_ok=True)
	create_daily_files(custom_set, sources_list, custom_template_json)
	print(sources_list)

if __name__ == "__main__":
	main()
