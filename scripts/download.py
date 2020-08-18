import requests
import json
from datetime import datetime
url = {}
url['states_daily'] = "https://api.covid19india.org/states_daily.json"

def statewise_timeseries(statecode):
	r = requests.get(url['states_daily'])
	r = r.json()
	print(r)
	maharashtra_time_series = {}
	for i in r['states_daily']:
		# maharashtra_time_series[i["date"]]
		i["date"] = datetime.strptime(i["date"], "%d-%b-%y").strftime("%d-%m-%Y")
		
		if  i["date"] not in maharashtra_time_series:
			maharashtra_time_series[i["date"]] = {}
		maharashtra_time_series[i["date"]][i["status"]] = i[statecode]
		# print(i["date"] + "\t\t" + i["status"])
	for day in maharashtra_time_series.values():
		print(day)
		day["Confirmed"] = int(day["Confirmed"])
		day["Recovered"] = int(day["Recovered"])
		day["Deceased"] = int(day["Deceased"])
		day["Active"] = day["Confirmed"] - day["Recovered"] - day["Deceased"]
		# collections.OrderedDict(sorted(d.items()))
	print(maharashtra_time_series)
	with open('../data/json/test.json', 'w', encoding='utf-8') as f:
		json.dump(maharashtra_time_series, f, ensure_ascii=False, indent=4)

statewise_timeseries("mh")
# print( date.date()) 