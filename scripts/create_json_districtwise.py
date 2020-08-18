# -*- coding: utf-8 -*-

from utils import to_json_file, progressBar, download_json_data
import json
from datetime import datetime, timedelta
from collections import OrderedDict
from os import makedirs, path, listdir
import argparse
from time import sleep

version = '1.0.0'
url = "https://api.covid19india.org/v4/data-YYYY-MM-DD.json"
state_district_map = dict()
state_parent_dir = '../data/json/districtwise/'

def download_raw_daily_data():
	force_refresh = 1
	date = datetime.today()
	makedirs("../data/raw/daily/", exist_ok=True)
	print("Downloading raw daily data\nForce Refreshed:")
	for i in progressBar(range(force_refresh)):
		# sleep(0.2)
		# print("FORCE: " + date.strftime("https://api.covid19india.org/v4/data-%Y-%m-%d.json"))
		try:
			data = download_json_data(date.strftime("https://api.covid19india.org/v4/data-%Y-%m-%d.json"))
			to_json_file(data, date.strftime("../data/raw/daily/%Y-%m-%d.json"))
		except:
			pass
		date = date - timedelta(days=1)

	max_days = (date - datetime.strptime("2020-02-29", "%Y-%m-%d")).days
	print("If not cached:")
	for i in progressBar(range(max_days)):
		# sleep(0.05)
		if not path.isfile(date.strftime("../data/raw/daily/%Y-%m-%d.json")):
			try:
				# print("DOWNLOADING: " + date.strftime("https://api.covid19india.org/v4/data-%Y-%m-%d.json"))
				data = download_json_data(date.strftime("https://api.covid19india.org/v4/data-%Y-%m-%d.json"))
				to_json_file(data, date.strftime("../data/raw/daily/%Y-%m-%d.json"))
				# break
				pass
			except:
				pass
		else:
			# print("CACHED: " + date.strftime("https://api.covid19india.org/v4/data-%Y-%m-%d.json"))
			pass
		date = date - timedelta(days=1)
	return 0

def process_raw_daily_files():
	file_list = sorted(listdir("../data/raw/daily/"))
	print("Processing raw daily files")
	for filename in progressBar(file_list):
		if filename == "YYYY-MM-DD.json":
			continue
		# print(filename)
		with open("../data/raw/daily/" + filename) as json_file:
			json_data = json.load(json_file)
			for state, values in json_data.items():
				if state not in state_district_map:
					# print("\tadd " + state)
					state_district_map[state] = set()
				if "districts" in values:
					for district, values in values["districts"].items():
						for count_type in ['total', 'delta']:
							if count_type not in values:
								values[count_type] = dict()
							for status in ['confirmed', 'deceased', 'recovered']:
								if status not in values[count_type]:
									values[count_type][status] = 0
							values[count_type]['active'] = values[count_type]['confirmed'] - values[count_type]['deceased'] - values[count_type]['recovered']
						if district not in state_district_map[state]:
							state_district_map[state].add(district)
							open_daily_district_file(filename.split('.')[0], values, state, district)
						else:
							add_to_daily_district_file(
								filename.split('.')[0], values, state, district)
						json_filepath = '../data/json/districtwise/' + state + '/' + district + '/' + filename
						to_json_file(values, json_filepath)
	close_all_daily_district_files()
	# print(state_district_map)
	pass

def open_daily_district_file(date, json_data, statecode, district):
	district_parent_dir = '../data/json/districtwise/' + statecode + '/' + district
	makedirs(district_parent_dir, exist_ok=True)
	with open(district_parent_dir + '/daily.json', 'w', encoding='utf-8') as json_file:
		json_file.write("{\n" + "\"" + date + "\": ")
		json.dump(json_data, json_file, ensure_ascii=False, indent=4)

def add_to_daily_district_file(date, json_data, statecode, district):
	district_parent_dir = '../data/json/districtwise/' + statecode + '/' + district
	with open(district_parent_dir + '/daily.json', 'a', encoding='utf-8') as json_file:
		json_file.write(",\n" + "\"" + date +"\": ")
		json.dump(json_data, json_file, ensure_ascii=False, indent=4)

def close_all_daily_district_files():
	state_list = sorted(listdir('../data/json/districtwise/'))
	print("Closing daily district files")
	for state in progressBar(state_list):
		if state == 'STATE':
			continue
		district_list = sorted(listdir('../data/json/districtwise/' + state))
		for district in district_list:
			district_parent_dir = '../data/json/districtwise/' + state + '/' + district
			with open(district_parent_dir + '/daily.json', 'a', encoding='utf-8') as json_file:
				json_file.write("}")

def main():
	download_raw_daily_data()
	process_raw_daily_files()

if __name__ == "__main__":
	main()
