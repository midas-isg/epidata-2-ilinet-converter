import Epidata
import csv
import sys

def get_weeks_for_season(year):
	weeks = []
	for week in range(40,54):
		weeks.append(str(year)+str(week))

	year = str(int(year) + 1)
	for week in range(1,21):
		pad = ""
		if week < 10:
			pad = "0"
		weeks.append(str(year)+pad+str(week))

	return weeks


def do_year(season, region):
	filename = season + "-" + region;

	year = season
	weeks = get_weeks_for_season(year)
	for week in weeks:
		epiweek_request = weeks[0] + "-" + week;
		curfilename = filename + "-" + "EW" + str(week) + ".csv"
		o = Epidata.Epidata.fluview(region, epiweek_request, issues=week)
		if o['result'] != 1:
			print("Error: No results for epiweek: " + epiweek_request)
		else:
			with open(curfilename, 'w') as f:  # Just use 'w' mode in 3.x
				f.write("PERCENTAGE OF VISITS FOR INFLUENZA-LIKE-ILLNESS REPORTED BY SENTINEL PROVIDERS\nREGION TYPE,REGION,YEAR,WEEK,% WEIGHTED ILI,%UNWEIGHTED ILI,AGE 0-4,AGE 25-49,AGE 25-64,AGE 5-24,AGE 50-64,AGE 65,ILITOTAL,NUM. OF PROVIDERS,TOTAL PATIENTS\n")
				num_results = len(o.get("epidata"))
				for i in range(num_results):
					r = o.get("epidata")[i]

					epiweek_full = str(r["epiweek"])
					epiweek_year = epiweek_full[:4]
					epiweek_week = epiweek_full[4:]

					if r["region"] == "nat":
						print_region = "X"
						region_type = "National"
					else:
						print_region = "Region " + r["region"][-1:]
						region_type = "HHS Regions"

					if len(epiweek_year) != 4:
						sys.exit(-1)

					f.write(region_type + ",")
					f.write(print_region+ ",")
					f.write(epiweek_year+ ",")
					f.write(epiweek_week+ ",")
					f.write(str(r["wili"])+ ",")
					f.write(str(r["ili"]) + ",")
					f.write(str(r["num_age_0"]) + ",")
					f.write(str(r["num_age_1"]) + ",")
					f.write(str(r["num_age_2"]) + ",")
					f.write(str(r["num_age_3"]) + ",")
					f.write(str(r["num_age_4"]) + ",")
					f.write(str(r["num_age_5"]) + ",")
					f.write(str(r["num_ili"]) + ",")
					f.write(str(r["num_providers"]) + ",")
					f.write(str(r["num_patients"]))
					f.write("\n")

if __name__ == '__main__':
	fieldnames = ['REGION TYPE', 'REGION', 'YEAR', 'WEEK', '% WEIGHTED ILI', '%UNWEIGHTED ILI', 'AGE 0-4', 'AGE 25-49', 'AGE 25-64', 'AGE 5-24', 'AGE 50-64', 'AGE 65', 'ILITOTAL', 'NUM. OF PROVIDERS', 'TOTAL PATIENTS']

	#	{'release_date': '2014-10-03', 'region': 'nat', 'issue': 201439, 'epiweek': 201439, 'lag': 0, 'num_ili': 7987,
	#	 'num_patients': 643078, 'num_providers': 1321, 'num_age_0': 2215, 'num_age_1': 3163, 'num_age_2': None,
	#	 'num_age_3': 1661, 'num_age_4': 584, 'num_age_5': 364, 'wili': 1.1151346010797, 'ili': 1.2419955277587}]

	#years =['2015','2016','2017','2018']
	years = ['2014']
	for year in years:
		regions = ['nat', 'hhs1', 'hhs2', 'hhs3', 'hhs4', 'hhs5', 'hhs6', 'hhs7', 'hhs8', 'hhs9', 'hhs10']
		for region in regions:
			print(year + " " + region)
			do_year(year, region)